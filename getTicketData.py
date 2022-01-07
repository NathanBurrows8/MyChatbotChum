import requests
import csv
import json
from bs4 import BeautifulSoup
import processUserInput
import userInterface

websiteDate = ""
websiteReturnDate = ""

def searchForLocations(websiteDeparture, websiteDestination):
    stationCodes = {}
    reader = csv.reader(open('static/crs_codes.csv'))
    for row in reader:
        key = row[0]
        stationCodes[key] = row[1]
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
    return websiteDeparture, websiteDestination


def formWebsiteReturn(websiteDeparture, websiteDestination, siteDate, websiteTime, websiteType, siteReturnDate, websiteReturnTime, websiteReturnType):
    websiteDeparture, websiteDestination = searchForLocations(websiteDeparture, websiteDestination)
    global websiteDate, websiteReturnDate
    websiteDate = siteDate
    websiteReturnDate = siteReturnDate

    website = "https://ojp.nationalrail.co.uk/service/timesandfares/" + websiteDeparture + "/" + websiteDestination \
              + "/" + websiteDate + "/" + websiteTime + "/" + websiteType + "/" + websiteReturnDate + "/" \
              + websiteReturnTime + "/" + websiteReturnType
    getData(website)


def formWebsite(websiteDeparture, websiteDestination, siteDate, websiteTime, websiteType):
    global websiteDate
    websiteDate = siteDate
    websiteDeparture, websiteDestination = searchForLocations(websiteDeparture, websiteDestination)
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
        print(website)


def printReturnTicket(dict1, dict2, dict3, dict4, cheapestOutboundPrice, cheapestInboundPrice, website):
    global websiteDate
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
    processUserInput.givenTicket = "true"


def printTicket(dict1, dict2, cheapestPrice, website):
    global websiteDate, websiteReturnDate
    ticket = "------------------------FOR " + websiteDate[0:2] + "/" + websiteDate[2:4] + "/" + websiteDate[4:6] \
             + "-----------------------<br> The cheapest journey departs from " \
             + str(dict1['departureStationName']) + "</mark> at " + str(dict1['departureTime']) + ", and arrives at " \
             + str(dict1['arrivalStationName']) + " at " + str(dict1['arrivalTime']) + ".<br> The journey will take " \
             + str(dict1['durationHours']) + " hours and " + str(dict1['durationMinutes']) + " minutes, and has " \
             + str(dict1['changes']) + " changes.<br> The ticket will cost £" + f'{cheapestPrice:.2f}' + ".<br>" \
             + "To view your booking, <a href=\"" + website + "\" target=\"_blank\"> click here.</a> <br> " \
             + "(Journey provided by " + str(dict2['tocName']) + ")<br>"
    if dict1['statusIcon'] == "AMBER_TRIANGLE":
        if dict1['statusMessage'] == "bus service":
            ticket = ticket + "(Some or all of this journey is via bus. Check the booking website for details)<br>"
        else:
            ticket = ticket + "(There may be some disruption on this route. Check the booking website for details)"

    userInterface.send_response(ticket)
    print(website)
    processUserInput.givenTicket = "true"
