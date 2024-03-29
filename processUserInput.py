#this file mainly concerns labelling the users input text into certain groups (is it a date, time, location etc...)
#based on this label then certain actions can be taken
import calendar
import datetime
import spacy
import KnowledgeEngine
from spacy.matcher import Matcher
import re

import getTicketData
import userInterface

#using SpaCy to match regex. LOWER = make text lowercase. TEXT = exact match.
helloRegex = [
    {"LOWER": {"REGEX": "hi(?![\S])|hey(?![\S])|yo(?![\S])|hello(?![\S])"}}
]
goodbyeRegex = [
    {"LOWER": {"REGEX": "goodbye(?![\S])|bye(?![\S])|cya(?![\S])|quit(?![\S])|exit(?![\S])"}}
]
bookingRegex = [
    {"LOWER": {"REGEX": "booking|book|ticket|buy"}}
]
delayRegex = [
    {"LOWER": {"REGEX": "delay|delayed|delays|predict"}}
]
singleRegex = [
    {"LOWER": {"REGEX": "single"}}
]
returnRegex = [
    {"LOWER": {"REGEX": "return"}}
]
todayRegex = [
    {"LOWER": {"REGEX": "today"}}
]
tomorrowRegex = [
    {"LOWER": {"REGEX": "tomorrow"}}
]
weekRegex = [
    {"LOWER": {"REGEX": "monday|tuesday|wednesday|thursday|friday|saturday|sunday"}}
]
slashDateRegex = [  # matches dd/mm/yyyy
    {"TEXT": {"REGEX": "(\d\d)[/](\d\d)[/](\d\d\d\d)"}}
]
slashDateNoYearRegex = [  # matches dd/mm and assumes this year
    {"TEXT": {"REGEX": "^(\d\d)[/](\d\d)(?!/)"}}
]
slashDateShorterYearRegex = [  # matches dd/mm/yy
    {"TEXT": {"REGEX": "^(\d\d)[/](\d\d)[/](\d\d)(?!/|\d)"}}
]
writtenDateRegex = [
    {"LOWER": {"REGEX": "(\d?\d)([stndhr]{2})?"}},
    {"LOWER": {"REGEX": "(january|february|march|april|may|june|july|august|september|october|november|december)"}}
]
writtenDateShorterMonthRegex = [
    {"LOWER": {"REGEX": "(\d?\d)[stndhr]{2}?"}},
    {"LOWER": {"REGEX": "((jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec)(?!\w))"}}
]
writtenDateOfRegex = [
    {"LOWER": {"REGEX": "(\d?\d)([stndhr]{2})?"}},
    {"LOWER": {"REGEX": "of"}},
    {"LOWER": {"REGEX": "(january|february|march|april|may|june|july|august|september|october|november|december)"}}
]
writtenDateShorterMonthOfRegex = [
    {"LOWER": {"REGEX": "(\d?\d)([stndhr]{2})?"}},
    {"LOWER": {"REGEX": "of"}},
    {"LOWER": {"REGEX": "((jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec)(?!\w))"}}
]

