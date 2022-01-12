import json
import requests

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
    r = requests.post(api_AllTrains, headers=headers, auth=auths, json=data)
    services = r.json().get("Services")
    ridList = []
    if services:
        for rid in services:
            individualTrain = rid.get("serviceAttributesMetrics").get("rids")
            for train in individualTrain:
                ridList.append(train)
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

if "__main__" == __name__:
    #this may take a little while
    #print(getTrainRIDS("NRW", "LST", "0700", "0800", "2016-07-01", "2016-08-01"))
    print(getDataFromRID("201607043432691"))

