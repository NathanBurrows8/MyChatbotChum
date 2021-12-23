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
websiteDeparture = stationCodes["Northampton"]
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
#below is the addition of multiple tickets in journey, the final price is all ticket prices combined
amountOfTicketsInJourney = len(data['singleJsonFareBreakdowns'])
cheapestPrice = 0
for x in range(0, amountOfTicketsInJourney):
    cheapestPrice += data['singleJsonFareBreakdowns'][x]['ticketPrice']



print("-----------------------------FOR " + websiteDate[0:2] + "/" + websiteDate[2:4] + "/" + websiteDate[4:6] +
      "----------------------------")
print("The cheapest journey departs from " + str(dict1['departureStationName']) + " at " + str(dict1['departureTime']) +
      ", and arrives at " + str(dict1['arrivalStationName']) + " at " + str(dict1['arrivalTime']) + ".")
print("The journey will take " + str(dict1['durationHours']) + " hours and " + str(dict1['durationMinutes']) +
      " minutes, and has " + str(dict1['changes']) + " changes.")
print("The ticket will cost £" + f'{cheapestPrice:.2f}' + ".")
print("(Journey provided by " + str(dict2['tocName']) + ")")
print(website)