timeRegex = [
    {"TEXT": {"REGEX": "(\d?\d)[:](\d\d)(?![\S])"}}
]
writtenTimeMorningRegex = [
    {"LOWER": {"REGEX": "(\d)?(\d)|(\d)?(\d)(([am]{2}))(?![\S])"}},
    {"LOWER": {"REGEX": "([am]{2})(?![\S])"}}
]
writtenTimeEveningRegex = [
    {"LOWER": {"REGEX": "(\d)?(\d)|(\d)?(\d)(([pm]{2}))(?![\S])"}},
    {"LOWER": {"REGEX": "([pm]{2})(?![\S])"}}
]
writtenTimeWithMinutesMorningRegex = [
    {"LOWER": {"REGEX": "(\d)?(\d)[:](\d\d)(([am]{2}))(?![\S])"}}
]
writtenTimeWithMinutesEveningRegex = [
    {"LOWER": {"REGEX": "(\d)?(\d)[:](\d\d)(([pm]{2}))(?![\S])"}}
]
wordTimeMorningRegex = [
    {"LOWER": {"REGEX": "morning"}}
]
wordTimeAfternoonRegex = [
    {"LOWER": {"REGEX": "afternoon"}}
]
wordTimeEveningRegex = [
    {"LOWER": {"REGEX": "evening|^(night)"}}
]
wordTimeNoonRegex = [
    {"LOWER": {"REGEX": "^(noon)|midday"}}
]
wordTimeMidnightRegex = [
    {"LOWER": {"REGEX": "midnight"}}
]
noTimeGivenRegex = [
    {"LOWER": {"REGEX": "whenever"}}
]
departBeforeTimeRegex = [
    {"LOWER": {"REGEX": "depart|leave|departing|leaving"}},
    {"LOWER": {"REGEX": "before"}}
]
arriveBeforeTimeRegex = [
    {"LOWER": {"REGEX": "arrive|arriving"}},
    {"LOWER": {"REGEX": "before"}}
]
dottedTimeWithSpaceMorningRegex = [
    {"TEXT": {"REGEX": "^(\d)?(\d)(?![\S])"}},
    {"LOWER": {"REGEX": "a.m."}}
]
dottedTimeWithSpaceEveningRegex = [
    {"TEXT": {"REGEX": "^(\d)?(\d)(?![\S])"}},
    {"LOWER": {"REGEX": "p.m."}}
]
thanksRegex = [
    {"LOWER": {"REGEX": "thanks|thankyou|thank(?![\S])|cheers|ty"}}
]

#   Regex Notes:
# currently 23rd jan works but not 23 jan - i think this is fine?
# currently '1:45 pm' only picks up 1pm
# 0am and 0pm are not split by spacy like 1am, etc, so we cannot get specific invalidDate error message
# currently 1:35 defaults to 1:35am
# "23rd feb 2023" fires writtenDateShorterMonth, which gives a valid string of 230222 <-- no regex to pick up written
#      date with a year


#these are the variables that the bot needs to make a valid request to National Rail or the MLPRegressor
isBooking = ""
isDelay = ""
websiteDeparture = ""
websiteDestination = ""
websiteDate = ""
websiteTime = ""
websiteType = ""
givenTicket = ""

isReturn = ""
websiteReturnDate = ""
websiteReturnTime = ""
websiteReturnType = ""

delayDepartureStation = ""
delayDestinationStation = ""
delayDepartureTime = ""
delayTimeFromUser = ""
delayStationUserIsAt = ""

nlp = spacy.load("en_core_web_sm")

