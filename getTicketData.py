import requests
import csv
import json
from bs4 import BeautifulSoup

stationCodes = {}
reader = csv.reader(open('static/crs_codes.csv'))
for row in reader:
    key = row[0]
    stationCodes[key] = row[1]

# change these 5 things for now to test the program

websiteDeparture = "Norwich"
websiteDestination = "Swansea"
websiteDate = "200122"
websiteTime = "1100"    #no way to search website without a time? maybe just default to dep 10:00 or something
websiteType = "first"  # 'dep' = "depart after", 'arr' = "arrive before", 'last', 'first'<-for "depart before"
websiteReturnDate = "300122"
websiteReturnTime = "1300"
websiteReturnType = "dep"

try:
    websiteDeparture = stationCodes[websiteDeparture]
except Exception as e:
    print("{No specific station found for '" + websiteDeparture +
          "'. Attempting to search using the location instead..}")
    pass

try:
    websiteDestination = stationCodes[websiteDestination]
except Exception as e:
    print("{No specific station found for '" + websiteDestination +
          "'. Attempting to search using the location instead..}")


def formWebsiteReturn(websiteDeparture, websiteDestination, websiteDate, websiteTime, websiteType, websiteReturnDate,
                      websiteReturnTime, websiteReturnType):
    website = "https://ojp.nationalrail.co.uk/service/timesandfares/" + websiteDeparture + "/" + websiteDestination \
              + "/" + websiteDate + "/" + websiteTime + "/" + websiteType + "/" + websiteReturnDate + "/" \
              + websiteReturnTime + "/" + websiteReturnType
    getData(website)


def formWebsite(websiteDeparture, websiteDestination, websiteDate, websiteTime, websiteType):
    website = "https://ojp.nationalrail.co.uk/service/timesandfares/" + websiteDeparture + "/" + websiteDestination \
              + "/" + websiteDate + "/" + websiteTime + "/" + websiteType
    getData(website)


def getData(website):
    page = requests.get(website)
    # scraping all html
    soup = BeautifulSoup(page.content, 'html.parser')
    hasCheapest = []
    for item in soup.find_all("td", class_="fare has-cheapest"):
        # getting cheapest fare item from table
        hasCheapest.append(str(item))
    parseData(hasCheapest, website)


def parseData(hasCheapest, website):
    if len(hasCheapest) == 1:
        # single journey
        soup1 = BeautifulSoup(hasCheapest[0], 'html.parser')
        scriptTag = soup1.find('script')  # print this to find all data given by National Rail
        data = json.loads(scriptTag.contents[0])
        dict1 = data['jsonJourneyBreakdown']
        dict2 = data['singleJsonFareBreakdowns'][0]
        # below is the addition of multiple tickets in journey, the final price is all ticket prices combined
        amountOfTicketsInJourney = len(data['singleJsonFareBreakdowns'])
        cheapestPrice = 0
        for x in range(0, amountOfTicketsInJourney):
            cheapestPrice += data['singleJsonFareBreakdowns'][x]['ticketPrice']
        printTicket(dict1, dict2, cheapestPrice, website)
    elif len(hasCheapest) == 2:
        soup1 = BeautifulSoup(hasCheapest[0], 'html.parser')
        scriptTag = soup1.find('script')  # print this to find all data given by National Rail
        data = json.loads(scriptTag.contents[0])
        dict1 = data['jsonJourneyBreakdown']
        dict2 = data['singleJsonFareBreakdowns'][0]
        # below is the addition of multiple tickets in journey, the final price is all ticket prices combined
        amountOfTicketsInJourney = len(data['singleJsonFareBreakdowns'])
        cheapestOutboundPrice = 0
        for x in range(0, amountOfTicketsInJourney):
            cheapestOutboundPrice += data['singleJsonFareBreakdowns'][x]['ticketPrice']

        soup1 = BeautifulSoup(hasCheapest[1], 'html.parser')
        scriptTag = soup1.find('script')  # print this to find all data given by National Rail
        data2 = json.loads(scriptTag.contents[0])
        dict3 = data2['jsonJourneyBreakdown']
        dict4 = data2['singleJsonFareBreakdowns'][0]
        # below is the addition of multiple tickets in journey, the final price is all ticket prices combined
        amountOfTicketsInJourney = len(data2['singleJsonFareBreakdowns'])
        cheapestInboundPrice = 0
        for x in range(0, amountOfTicketsInJourney):
            cheapestInboundPrice += data2['singleJsonFareBreakdowns'][x]['ticketPrice']
        printReturnTicket(dict1, dict2, dict3, dict4, cheapestOutboundPrice, cheapestInboundPrice, website)
    else:
        print("No results were found for the journey - were the locations inputted correctly?")


