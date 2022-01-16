import json
import requests
import datetime
from sklearn.neural_network import MLPRegressor
import numpy as np

api_AllTrains = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
api_SpecificTrain = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"

#use top API to get train RIDS of certain route, then get specific data on each one with the bottom API
#need some CRS code validation? maybe refuse to go further in conversation without CRS code match
headers = { "Content-Type": "application/json" }
auths = ("nathanburrows68@gmail.com", "Jwc2dY4q4M2i!!8")

#this is the history of a train route between certain times
def getTrainRIDS(departureCode, arrivalCode, departureTime, arrivalTime, departureDate, arrivalDate):
    #change date here to "YYYY-MM-DD"
    data = {
      "from_loc": departureCode,
      "to_loc": arrivalCode,
      "from_time": departureTime,
      "to_time": arrivalTime,
      "from_date": departureDate,
      "to_date": arrivalDate,
      "days": "WEEKDAY"
    }
    print("Getting train data...")
    r = requests.post(api_AllTrains, headers=headers, auth=auths, json=data)
    services = r.json().get("Services")
    ridList = []
    if services:
        for rid in services:
            individualTrain = rid.get("serviceAttributesMetrics").get("rids")
            for train in individualTrain:
                ridList.append(str(train))
        return ridList
    else:
        return False #error handle this

#this is the individual train data from a train on that route
def getDataFromRID(rid):
    data = {
        "rid": rid
    }
    r = requests.post(api_SpecificTrain, headers=headers, auth=auths, json=data)
    trainData = r.json()
    return trainData

def predict(departureCode, arrivalCode, stationCode, delayInMinutes):
    ridList = getTrainRIDS(departureCode, arrivalCode, "0700", "0800", "2016-07-01", "2016-08-01")
    inputArray = []
    trainDataList = []
    for rid in ridList:
        trainDataList.append(getDataFromRID(rid))

    location_list = []
    for i in trainDataList:
        location_list.append(i['serviceAttributesDetails']['locations'])

    if len(location_list) == 0:
        print("Error")
    else:
        for i in location_list:
            for j in i:
                if j['location'] == stationCode:
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

                elif j['location'] == arrivalCode and len(str(delayAtStation)) != 0:
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

    arr = np.array(inputArray)
    print("Predicting delay...")
    nn = MLPRegressor(max_iter=5000).fit(arr[:, :-1], arr[:, -1])
    prediction = nn.predict([[delayInMinutes]])
    return prediction

if "__main__" == __name__:
    #print a prediction of the train from norwich to london - im at ipswich, and there has been a 2 minute delay announced
    print(predict("NRW", "LST", "IPS", 2))




#INPUT: delay at specific station (actual dep - expected dep)   OUTPUT: delay at last station (actual arr - expected arr)
#if prediction < 1, then we do not predict any extra delays as well as what was already announced