#loading in all of the previous regex into a SpaCy matcher, that runs on every message sent by the user labelling it
matcher = Matcher(nlp.vocab)
matcher.add("hello", [helloRegex])
matcher.add("goodbye", [goodbyeRegex])
matcher.add("booking", [bookingRegex])
matcher.add("delay", [delayRegex])
matcher.add("today", [todayRegex])
matcher.add("tomorrow", [tomorrowRegex])
matcher.add("day", [weekRegex])
matcher.add("slashDate", [slashDateRegex])
matcher.add("slashDateNoYear", [slashDateNoYearRegex])
matcher.add("slashDateShorterYear", [slashDateShorterYearRegex])
matcher.add("writtenDate", [writtenDateRegex])
matcher.add("writtenDateShorterMonth", [writtenDateShorterMonthRegex])
matcher.add("writtenDateOf", [writtenDateOfRegex])
matcher.add("writtenDateShorterMonthOf", [writtenDateShorterMonthOfRegex])
matcher.add("writtenTimeMorning", [writtenTimeMorningRegex])
matcher.add("writtenTimeEvening", [writtenTimeEveningRegex])
matcher.add("writtenTimeWithMinutesMorning", [writtenTimeWithMinutesMorningRegex])
matcher.add("writtenTimeWithMinutesEvening", [writtenTimeWithMinutesEveningRegex])
matcher.add("time", [timeRegex])
matcher.add("wordTimeMorning", [wordTimeMorningRegex])
matcher.add("wordTimeEvening", [wordTimeEveningRegex])
matcher.add("wordTimeAfternoon", [wordTimeAfternoonRegex])
matcher.add("wordTimeNoon", [wordTimeNoonRegex])
matcher.add("wordTimeMidnight", [wordTimeMidnightRegex])
matcher.add("noTimeGiven", [noTimeGivenRegex])
matcher.add("single", [singleRegex])
matcher.add("return", [returnRegex])
matcher.add("departBefore", [departBeforeTimeRegex])
matcher.add("arriveBefore", [arriveBeforeTimeRegex])
matcher.add("dottedTimeWithSpaceMorning", [dottedTimeWithSpaceMorningRegex])
matcher.add("dottedTimeWithSpaceEvening", [dottedTimeWithSpaceEveningRegex])
matcher.add("thanks", [thanksRegex])


