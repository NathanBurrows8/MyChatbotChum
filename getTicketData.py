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
websiteDeparture = stationCodes["Fleet"]
websiteDestination = stationCodes["Norwich"]
websiteDate = "271221"
websiteTime = "1230"
websiteType = "dep"  # 'dep' = "depart after", 'arr' = "arrive before"

website = "https://ojp.nationalrail.co.uk/service/timesandfares/" + websiteDeparture + "/" + websiteDestination + "/" \
          + websiteDate + "/" + websiteTime + "/" + websiteType
        #need to add functionality for return tickets, and arrive before tickets <- not done yet, but easy
        #also the user needs to be given the final web link to their ticket

page = requests.get(website)
# scraping all html
soup = BeautifulSoup(page.content, 'html.parser')
parsedString = ""
for item in soup.find_all("td", class_="fare has-cheapest"):
    # getting cheapest fare item from table
    parsedString = str(item)
# getting just script tag from cheapest item
soup1 = BeautifulSoup(parsedString, 'html.parser')
scriptTag = soup1.find('script')  # print this to find all data given by National Rail
data = json.loads(scriptTag.contents[0])
dict1 = data['jsonJourneyBreakdown']
dict2 = data['singleJsonFareBreakdowns'][0]
cheapestPrice = (dict2['ticketPrice'])


print("-----------------------------FOR " + websiteDate[0:2] + "/" + websiteDate[2:4] + "/" + websiteDate[4:6] +
      "----------------------------")
print("The cheapest journey departs from " + str(dict1['departureStationName']) + " at " + str(dict1['departureTime']) +
      ", and arrives at " + str(dict1['arrivalStationName']) + " at " + str(dict1['arrivalTime']) + ".")
print("The journey will take " + str(dict1['durationHours']) + " hours and " + str(dict1['durationMinutes']) +
      " minutes, and has " + str(dict1['changes']) + " changes.")
print("The ticket will cost £" + f'{cheapestPrice:.2f}' + ".")
print("(Journey provided by " + str(dict2['tocName']) + ")")

#if a journey needs multiple tickets price needs to be added - this is fleet to norwich:
#{"jsonJourneyBreakdown":{"departureStationName":"Fleet","departureStationCRS":"FLE","arrivalStationName":"Norwich","arrivalStationCRS":"NRW","statusMessage":null,"departureTime":"12:34","arrivalTime":"17:37","durationHours":5,"durationMinutes":3,"changes":6,"journeyId":1,"responseId":4,"statusIcon":"AMBER_TRIANGLE","hoverInformation":null},"singleJsonFareBreakdowns":[{"breakdownType":"SingleFare","fareTicketType":"Evening Out Single","ticketRestriction":"UL","fareRouteDescription":"Travel is allowed via any permitted route.","fareRouteName":"ANY PERMITTED","passengerType":"Adult","railcardName":"","ticketType":"Evening Out Single","ticketTypeCode":"EVA","fareSetter":"SWT","fareProvider":"South Western Railway","tocName":"South Western Railway","tocProvider":"South Western Railway","fareId":10078,"numberOfTickets":1,"fullFarePrice":6.0,"discount":0,"ticketPrice":6.0,"cheapestFirstClassFare":59.8,"nreFareCategory":"FLEXIBLE","redRoute":true},{"breakdownType":"SingleFare","fareTicketType":"Advance (Standard Class)","ticketRestriction":"OB","fareRouteDescription":"Only valid on booked Greater Anglia services and required connecting services.","fareRouteName":"AP GRTANG&CONCTS","passengerType":"Adult","railcardName":"","ticketType":"Advance (Standard Class)","ticketTypeCode":"OS4","fareSetter":"LER","fareProvider":"Greater Anglia","tocName":"Greater Anglia","tocProvider":"Greater Anglia","fareId":10089,"numberOfTickets":1,"fullFarePrice":37.5,"discount":0,"ticketPrice":37.5,"cheapestFirstClassFare":28.3,"nreFareCategory":"RESTRICTED","redRoute":true}],"returnJsonFareBreakdowns":[]}