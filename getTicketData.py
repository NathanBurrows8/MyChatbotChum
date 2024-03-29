# This file is the web-scraping file, called by the Knowledge Engine when it has everything it
# needs, and wants to display a ticket.

import re
import string
import requests
import csv
import json
from bs4 import BeautifulSoup
import processUserInput
import userInterface

websiteDate = ""
websiteReturnDate = ""
page = ""

#A file of station CRS codes is opened, and the file tries to substitute both departure and arrival locations for
#a corresponding CRS code. If this cannot be found, a general search for the users text is done instead.
#e.g. if the user inputs Norwich, this gets substituted to NRW. if they enter London, nothing is done
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

    try:
        websiteDestination = stationCodes[websiteDestination]
    except Exception as e:
        print("{No specific station found for '" + websiteDestination +
              "'. Attempting to search using the location instead..}")
    return websiteDeparture, websiteDestination

#This is the validation of each station in the delay prediction mode, where each station is instantly validated
#after input. If the users text does not match a CRS code, the validation will fail
def searchForSingleStation(text):
    stationCodes = {}
    reader = csv.reader(open("static/crs_codes.csv"))
    for row in reader:
        key = row[0]
        stationCodes[key] = row[1]
    try:
        temp = stationCodes[string.capwords(text)]
    except KeyError as e:
        return False
    return temp


#This is called from the KE and generates the correct website for a return ticket
def formWebsiteReturn(websiteDeparture, websiteDestination, siteDate, websiteTime, websiteType, siteReturnDate, websiteReturnTime, websiteReturnType):
    websiteDeparture, websiteDestination = searchForLocations(websiteDeparture, websiteDestination)
    global websiteDate, websiteReturnDate
    websiteDate = siteDate
    websiteReturnDate = siteReturnDate

    website = "https://ojp.nationalrail.co.uk/service/timesandfares/" + websiteDeparture + "/" + websiteDestination \
              + "/" + websiteDate + "/" + websiteTime + "/" + websiteType + "/" + websiteReturnDate + "/" \
              + websiteReturnTime + "/" + websiteReturnType
    getData(website)

#This is called from the KE and generates the correct website for a single ticket
def formWebsite(websiteDeparture, websiteDestination, siteDate, websiteTime, websiteType):
    global websiteDate
    websiteDate = siteDate
    websiteDeparture, websiteDestination = searchForLocations(websiteDeparture, websiteDestination)
    website = "https://ojp.nationalrail.co.uk/service/timesandfares/" + websiteDeparture + "/" + websiteDestination \
              + "/" + websiteDate + "/" + websiteTime + "/" + websiteType
    getData(website)

#This function scrapes the website and gets all tickets that are highlighted golden (the cheapest ones) in a list.
#The cheapest price is also scraped here
def getData(website):
    global page
    page = requests.get(website)
    # scraping all html
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        price = re.search("(?<=Buy cheapest for £ )(\d?)(\d?)\d.\d\d", str(soup)).group(0)
        hasCheapest = []
        for item in soup.find_all("td", class_="fare has-cheapest"):
            # getting cheapest fare item from table
            hasCheapest.append(str(item))
        parseData(hasCheapest, website, price)
    except AttributeError:
        userInterface.send_response("Sorry, I didn't understand that query! Would you like me to help you make a booking, or find potential delays?")
        processUserInput.resetStrings()