def labelUserInput(text):
    global websiteDeparture, websiteDestination, isReturn, websiteType, websiteDate, websiteTime, isBooking, websiteReturnType, givenTicket

    dictionary = {}
    now = datetime.datetime.now()

    nlptext = nlp(text)     #tokenising text
    for token in nlptext:
        print(token.text, token.pos_, token.dep_) #printing NLP text for debugging in console

    regex_matches = matcher(nlptext)
    for match_id, start, end in regex_matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        matchedtext = nlptext[start:end]  # The matched text
        dictionary[string_id] = matchedtext

    KEData = {} #this dictionary will be passed to the KE later
    for string_id in dictionary:
        #depending on what label the text has, different actions will be taken. Date needs to be a DDMMYY string,
        #Time needs to be an HHMM string etc..
        if string_id == "hello":
            KEData["hello"] = "true"
        elif string_id == "booking":
            KEData["booking"] = "true"
            isBooking = "true"
            parseFromAndTo(text)
            givenTicket = ""
            if "single" in text:
                KEData["single"] = "true"
                isReturn = "false"
            elif "return" in text:
                KEData["return"] = "true"
                isReturn = "true"
        elif string_id == "delay":
            KEData["delay"] = "true"
            isBooking = "false"
            givenTicket = ""
        elif string_id == "single":
            KEData["single"] = "true"
            parseFromAndTo(text)
            isReturn = "false"
        elif string_id == "return":
            KEData["return"] = "true"
            isReturn = "true"
            parseFromAndTo(text)
        elif string_id == "goodbye":
            KEData["goodbye"] = "true"
        elif string_id == "thanks":
            KEData["thanks"] = "true"
        elif string_id == "today":
            KEData["today"] = "true"
            date = str(now.day).zfill(2) + str(now.month).zfill(2) + str(now.year)[2:4]
            if validateDate(date):
                if isDateTooFarInFuture(date):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    setDate(date, KEData)
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "tomorrow":
            KEData["tomorrow"] = "true"
            tomorrow = now + datetime.timedelta(days=1)
            date = str(tomorrow.day).zfill(2) + str(tomorrow.month).zfill(2) + str(tomorrow.year)[2:4]
            if validateDate(date):
                if isDateTooFarInFuture(date):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    setDate(date, KEData)
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "day":
            KEData["day"] = "true"
            setWeekday(str(dictionary["day"]), KEData)
        elif string_id == "slashDate":
            KEData["slashDate"] = "true"
            date = str(dictionary["slashDate"])
            date = date.replace("/", "")
            date = date[0:4] + date[6:8]
            if validateDate(date):
                if isDateTooFarInFuture(date):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    setDate(date, KEData)
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "slashDateNoYear":
            KEData["slashDateNoYear"] = "true"
            date = str(dictionary["slashDateNoYear"])
            date = date.replace("/", "")
            date = date + str(now.year)[2:4]
            if validateDate(date):
                if isDateTooFarInFuture(date):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    setDate(date, KEData)
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "slashDateShorterYear":
            KEData["slashDateShorterYear"] = "true"
            date = str(dictionary["slashDateShorterYear"])
            date = date.replace("/", "")
            if validateDate(date):
                if isDateTooFarInFuture(date):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    setDate(date, KEData)
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "writtenDate":
            KEData["writtenDate"] = "true"
            date = dictionary["writtenDate"]
            date = stripOrdinals(date)
            try:
                stringDate = parseDate(date, "%d %B %Y")
                if isDateTooFarInFuture(stringDate):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    if validateDate(stringDate):
                        setDate(stringDate, KEData)
                    else:
                        KEData["invalidDate"] = "true"
            except ValueError:
                KEData["invalidDate"] = "true"
        elif string_id == "writtenDateShorterMonth":
            KEData["writtenDateShorterMonth"] = "true"
            date = dictionary["writtenDateShorterMonth"]
            date = stripOrdinals(date)
            try:
                stringDate = parseDate(date, "%d %b %Y")
                if isDateTooFarInFuture(stringDate):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    if validateDate(stringDate):
                        setDate(stringDate, KEData)
                    else:
                        KEData["invalidDate"] = "true"
            except ValueError:
                KEData["invalidDate"] = "true"
        elif string_id == "writtenDateOf":
            KEData["writtenDateOf"] = "true"
            date = str(dictionary["writtenDateOf"])
            date = date.replace("of ", "")
            date = stripOrdinals(date)
            try:
                stringDate = parseDate(date, "%d %B %Y")
                if isDateTooFarInFuture(stringDate):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    if validateDate(stringDate):
                        setDate(stringDate, KEData)
                    else:
                        KEData["invalidDate"] = "true"
            except ValueError:
                KEData["invalidDate"] = "true"
        elif string_id == "writtenDateShorterMonthOf":
            KEData["writtenDateShorterMonthOf"] = "true"
            date = str(dictionary["writtenDateShorterMonthOf"])
            date = date.replace("of ", "")
            date = stripOrdinals(date)
            try:
                stringDate = parseDate(date, "%d %b %Y")
                if isDateTooFarInFuture(stringDate):
                    KEData["dateTooFarInFuture"] = "true"
                else:
                    if validateDate(stringDate):
                        setDate(stringDate, KEData)
                    else:
                        KEData["invalidDate"] = "true"
            except ValueError:
                KEData["invalidDate"] = "true"
        elif string_id == "writtenTimeMorning":
            KEData["writtenTimeMorning"] = "true"
            time = str(dictionary["writtenTimeMorning"])
            number = int(re.search(r"\d+", time).group())
            if number < 1 or number > 12:
                KEData["invalidTime"] = "true"
            else:
                if number == 12:
                    number = 0
                number = str(number).zfill(2)
                number = number + "00"
                if validateTime(number):
                    setTime(number)
                else:
                    KEData["invalidTime"] = "true"
        elif string_id == "writtenTimeEvening":
            KEData["writtenTimeEvening"] = "true"
            time = str(dictionary["writtenTimeEvening"])
            number = int(re.search(r"\d+", time).group())
            if number < 1 or number > 12:
                KEData["invalidTime"] = "true"
            else:
                if number != 12:
                    number = number + 12
                number = str(number) + "00"
                if validateTime(number):
                   setTime(number)
                else:
                    KEData["invalidTime"] = "true"
        elif string_id == "writtenTimeWithMinutesMorning":
            KEData["writtenTimeWithMinutesMorning"] = "true"
            time = str(dictionary["writtenTimeWithMinutesMorning"])
            time = time.replace("am", "")
            index = time.index(":")
            hour = time[0:index]
            minutes = time[index + 1:]
            if int(hour) < 1 or int(hour) > 12:
                KEData["invalidTime"] = "true"
            else:
                if hour == "12":
                    hour = "00"
                time = hour.zfill(2) + minutes.zfill(2)
                if validateTime(time):
                    setTime(time)
                else:
                    KEData["invalidTime"] = "true"
        elif string_id == "writtenTimeWithMinutesEvening":
            KEData["writtenTimeWithMinutesEvening"] = "true"
            time = str(dictionary["writtenTimeWithMinutesEvening"])
            time = time.replace("pm", "")
            index = time.index(":")
            hour = time[0:index]
            minutes = time[index + 1:]
            if (int(hour)) < 1 or int(hour) > 12:
                KEData["invalidTime"] = "true"
            else:
                if int(hour) != 12:
                    hour = int(hour) + 12
                time = str(hour).zfill(2) + minutes.zfill(2)
                if validateTime(time):
                    setTime(time)
                else:
                    KEData["invalidTime"] = "true"
        elif string_id == "time":
            if "p.m." in text:
                KEData["time"] = "true"
                time = str(dictionary["time"])
                index = time.index(":")
                hour = time[0:index]
                minutes = time[index + 1:]
                if (int(hour)) < 1 or int(hour) > 12:
                    KEData["invalidTime"] = "true"
                else:
                    if int(hour) != 12:
                        hour = int(hour) + 12
                    time = str(hour).zfill(2) + minutes.zfill(2)
                    if validateTime(time):
                        setTime(time)
                    else:
                        KEData["invalidTime"] = "true"
            elif "a.m." in text:
                KEData["time"] = "true"
                time = str(dictionary["time"])
                index = time.index(":")
                hour = time[0:index]
                minutes = time[index + 1:]
                if (int(hour)) < 1 or int(hour) > 12:
                    KEData["invalidTime"] = "true"
                else:
                    if hour == "12":
                        hour = "00"
                    time = str(hour).zfill(2) + minutes.zfill(2)
                    if validateTime(time):
                        setTime(time)
                    else:
                        KEData["invalidTime"] = "true"
            else:
                KEData["time"] = "true"
                time = str(dictionary["time"])
                index = time.index(":")
                hour = time[0:index]
                minutes = time[index + 1:]
                time = hour.zfill(2) + minutes.zfill(2)
                if validateTime(time):
                    setTime(time)
                else:
                    KEData["invalidTime"] = "true"
        elif string_id == "dottedTimeWithSpaceMorning":
            KEData["dottedTimeWithSpaceMorning"] = "true"
            time = str(dictionary["dottedTimeWithSpaceMorning"])
            time = time.replace(" a.m.", "")
            time = time.zfill(2)
            if time == "12":
                time = "00"
            timeString = time + "00"
            if validateTime(timeString):
                setTime(timeString)
            else:
                KEData["invalidTime"] = "true"
        elif string_id == "dottedTimeWithSpaceEvening":
            KEData["dottedTimeWithSpaceEvening"] = "true"
            time = str(dictionary["dottedTimeWithSpaceEvening"])
            print(time, "time")
            time = time.replace(" p.m.", "")
            time = time.zfill(2)
            if time != "12":
                time = int(time)
                time += 12
            timeString = str(time) + "00"
            if validateTime(timeString):
                setTime(timeString)
            else:
                KEData["invalidTime"] = "true"
        elif string_id == "wordTimeMorning":
            KEData["wordTimeMorning"] = "true"
            setTime("0900")
        elif string_id == "wordTimeEvening":
            KEData["wordTimeEvening"] = "true"
            setTime("1800")
        elif string_id == "wordTimeAfternoon":
            KEData["wordTimeAfternoon"] = "true"
            setTime("1300")
        elif string_id == "wordTimeNoon":
            KEData["wordTimeNoon"] = "true"
            setTime("1200")
        elif string_id == "wordTimeMidnight":
            KEData["wordTimeMidnight"] = "true"
            setTime("0000")
        elif string_id == "noTimeGiven":
            KEData["noTimeGiven"] = "true"
            setTime("2000")
        elif string_id == "arriveBefore":
            KEData["arriveBefore"] = "true"
        elif string_id == "departBefore":
            KEData["departBefore"] = "true"

    if (len(regex_matches) == 0):
        KEData["noMatches"] = "true"

    if isBooking == "true":
        parseLocations(KEData, text)
    elif isBooking == "false":
        if len(delayStationUserIsAt) == 0:
            parseDelayLocations(KEData, text)
        else:
            parseDelayTime(KEData, text)



    if (len(websiteReturnTime) > 0) and (isReturn == "true") and len(websiteReturnType) == 0:
        parseReturnType(KEData)
    elif (len(websiteTime) > 0) and len(websiteType) == 0:
        parseSingleType(KEData)


    KEData["userText"] = text       # the entire user message is also added to the KE's dictionary

    printStringsDebug()

    KnowledgeEngine.finalResponseText(KEData)   # calling the knowledge engine, the final step in the process