def printReturnTicket(dict1, dict2, dict3, dict4, cheapestOutboundPrice, cheapestInboundPrice, website):
    print("-----------------------------FOR " + websiteDate[0:2] + "/" + websiteDate[2:4] + "/" + websiteDate[4:6] +
          "----------------------------")
    print("The cheapest outbound journey departs from " + str(dict1['departureStationName']) + " at " +
          str(dict1['departureTime']) + ", and arrives at " + str(dict1['arrivalStationName']) + " at " +
          str(dict1['arrivalTime']) + ".")
    print("The journey will take " + str(dict1['durationHours']) + " hours and " + str(dict1['durationMinutes']) +
          " minutes, and has " + str(dict1['changes']) + " changes.")
    print("(Journey provided by " + str(dict2['tocName']) + ")")
    if dict1['statusIcon'] == "AMBER_TRIANGLE":
        if dict1['statusMessage'] == "bus service":
            print("(Some or all of this journey is via bus. Check the booking website for details.)")
        else:
            print("(There may be some disruption on this route. Check the booking website for details.)")
    print("-----------------------------FOR " + websiteReturnDate[0:2] + "/" + websiteReturnDate[2:4] + "/" +
          websiteReturnDate[4:6] + "----------------------------")

    print("The cheapest inbound journey departs from " + str(dict3['departureStationName']) + " at " +
          str(dict3['departureTime']) + ", and arrives at " + str(dict3['arrivalStationName']) + " at " +
          str(dict3['arrivalTime']) + ".")
    print("The journey will take " + str(dict3['durationHours']) + " hours and " + str(dict3['durationMinutes']) +
          " minutes, and has " + str(dict3['changes']) + " changes.")
    print("(Journey provided by " + str(dict4['tocName']) + ")")
    if dict3['statusIcon'] == "AMBER_TRIANGLE":
        if dict3['statusMessage'] == "bus service":
            print("(Some or all of this journey is via bus. Check the booking website for details.)")
        else:
            print("(There may be some disruption on this route. Check the booking website for details.)")
    print("---------------------------------------------------------------------")
    print("The ticket will cost £" + f'{cheapestOutboundPrice + cheapestInboundPrice:.2f}' + ". " +
          "(Outbound = £" + f'{cheapestOutboundPrice:.2f}' + ", Inbound = £" + f'{cheapestOutboundPrice:.2f}' + ")")
    print(website)


def printTicket(dict1, dict2, cheapestPrice, website):
    print("-----------------------------FOR " + websiteDate[0:2] + "/" + websiteDate[2:4] + "/" + websiteDate[4:6] +
          "----------------------------")
    print("The cheapest journey departs from " + str(dict1['departureStationName']) + " at " + str(
        dict1['departureTime']) +
          ", and arrives at " + str(dict1['arrivalStationName']) + " at " + str(dict1['arrivalTime']) + ".")
    print("The journey will take " + str(dict1['durationHours']) + " hours and " + str(dict1['durationMinutes']) +
          " minutes, and has " + str(dict1['changes']) + " changes.")
    print("The ticket will cost £" + f'{cheapestPrice:.2f}' + ".")
    print("(Journey provided by " + str(dict2['tocName']) + ")")
    if dict1['statusIcon'] == "AMBER_TRIANGLE":
        if dict1['statusMessage'] == "bus service":
            print("(Some or all of this journey is via bus. Check the booking website for details.)")
        else:
            print("(There may be some disruption on this route. Check the booking website for details.)")
    print(website)



formWebsiteReturn(websiteDeparture, websiteDestination, websiteDate, websiteTime, websiteType, websiteReturnDate,
                  websiteReturnTime, websiteReturnType)
#formWebsite(websiteDeparture, websiteDestination, websiteDate, websiteTime, websiteType)





#needs validation! is time in past? etc