import datetime
import spacy
import KnowledgeEngine
from spacy.matcher import Matcher
import re
import userInterface

helloRegex = [
    {"LOWER": {"REGEX": "hi|hey|yo|hello"}}
]
goodbyeRegex = [
    {"LOWER": {"REGEX": "goodbye|bye|cya|quit|exit"}}
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

# currently 23rd jan works but not 23 jan - i think this is fine?
# 0am and 0pm are not split by spacy like 1am, etc, so we cannot get specific invalidDate error message
# currently 1:35 defaults to 1:35am


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

nlp = spacy.load("en_core_web_sm")

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


def getUserInput(text):
    global websiteDeparture, websiteDestination, isReturn, websiteType, websiteDate, websiteTime, isBooking
    dictionary = {}
    now = datetime.datetime.now()

    nlptext = nlp(text)
    for token in nlptext:
        print(token.text, token.pos_, token.dep_)

    regex_matches = matcher(nlptext)
    for match_id, start, end in regex_matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        matchedtext = nlptext[start:end]  # The matched text
        dictionary[string_id] = matchedtext

    KEData = {}
    for string_id in dictionary:
        #08-01-22 : this elif statement is 319 lines long
        if string_id == "hello":
            KEData["hello"] = "true"
        elif string_id == "booking":
            KEData["booking"] = "true"
            isBooking = "true"
            text = text.lower()
            if re.search("(?<![\w\d])from(?![\w\d])", text):
                if re.search("(?<![\w\d])to(?![\w\d])", text):
                    a, b = text.find(' from '), text.find(' to ')
                    if b > a:
                        departure = text[a + 6:b]
                        destination = text[b + 4:]
                        websiteDeparture = departure
                        websiteDestination = destination
            if "single" in text:
                KEData["single"] = "true"
                isReturn = "false"
            elif "return" in text:
                KEData["return"] = "true"
                isReturn = "true"
        elif string_id == "delay":
            KEData["delay"] = "true"
        elif string_id == "single":
            KEData["single"] = "true"
            isReturn = "false"
        elif string_id == "return":
            KEData["return"] = "true"
            isReturn = "true"
        elif string_id == "goodbye":
            KEData["goodbye"] = "true"
        elif string_id == "today":
            KEData["today"] = "true"
            date = str(now.day).zfill(2) + str(now.month).zfill(2) + str(now.year)[2:4]
            if validateDate(date):
                if isReturn == "false":
                    if isDateTooFarInFuture(date):
                        KEData["dateTooFarInFuture"] = "true"
                    else:
                        websiteDate = date
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "tomorrow":
            KEData["tomorrow"] = "true"
            tomorrow = now + datetime.timedelta(days=1)
            date = str(tomorrow.day).zfill(2) + str(tomorrow.month).zfill(2) + str(tomorrow.year)[2:4]
            if validateDate(date):
                if isReturn == "false":
                    if isDateTooFarInFuture(date):
                        KEData["dateTooFarInFuture"] = "true"
                    else:
                        websiteDate = date
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "day":
            KEData["day"] = "true"
        elif string_id == "slashDate":
            KEData["slashDate"] = "true"
            date = str(dictionary["slashDate"])
            date = date.replace("/", "")
            date = date[0:4] + date[6:8]
            if validateDate(date):
                if isReturn == "false":  # need to add return functionality to these
                    if isDateTooFarInFuture(date):
                        KEData["dateTooFarInFuture"] = "true"
                    else:
                        websiteDate = date
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "slashDateNoYear":
            KEData["slashDateNoYear"] = "true"
            date = str(dictionary["slashDateNoYear"])
            date = date.replace("/", "")
            date = date + str(now.year)[2:4]
            if validateDate(date):
                if isReturn == "false":
                    if isDateTooFarInFuture(date):
                        KEData["dateTooFarInFuture"] = "true"
                    else:
                        websiteDate = date
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "slashDateShorterYear":
            KEData["slashDateShorterYear"] = "true"
            date = str(dictionary["slashDateShorterYear"])
            date = date.replace("/", "")
            if validateDate(date):
                if isReturn == "false":
                    if isDateTooFarInFuture(date):
                        KEData["dateTooFarInFuture"] = "true"
                    else:
                        websiteDate = date
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
                    websiteDate = stringDate
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
                    websiteDate = stringDate
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
                    websiteDate = stringDate
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
                    websiteDate = stringDate
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
                    websiteTime = number
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
                    websiteTime = number
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
                    websiteTime = time
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
                    websiteTime = time
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
                        websiteTime = time
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
                        websiteTime = time
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
                    websiteTime = time
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
                websiteTime = timeString
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
                websiteTime = timeString
            else:
                KEData["invalidTime"] = "true"
        elif string_id == "wordTimeMorning":
            KEData["wordTimeMorning"] = "true"
            websiteTime = "0900"
        elif string_id == "wordTimeEvening":
            KEData["wordTimeEvening"] = "true"
            websiteTime = "1800"
        elif string_id == "wordTimeAfternoon":
            KEData["wordTimeAfternoon"] = "true"
            websiteTime = "1300"
        elif string_id == "wordTimeNoon":
            KEData["wordTimeNoon"] = "true"
            websiteTime = "1200"
        elif string_id == "wordTimeMidnight":
            KEData["wordTimeMidnight"] = "true"
            websiteTime = "0000"
        elif string_id == "noTimeGiven":
            KEData["noTimeGiven"] = "true"
            websiteTime = "1000"
        elif string_id == "arriveBefore":
            KEData["arriveBefore"] = "true"
        elif string_id == "departBefore":
            KEData["departBefore"] = "true"

    if (len(regex_matches) == 0):
        KEData["noMatches"] = "true"
    if len(isReturn) > 0:
        if (len(websiteDestination) == 0) and (len(websiteDeparture) == 0) and "booking" not in KEData:
            if "single" not in KEData and "return" not in KEData:
                websiteDeparture = text
        elif (len(websiteDeparture) > 0) and (len(websiteDestination) == 0) and "booking" not in KEData:
            if "single" not in KEData and "return" not in KEData:
                if websiteDeparture != text:
                    websiteDestination = text
                else:
                    userInterface.send_response("Sorry, the destination and departure locations cannot be the same!")

    if (len(websiteDestination) > 0) & (isReturn == "false"):
        # parse time
        if "departBefore" in KEData:
            websiteType = "first"
        elif "arriveBefore" in KEData:
            websiteType = "arr"
        else:
            websiteType = "dep"

    KEData["userText"] = text

    print("WEBSITE_DEPARTURE", websiteDeparture)
    print("WEBSITE_DESTINATION", websiteDestination)
    print("IS_BOOKING", isBooking)
    print("IS_RETURN", isReturn)
    print("WEBSITE_DATE", websiteDate)
    print("WEBSITE_TIME", websiteTime)
    print("WEBSITE_TYPE", websiteType)


    KnowledgeEngine.finalResponseText(KEData)

def parseDate(date, format):
    now = datetime.datetime.now()
    if re.match("\d\d\d\d", date):
        formatted = datetime.datetime.strptime(date, format)
    else:
        date = date + " " + str(now.year)
        formatted = datetime.datetime.strptime(date, format)
    stringDate = datetimeToString(formatted)
    return stringDate


def validateTime(string):
    # pass time in format HHMM
    hours = int(string[0:2])
    minutes = int(string[2:4])
    try:
        formattedTime = datetime.time(hours, minutes, 00)
    except ValueError:
        return False
    return True


def validateDate(string):
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
    return fullInputtedDateTime.date() > today.date()


def isDateTooFarInFuture(string):
    # pass date in format DDMMYY
    maxDateForNationalRail = datetime.datetime(2022, 3, 30)
    inputtedDay = string[0:2]
    inputtedMonth = string[2:4]
    inputtedYear = "20" + string[4:6]
    fullInputtedDate = inputtedDay + "/" + inputtedMonth + "/" + inputtedYear
    fullInputtedDateTime = datetime.datetime.strptime(fullInputtedDate, "%d/%m/%Y")
    return fullInputtedDateTime.date() > maxDateForNationalRail.date()


def stripOrdinals(date):
    date = str(date)
    date = date.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
    return date


def datetimeToString(date):
    string = str(date.day).zfill(2) + str(date.month).zfill(2) + str(date.year)[2:4]
    print(string, "string")
    return string


def resetStrings():
    global websiteDeparture, websiteDestination, websiteDate, websiteTime, websiteType, websiteReturnDate, \
        websiteReturnTime, websiteReturnType, isBooking, isReturn, isDelay, givenTicket
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
    givenTicket = ""

# verify named entity as location/dummy ticket purchase before moving on to the next step? so user can instantly
# try another location?