def parseDelayTime(KEData, text):
    #getting an integer when the user is prompted to enter a delay time in minutes
    global delayTimeFromUser, delayDepartureTime
    if "noMatches" in KEData and len(delayDepartureTime) > 0:
        try:
            delayTimeFromUser = re.search("\d+", text).group()
            KEData["readyToCalculate"] = "true"
        except Exception:
            KEData["invalidDelayTime"] = "true"

def validateReturnDate(returnDate):
    #making sure the return date is a valid date, and after the outbound date
    #pass return date as string, in format DDMMYY
    global websiteDate
    outboundDay = websiteDate[0:2]
    outboundMonth = websiteDate[2:4]
    outboundYear = "20" + websiteDate[4:6]
    inboundDay = returnDate[0:2]
    inboundMonth = returnDate[2:4]
    inboundYear = "20" + returnDate[4:6]

    outboundDate = outboundDay + "/" + outboundMonth + "/" + outboundYear
    outboundDateTime = datetime.datetime.strptime(outboundDate, "%d/%m/%Y")
    inboundDate = inboundDay + "/" + inboundMonth + "/" + inboundYear
    inboundDateTime = datetime.datetime.strptime(inboundDate, "%d/%m/%Y")

    return outboundDateTime <= inboundDateTime

def parseDelayLocations(KEData, text):
    #each location in the delay prediction mode needs to be a specific station. This is validated instantly, and they are set here
    #First departure station is asked, then arrival station, then current station
    global delayDestinationStation, delayDepartureStation, delayStationUserIsAt, delayDepartureTime
    if len(delayStationUserIsAt) == 0 and len(delayDepartureTime) == 0:
        if len(delayDepartureStation) == 0 and "delay" not in KEData:
            station = getTicketData.searchForSingleStation(text)
            if not station:
                KEData["noStationFound"] = "true"
            else:
                delayDepartureStation = station
                KEData["delayDepartureFound"] = "true"

        elif len(delayDestinationStation) > 0 and "delay" not in KEData:
            station = getTicketData.searchForSingleStation(text)
            if station == False:
                KEData["noStationFound"] = "true"
            else:
                if station != delayDestinationStation:
                    delayStationUserIsAt = station
                    KEData["stationFound"] = "true"
                else:
                    KEData["duplicateStation"] = "true"

        elif len(delayDepartureStation) > 0 and "delay" not in KEData:
            station = getTicketData.searchForSingleStation(text)
            if not station:
                KEData["noStationFound"] = "true"
            else:
                if station != delayDepartureStation:
                    delayDestinationStation = station
                    KEData["delayDestinationFound"] = "true"
                else:
                    KEData["duplicateStation"] = "true"