def parseData(hasCheapest, website, price):
    #Depending on how many cheapest tickets were found, different json data is loaded from this
    global page

    if len(hasCheapest) == 1 and processUserInput.isReturn == "false":
        # single journey
        soup1 = BeautifulSoup(hasCheapest[0], 'html.parser')
        scriptTag = soup1.find('script')  # print this to find all data given by National Rail
        data = json.loads(scriptTag.contents[0])
        dict1 = data['jsonJourneyBreakdown']
        dict2 = data['singleJsonFareBreakdowns'][0]

        printTicket(dict1, dict2, price, website)

    elif len(hasCheapest) == 2 and processUserInput.isReturn == "true":
        #return journey with 2 single tickets being the cheapest option
        soup1 = BeautifulSoup(hasCheapest[0], 'html.parser')
        scriptTag = soup1.find('script')  # print this to find all data given by National Rail
        data = json.loads(scriptTag.contents[0])
        dict1 = data['jsonJourneyBreakdown']
        dict2 = data['singleJsonFareBreakdowns'][0]

        soup1 = BeautifulSoup(hasCheapest[1], 'html.parser')
        scriptTag = soup1.find('script')  # print this to find all data given by National Rail
        data2 = json.loads(scriptTag.contents[0])
        dict3 = data2['jsonJourneyBreakdown']
        dict4 = data2['singleJsonFareBreakdowns'][0]


        printReturnTicket(dict1, dict2, dict3, dict4, price, website)

    elif len(hasCheapest) == 1 and processUserInput.isReturn == "true":
        #return journey with 1 return ticket being the cheapest option -- however, just printing 1 ticket will not
        #display properly. So, we scrape the ticket that is highlighted as automatically SELECTED instead and
        #display that alongside with the outbound ticket.
        soup1 = BeautifulSoup(hasCheapest[0], 'html.parser')
        scriptTag = soup1.find('script')  # print this to find all data given by National Rail
        data = json.loads(scriptTag.contents[0])
        dict1 = data['jsonJourneyBreakdown']
        dict2 = data['singleJsonFareBreakdowns'][0]

        #sometimes the return is not selected as the cheapest, so here is the workaround to get the return that is
        #automatically selected by the website, when it is not highlighted as the cheapest (it is labelled as SELECTED)
        dict3 = {}
        dict4 = {}
        soup = BeautifulSoup(page.content, 'html.parser')
        for item in soup.find_all("td", class_="fare"):
            soup1 = BeautifulSoup(str(item), 'html.parser')
            labelTag = soup1.find('label')
            match = re.search("checked", str(labelTag))
            match1 = re.search("returnFareLabel", str(labelTag))
            if match and match1:
                soup1 = BeautifulSoup(str(item), 'html.parser')
                scriptTag = soup1.find('script')
                data2 = json.loads(str(scriptTag.contents[0]))
                dict3 = data2['jsonJourneyBreakdown']
                dict4 = data2['singleJsonFareBreakdowns'][0]
                break

        printReturnTicket(dict1, dict2, dict3, dict4, price, website)


    else:
        print("No results were found for the journey - were the locations inputted correctly?")
        userInterface.send_response("Oops! I couldn't find any results for that journey, please try again."
        + " I can help you book a train ticket, or predict delays, what would you like me to do?")
        print(website)

def printReturnTicket(dict1, dict2, dict3, dict4, price, website):
    #This function displays the complete ticket data for a return ticket.
    #Many of the lines below are syntax changes to display the time and change numbers effectively. The robot will now
    #say '1 minute' '1 hour and 1 minute' 'exactly 1 hour' 'exactly 2 hours' '2 hours and 2 minutes' '1 change' etc
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

            #this is the ticket string being formed for the outbound journey
    ticket = "------------------------FOR " + websiteDate[0:2] + "/" + websiteDate[2:4] + "/" + websiteDate[4:6] \
            + "-----------------------<br> The cheapest outbound journey departs from " + str(dict1['departureStationName']) \
            + " at " + str(dict1['departureTime']) + ", and arrives at " + str(dict1['arrivalStationName']) + " at " \
            + str(dict1['arrivalTime']) + ".<br> " + timeString + "(Journey provided by " + str(dict2['tocName']) \
            + ")<br>"

            #detailing any possible disruptions on the route
    if dict1['statusIcon'] == "AMBER_TRIANGLE":
        if dict1['statusMessage'] == "bus service":
            ticket = ticket + "(Some or all of this journey is via bus. Check the booking website for details.)<br>"
        else:
            ticket = ticket + "(There may be some disruption on this route. Check the booking website for details.) <br>"
            #below is the same, but for the inbound journey
    ticket = ticket + "------------------------FOR " + websiteReturnDate[0:2] + "/" + websiteReturnDate[2:4] + "/" + websiteReturnDate[4:6] \
            + "-----------------------<br> The cheapest inbound journey departs from " + str(dict3['departureStationName']) \
            + " at " + str(dict3['departureTime']) + ", and arrives at " + str(dict3['arrivalStationName']) + " at " \
            + str(dict3['arrivalTime']) + ".<br>" + timeString1 + "(Journey provided by " + str(dict4['tocName']) \
            + ")<br>"

    if dict3['statusIcon'] == "AMBER_TRIANGLE":
        if dict3['statusMessage'] == "bus service":
            ticket = ticket + "(Some or all of this journey is via bus. Check the booking website for details.)<br>"
        else:
            ticket = ticket + "(There may be some disruption on this route. Check the booking website for details.) <br>"

    ticket = ticket + "<br> This return ticket will cost £" + price + ".<br> To view your booking, <a href=\""\
                    + website + "\" target=\"_blank\"> click here.</a> <br> "

    userInterface.send_response(ticket)
    print(website)
    processUserInput.givenTicket = "true"


def printTicket(dict1, dict2, price, website):
    #below is the same function in essence, but for a single ticket instead of a return ticket
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
             + "The ticket will cost £" + price + ".<br> To view your booking, <a href=\"" \
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