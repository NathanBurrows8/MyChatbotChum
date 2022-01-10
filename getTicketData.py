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
        userInterface.send_response("Oops! I couldn't find any results for that journey, please try again."
        + " I can help you book a train ticket, or predict delays, what would you like me to do?")
        print(website)

def printReturnTicket(dict1, dict2, dict3, dict4, cheapestOutboundPrice, cheapestInboundPrice, website):
    global websiteDate, websiteReturnDate
    timeString = "This journey will take "
    extraTimeString = ""
    extraMinuteString = ""
    andNeeded = True
    exactlyNeeded = False
    pluralForChanges = "s"
    if str(dict1['changes']) == "1":
        pluralForChanges = ""
    if str(dict1['durationHours']) == "0":
        andNeeded = False
    elif str(dict1['durationHours']) == "1":
        extraTimeString = "1 hour "
    else:
       extraTimeString = str(dict1['durationHours']) + " hours "
    if str(dict1['durationMinutes']) == "0":
        exactlyNeeded = True
        andNeeded = False
    elif str(dict1['durationMinutes']) == "1":
        extraMinuteString = "1 minute, "
    else:
        extraMinuteString = str(dict1['durationMinutes']) + " minutes, "

    if andNeeded:
        timeString = timeString + extraTimeString + " and "  + extraMinuteString + "and has " + str(dict1['changes']) \
            + " change" + pluralForChanges + ".<br>"
    else:
        if exactlyNeeded:
            timeString = timeString + "exactly " + extraTimeString + "and has " + str(dict1['changes']) \
                + " change" + pluralForChanges + ".<br>"
        else:
            timeString = timeString + extraTimeString + extraMinuteString + "and has " + str(dict1['changes']) \
                + " change" + pluralForChanges + ".<br>"

    timeString1 = "This journey will take "
    extraTimeString1 = ""
    extraMinuteString1 = ""
    andNeeded1 = True
    exactlyNeeded1 = False
    pluralForChanges1 = "s"
    if str(dict3['changes']) == "1":
        pluralForChanges1 = ""
    if str(dict3['durationHours']) == "0":
        andNeeded1 = False
    elif str(dict3['durationHours']) == "1":
        extraTimeString1 = "1 hour "
    else:
        extraTimeString1 = str(dict3['durationHours']) + " hours "
    if str(dict3['durationMinutes']) == "0":
        exactlyNeeded1 = True
        andNeeded1 = False
    elif str(dict3['durationMinutes']) == "1":
        extraMinuteString1 = "1 minute, "
    else:
        extraMinuteString1 = str(dict3['durationMinutes']) + " minutes, "

    if andNeeded1:
        timeString1 = timeString1 + extraTimeString1 + " and " + extraMinuteString1 + "and has " + str(dict3['changes']) \
                     + " change" + pluralForChanges1 + ".<br>"
    else:
        if exactlyNeeded1:
            timeString1 = timeString1 + "exactly " + extraTimeString1 + "and has " + str(dict3['changes']) \
                         + " change" + pluralForChanges1 + ".<br>"
        else:
            timeString1 = timeString1 + extraTimeString1 + extraMinuteString1 + "and has " + str(dict3['changes']) \
                         + " change" + pluralForChanges1 + ".<br>"

    ticket = "------------------------FOR " + websiteDate[0:2] + "/" + websiteDate[2:4] + "/" + websiteDate[4:6] \
            + "-----------------------<br> The cheapest outbound journey departs from " + str(dict1['departureStationName']) \
            + " at " + str(dict1['departureTime']) + ", and arrives at " + str(dict1['arrivalStationName']) + " at " \
            + str(dict1['arrivalTime']) + ".<br> " + timeString + "(Journey provided by " + str(dict2['tocName']) \
            + ")<br>"


    if dict1['statusIcon'] == "AMBER_TRIANGLE":
        if dict1['statusMessage'] == "bus service":
            ticket = ticket + "(Some or all of this journey is via bus. Check the booking website for details.)<br>"
        else:
            ticket = ticket + "(There may be some disruption on this route. Check the booking website for details.) <br>"
    ticket = ticket + "------------------------FOR " + websiteReturnDate[0:2] + "/" + websiteReturnDate[2:4] + "/" + websiteReturnDate[4:6] \
            + "-----------------------<br> The cheapest inbound journey departs from " + str(dict3['departureStationName']) \
            + " at " + str(dict3['departureTime']) + ", and arrives at " + str(dict3['arrivalStationName']) + " at " \
            + str(dict3['arrivalTime']) + ".<br>" + timeString1 + "(Journey provided by " + str(dict4['tocName']) \
            + ")<br>"

    if dict1['statusIcon'] == "AMBER_TRIANGLE":
        if dict1['statusMessage'] == "bus service":
            ticket = ticket + "(Some or all of this journey is via bus. Check the booking website for details.)<br>"
        else:
            ticket = ticket + "(There may be some disruption on this route. Check the booking website for details.) <br>"

    ticket = ticket + "<br> This return ticket will cost £" + f'{cheapestOutboundPrice + cheapestInboundPrice:.2f}' \
             + ". " + "(Outbound = £" + f'{cheapestOutboundPrice:.2f}' + ", Inbound = £" \
             + f'{cheapestOutboundPrice:.2f}' + ")<br> To view your booking, <a href=\"" + website \
             + "\" target=\"_blank\"> click here.</a> <br> "

    userInterface.send_response(ticket)
    print(website)
    processUserInput.givenTicket = "true"