def parseLocations(KEData, text):
    #makes sure the return and outbound locations for a ticket booking are not the same, and sets them
    global websiteDeparture, websiteDestination
    if len(isReturn) > 0:
        if (len(websiteDestination) == 0) and (len(websiteDeparture) == 0) and "booking" not in KEData:
            if "single" not in KEData and "return" not in KEData:
                websiteDeparture = text
        elif (len(websiteDeparture) > 0) and (len(websiteDestination) == 0) and "booking" not in KEData:
            if "single" not in KEData and "return" not in KEData:
                if websiteDeparture.lower() != text.lower():
                    websiteDestination = text
                else:
                    userInterface.send_response("Sorry, the destination and departure locations cannot be the same!")

def parseReturnType(KEData):
    #getting type of return inbound ticket - default is DEPART AFTER TIME, but can be ARRIVE BEFORE TIME or TAKE FIRST TRAIN
    global websiteReturnType
    if "departBefore" in KEData:
        websiteReturnType = "first"
    elif "arriveBefore" in KEData:
        websiteReturnType = "arr"

def parseSingleType(KEData):
    #like above function, but for type of outbound journey
    global websiteType
    if "departBefore" in KEData:
        websiteType = "first"
    elif "arriveBefore" in KEData:
        websiteType = "arr"

