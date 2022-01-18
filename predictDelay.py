#This file takes in 3 stations (departure, arrival, current) and a quoted delay time, and attempts to predict
#the total delay at the user's arrival destination, using prior train data as a training set


import json
import requests
import datetime
from sklearn.neural_network import MLPRegressor
import numpy as np

import processUserInput
import userInterface

api_AllTrains = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
api_SpecificTrain = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"

#use top API to get train RIDS of certain route, then get specific data on each one with the bottom API
#need some CRS code validation? maybe refuse to go further in conversation without CRS code match
headers = { "Content-Type": "application/json" }
auths = ("nathanburrows68@gmail.com", "Jwc2dY4q4M2i!!8")

delayAtStation = ""

#this is the history of a train route between certain times
def getTrainRIDS(departureCode, arrivalCode, departureTime, arrivalTime, departureDate, arrivalDate):
    #date should be passed as YYYY-MM-DD
    data = {
      "from_loc": departureCode,
      "to_loc": arrivalCode,
      "from_time": departureTime,
      "to_time": arrivalTime,
      "from_date": departureDate,
      "to_date": arrivalDate,
      "days": "WEEKDAY"
    }
    userInterface.send_response("Getting train data...")
    r = requests.post(api_AllTrains, headers=headers, auth=auths, json=data)
    services = r.json().get("Services")
    ridList = []
    if services:
        for rid in services:
            individualTrain = rid.get("serviceAttributesMetrics").get("rids")
            for train in individualTrain:
                ridList.append(str(train))
        return ridList  #this list gets the ids of each train in a certain timespan on this route
    else:
        return False

#this is the individual train data from a train on that route
def getDataFromRID(rid):
    data = {
        "rid": rid
    }
    r = requests.post(api_SpecificTrain, headers=headers, auth=auths, json=data)
    trainData = r.json()
    return trainData

def predict(departureCode, arrivalCode, stationCode, delayInMinutes):
    global delayAtStation
    ridList = getTrainRIDS(departureCode, arrivalCode, "0700", "0800", "2016-07-01", "2016-08-01")
    #currently we are getting one months of data at a time, but this API call takes time
    if ridList is not False:
        inputArray = []
        trainDataList = []
        for rid in ridList:
            trainDataList.append(getDataFromRID(rid))

        location_list = []  #getting a list of all locations a train goes to during a certain route
        for i in trainDataList:
            location_list.append(i['serviceAttributesDetails']['locations'])

        if len(location_list) == 0:
            userInterface.send_response("Sorry, I cant find any train IDs for that route. "
                                        "Want me to predict another route, or book a train ticket?")
            processUserInput.resetStrings()
        else:
            for i in location_list:
                for j in i:     #iterating through each location
                    if j['location'] == stationCode:        #if this index is the station the user is at
                        expectedDep = j['gbtt_ptd']
                        if len(expectedDep) == 0:
                            break
                        expectedDepTime = datetime.datetime.strptime(expectedDep[0:2] + ":" + expectedDep[2:4], '%H:%M')
                        actualDep = j['actual_td']
                        if len(actualDep) == 0:
                            break
                        actualDepTime = datetime.datetime.strptime(actualDep[0:2] + ":" + actualDep[2:4], '%H:%M')
                        if actualDepTime < expectedDepTime:
                            actualDepTime = expectedDepTime
                        delayAtStation = int((actualDepTime - expectedDepTime).seconds / 60)    #in minutes

                    elif j['location'] == arrivalCode and len(str(delayAtStation)) != 0:    #if this index is the arrival station
                        if len(str(delayAtStation)) != 0:
                            expectedDep = j['gbtt_pta']
                            if len(expectedDep) == 0:
                                break
                            expectedDepTime = datetime.datetime.strptime(expectedDep[0:2] + ":" + expectedDep[2:4], '%H:%M')
                            actualDep = j['actual_ta']
                            if len(actualDep) == 0:
                                break
                            actualDepTime = datetime.datetime.strptime(actualDep[0:2] + ":" + actualDep[2:4], '%H:%M')
                            if actualDepTime < expectedDepTime:
                                actualDepTime = expectedDepTime
                            delayAtArrival = int((actualDepTime - expectedDepTime).seconds / 60)    #in minutes
                            inputArray.append([delayAtStation, delayAtArrival])
                        else:
                            userInterface.send_response("Sorry, it doesn't seem like this route was valid. "
                                                        "Want me to predict another route, or book a train ticket?")
                            processUserInput.resetStrings()


        arr = np.array(inputArray)
        userInterface.send_response("Predicting delay...")
        try:
            nn = MLPRegressor(max_iter=9000).fit(arr[:, :-1], arr[:, -1])   #a multilayer perceptron is the AI model
            prediction = nn.predict([[delayInMinutes]])[0]
            print("PREDICTION", prediction)
            prediction = int(prediction)
            if prediction < 1:
                userInterface.send_response(
                    "Good news! You are still expected to arrive on time. Thanks for using our service.")
            elif prediction == 1:
                userInterface.send_response(
                    "I predict that you will be just 1 minute late to your destination. Thanks for using our service.")
            else:
                userInterface.send_response("I predict that you will be " + str(
                    prediction) + " minutes late to your destination. Thanks for using our service.")
            processUserInput.resetStrings()
        except Exception:
            userInterface.send_response("Sorry, I can't find the station you're at on this route. Want me to predict another delay, or book a train ticket?")
            processUserInput.resetStrings()

    else:
        userInterface.send_response("Sorry, I couldn't find any results for this journey. Want me to predict another route, or book a train ticket?")
        processUserInput.resetStrings()


#INPUT: delay at specific station (actual dep - expected dep)   OUTPUT: delay at last station (actual arr - expected arr)