def printTicket(dict1, dict2, cheapestPrice, website):
    global websiteDate
    timeString = "The journey will take "
    extraTimeString = ""
    extraMinuteString = ""
    andNeeded = True
    exactlyNeeded = False
    pluralForChanges = "s"
    if str(dict1['changes']) == "1":
        pluralForChanges = ""
    if str(dict1['durationHours']) == "0":
        andNeeded = False
    elif str(dict1['durationHours']) == "1":
        extraTimeString = "1 hour "
    else:
       extraTimeString = str(dict1['durationHours']) + " hours "
    if str(dict1['durationMinutes']) == "0":
        exactlyNeeded = True
        andNeeded = False
    elif str(dict1['durationMinutes']) == "1":
        extraMinuteString = "1 minute, "
    else:
        extraMinuteString = str(dict1['durationMinutes']) + " minutes, "

    if andNeeded:
        timeString = timeString + extraTimeString + " and "  + extraMinuteString + "and has " + str(dict1['changes']) \
            + " change" + pluralForChanges + ".<br>"
    else:
        if exactlyNeeded:
            timeString = timeString + "exactly " + extraTimeString + "and has " + str(dict1['changes']) \
                + " change" + pluralForChanges + ".<br>"
        else:
            timeString = timeString + extraTimeString + extraMinuteString + "and has " + str(dict1['changes']) \
                + " change" + pluralForChanges + ".<br>"

    ticket = "------------------------FOR " + websiteDate[0:2] + "/" + websiteDate[2:4] + "/" + websiteDate[4:6] \
             + "-----------------------<br> The cheapest journey departs from " \
             + str(dict1['departureStationName']) + "</mark> at " + str(dict1['departureTime']) + ", and arrives at " \
             + str(dict1['arrivalStationName']) + " at " + str(dict1['arrivalTime']) + ".<br>" + timeString \
             + "The ticket will cost £" + f'{cheapestPrice:.2f}' + ".<br> To view your booking, <a href=\"" \
             + website + "\" target=\"_blank\"> click here.</a> <br> " \
             + "(Journey provided by " + str(dict2['tocName']) + ")<br>"
    if dict1['statusIcon'] == "AMBER_TRIANGLE":
        if dict1['statusMessage'] == "bus service":
            ticket = ticket + "(Some or all of this journey is via bus. Check the booking website for details)<br>"
        else:
            ticket = ticket + "(There may be some disruption on this route. Check the booking website for details)"

    userInterface.send_response(ticket)
    print(website)
    processUserInput.givenTicket = "true"