def printStringsDebug():
    print("WEBSITE_DEPARTURE", websiteDeparture)
    print("WEBSITE_DESTINATION", websiteDestination)
    print("IS_BOOKING", isBooking)
    print("IS_RETURN", isReturn)
    print("WEBSITE_DATE", websiteDate)
    print("WEBSITE_TIME", websiteTime)
    print("WEBSITE_TYPE", websiteType)
    print("WEBSITE_RETURN_DATE", websiteReturnDate)
    print("WEBSITE_RETURN_TIME", websiteReturnTime)
    print("WEBSITE_RETURN_TYPE", websiteReturnType)
    print("DELAY_DEPARTURE", delayDepartureStation)
    print("DELAY_DESTINATION", delayDestinationStation)
    print("DELAY_DEPARTURE_TIME", delayDepartureTime)
    print("DELAY_STATION", delayStationUserIsAt)
    print("DELAY_TIME_USER", delayTimeFromUser)
    print("GIVEN_TICKET", givenTicket)

def setDate(date, KEData):
    #sets the date either as an outbound or inbound journey
    # pass date as string, in format DDMMYY
    global websiteDate, websiteReturnDate
    if len(websiteDate) > 0 and isReturn == "true":
        if validateReturnDate(date):
            websiteReturnDate = date
        else:
            KEData["outgoingDateBeforeIncoming"] = "true"
    else:
        websiteDate = date


def setTime(time):
    #sets the time either as an outbound or inbound journey
    # pass time as string, in format HHMM
    global websiteTime, websiteReturnTime, delayDestinationStation, delayDepartureTime
    if isBooking == "true":
        if len(websiteTime) > 0 and isReturn == "true":
            websiteReturnTime = time
        else:
            websiteTime = time
    elif isBooking == "false":
        if len(delayDestinationStation) > 0:
           delayDepartureTime = time


def parseFromAndTo(text):
    #a single sentence saying "book a ticket FROM NORTHAMPTON TO LONDON", this function will parse
    #2 locations from X to Y and set those
    global websiteDeparture, websiteDestination
    text = text.lower()
    if re.search("(?<![\w\d])from(?![\w\d])", text):
        if re.search("(?<![\w\d])to(?![\w\d])", text):
            a, b = text.find(' from '), text.find(' to ')
            if b > a:
                departure = text[a + 6:b]
                destination = text[b + 4:]
                websiteDeparture = departure
                websiteDestination = destination


def parseDate(date, format):
    #a general function that generates a string date from a date and the format of that date
    now = datetime.datetime.now()
    if re.match("\d\d\d\d", date):
        formatted = datetime.datetime.strptime(date, format)
    else:
        date = date + " " + str(now.year)
        formatted = datetime.datetime.strptime(date, format)
    stringDate = datetimeToString(formatted)
    return stringDate


def validateTime(string):
    #makes sure the 24h string time (HHMM) is valid
    # pass time in format HHMM
    hours = int(string[0:2])
    minutes = int(string[2:4])
    try:
        formattedTime = datetime.time(hours, minutes, 00)
    except ValueError:
        return False
    return True


def validateDate(string):
    #makes sure the string date (DDMMYY) is valid, and not in the past
    # pass date in format DDMMYY
    today = datetime.datetime.now()
    inputtedDay = string[0:2]
    inputtedMonth = string[2:4]
    inputtedYear = "20" + string[4:6]
    fullInputtedDate = inputtedDay + "/" + inputtedMonth + "/" + inputtedYear
    try:
        fullInputtedDateTime = datetime.datetime.strptime(fullInputtedDate, "%d/%m/%Y")
    except ValueError:
        return False
    return fullInputtedDateTime.date() >= today.date()


def isDateTooFarInFuture(string):
    #national rail can only book dates no further than 82 days ahead
    # pass date in format DDMMYY
    maxDateForNationalRail = datetime.datetime.now() + datetime.timedelta(days=82)

    inputtedDay = string[0:2]
    inputtedMonth = string[2:4]
    inputtedYear = "20" + string[4:6]
    fullInputtedDate = inputtedDay + "/" + inputtedMonth + "/" + inputtedYear
    fullInputtedDateTime = datetime.datetime.strptime(fullInputtedDate, "%d/%m/%Y")
    return fullInputtedDateTime.date() > maxDateForNationalRail.date()


def stripOrdinals(date):
    #stripping ordinals from date, like 1*ST*, 2*ND*, etc
    date = str(date)
    date = date.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
    return date


def datetimeToString(date):
    #turns a datetime to a DDMMYY string
    string = str(date.day).zfill(2) + str(date.month).zfill(2) + str(date.year)[2:4]
    print(string, "string")
    return string


def resetStrings():
    #resets the internal variables to allow for a new conversation
    global websiteDeparture, websiteDestination, websiteDate, websiteTime, websiteType, websiteReturnDate, \
        websiteReturnTime, websiteReturnType, isBooking, isReturn, isDelay, delayDestinationStation, \
        delayDepartureStation, delayStationUserIsAt, delayTimeFromUser, delayDepartureTime
    isBooking = ""
    isReturn = ""
    isDelay = ""
    websiteDeparture = ""
    websiteDestination = ""
    websiteDate = ""
    websiteTime = ""
    websiteType = ""
    websiteReturnDate = ""
    websiteReturnTime = ""
    websiteReturnType = ""
    delayStationUserIsAt = ""
    delayTimeFromUser = ""
    delayDestinationStation = ""
    delayDepartureStation = ""
    delayDepartureTime = ""

def setWeekday(string, KEData):
    #if e.g. 'Monday' is specified as the date, this function gets the next 'Monday'
    global websiteDate, websiteReturnDate
    string = string.capitalize()
    weekdaysNumber = dict(zip(calendar.day_name, range(7)))
    today = datetime.datetime.now()
    todaysNumber = today.weekday()
    difference = (weekdaysNumber[string] - todaysNumber)
    if difference <= 0:
        difference += 7
    date = today + datetime.timedelta(days=difference)
    dateString = str(date.day).zfill(2) + str(date.month).zfill(2) + str(date.year)[2:4]
    if len(websiteDate) > 0 and isReturn == "true":
        if validateReturnDate(dateString):
            websiteReturnDate = dateString
        else:
            KEData["outgoingDateBeforeIncoming"] = "true"
    else:
        websiteDate = dateString

