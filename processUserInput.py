import datetime
import spacy
import KnowledgeEngine
from spacy.matcher import Matcher

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
writtenDateNoYearRegex = [
    {"LOWER": {"REGEX": "(\d?\d)([stndh]{2})?"}},
    {"LOWER": {"REGEX": "(january|february|march|april|may|june|july|august|september|october|november|december)"}}
]
writtenDateRegex = [
    {"LOWER": {"REGEX": "(\d?\d)([stndh]{2})?"}},
    {"LOWER": {"REGEX": "(january|february|march|april|may|june|july|august|september|october|november|december)"}},
    {"TEXT": {"REGEX": "(\d\d\d\d)"}}
]
writtenDateShorterMonthRegex = [
    {"LOWER": {"REGEX": "(\d\d)[stndh]{2}(Jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s(\d\d\d\d)"}},
    {"LOWER": {"REGEX": "(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"}},
    {"TEXT": {"REGEX": "(\d\d\d\d)"}}
]
writtenDateShorterMonthNoYearRegex = [
    {"LOWER": {"REGEX": "(\d\d)[stndh]{2}"}},
    {"LOWER": {"REGEX": "(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"}}
]
# add dotted and hyphenated versions of date regex?
timeRegex = [
    {"TEXT": {"REGEX": "(\d\d)[:](\d\d)"}}
]
writtenTimeMorningRegex = [
    {"LOWER": {"REGEX": "(\d)?(\d)|(\d)?(\d)(([am]{2}))"}},
    {"LOWER": {"REGEX": "([am]{2})"}}
]
writtenTimeEveningRegex = [
    {"LOWER": {"REGEX": "(\d)?(\d)|(\d)?(\d)(([pm]{2}))"}},
    {"LOWER": {"REGEX": "([pm]{2})"}}
]
writtenTimeWithMinutesMorningRegex = [
    {"LOWER": {"REGEX": "(\d)?(\d)[:](\d\d)(([am]{2}))"}}
]
writtenTimeWithMinutesEveningRegex = [  # cant currently do 12:45 pm with a space
    {"LOWER": {"REGEX": "(\d)?(\d)[:](\d\d)(([pm]{2}))"}}
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
noTimeGivenRegex = [ #default to 'dep' 10:00?, 'dep' is normal default anyway
    {"LOWER": {"REGEX": "whenever"}}
]
departBeforeTimeRegex = [
    {"LOWER": {"REGEX": "depart|leave"}},
    {"LOWER": {"REGEX": "before"}}
]
arriveBeforeTimeRegex = [
    {"LOWER": {"REGEX": "arrive"}},
    {"LOWER": {"REGEX": "before"}}
]

isBooking = ""
isDelay = ""
websiteDeparture = ""
websiteDestination = ""
websiteDate = ""
websiteTime = ""
websiteType = ""

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
matcher.add("writtenDateNoYear", [writtenDateNoYearRegex])
matcher.add("writtenDateShorterMonth", [writtenDateShorterMonthRegex])
matcher.add("writtenDateShorterMonthNoYear", [writtenDateShorterMonthNoYearRegex])
matcher.add("time", [timeRegex])
matcher.add("writtenTimeMorning", [writtenTimeMorningRegex])
matcher.add("writtenTimeEvening", [writtenTimeEveningRegex])
matcher.add("writtenTimeWithMinutesMorning", [writtenTimeWithMinutesMorningRegex])
matcher.add("writtenTimeWithMinutesEvening", [writtenTimeWithMinutesEveningRegex])
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


def getUserInput(text):
    global websiteDeparture, websiteDestination, isReturn, websiteType, websiteDate
    dictionary = {}
    now = datetime.datetime.now()

    nlptext = nlp(text)
    for token in nlptext:
        print(token.text, token.pos_, token.dep_)

    regex_matches = matcher(nlptext)
    for match_id, start, end in regex_matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = nlptext[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text, "total matches")
        dictionary[string_id] = span

    KEData = {}
    for string_id in dictionary:
        if string_id == "hello":
            KEData["hello"] = "true"
        elif string_id == "booking":
            KEData["booking"] = "true"
        elif string_id == "delay":
            KEData["delay"] = "true"
        elif string_id == "single":
            KEData["single"] = "true"
        elif string_id == "return":
            KEData["return"] = "true"
        elif string_id == "goodbye":
            KEData["goodbye"] = "true"
        elif string_id == "today":
            KEData["today"] = "true"
        elif string_id == "tomorrow":
            KEData["tomorrow"] = "true"
        elif string_id == "day":
            KEData["day"] = "true"
        elif string_id == "slashDate":
            KEData["slashDate"] = "true"
            date = str(dictionary["slashDate"])
            date = date.replace("/", "")
            date = date[0:4] + date[6:8]
            if validateDate(date):
                if isReturn == "false": #need to add return functionality to these
                    websiteDate = date
                    print(websiteDate, "website")
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "slashDateNoYear":
            KEData["slashDateNoYear"] = "true"
            date = str(dictionary["slashDate"])
            date = date.replace("/", "")
            date = date + str(now.year)[2:4]
            if validateDate(date):
                if isReturn == "false":
                    websiteDate = date
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "slashDateShorterYear":
            KEData["slashDateShorterYear"] = "true"
            date = str(dictionary["slashDateShorterYear"])
            date = date.replace("/", "")
            if validateDate(date):
                if isReturn == "false":
                    websiteDate = date
            else:
                KEData["invalidDate"] = "true"
        elif string_id == "writtenDate":
            KEData["writtenDate"] = "true"
        elif string_id == "writtenDateNoYear":
            KEData["writtenDateNoYear"] = "true"
        elif string_id == "writtenDateShorterMonth":
            KEData["writtenDateShorterMonth"] = "true"
        elif string_id == "writtenDateShorterMonthNoYear":
            KEData["writtenDateShorterMonthNoYear"] = "true"
        elif string_id == "time":
            KEData["time"] = "true"
        elif string_id == "writtenTimeMorning":
            KEData["writtenTimeMorning"] = "true"
        elif string_id == "writtenTimeEvening":
            KEData["writtenTimeEvening"] = "true"
        elif string_id == "writtenTimeWithMinutesMorning":
            KEData["writtenTimeWithMinutesMorning"] = "true"
        elif string_id == "writtenTimeWithMinutesEvening":
            KEData["writtenTimeWithMinutesEvening"] = "true"
        elif string_id == "wordTimeMorning":
            KEData["wordTimeMorning"] = "true"
        elif string_id == "wordTimeEvening":
            KEData["wordTimeEvening"] = "true"
        elif string_id == "wordTimeAfternoon":
            KEData["wordTimeAfternoon"] = "true"
        elif string_id == "wordTimeNoon":
            KEData["wordTimeNoon"] = "true"
        elif string_id == "wordTimeMidnight":
            KEData["wordTimeMidnight"] = "true"
        elif string_id == "noTimeGiven":
            KEData["noTimeGiven"] = "true"
        elif string_id == "departBefore":
            KEData["departBefore"] = "true"
        elif string_id == "arriveBefore":
            KEData["arriveBefore"] = "true"
    if (len(regex_matches) == 0):
        KEData["noMatches"] = "true"
    if len(isReturn) > 0:
        if (len(websiteDestination) == 0) & (len(websiteDeparture) == 0):
            websiteDeparture = text
        elif (len(websiteDeparture) > 0) & (len(websiteDestination) == 0):
            if websiteDeparture != text:
                 websiteDestination = text
            else:
                userInterface.send_response("Sorry, the destination and departure locations cannot be the same! Please tell me a different destination:")


    if (len(websiteDestination) > 0) & (isReturn == "false"):
        #parse time
        if "departBefore" in KEData:
            websiteType = "first"
        elif "arriveBefore" in KEData:
            websiteType = "arr"
        else:
            websiteType = "dep"







    KEData["userText"] = text

    KnowledgeEngine.finalResponseText(KEData)


def validateDate(string):
    # pass date in format DDMMYY
    today = datetime.datetime.now()
    print(string, "string")
    inputtedDay = string[0:2]
    inputtedMonth = string[2:4]
    inputtedYear = "20" + string[4:6]
    fullInputtedDate = inputtedDay + "/" + inputtedMonth + "/" + inputtedYear
    try:
        fullInputtedDateTime = datetime.datetime.strptime(fullInputtedDate, "%d/%m/%Y")
    except ValueError:
        return False
    print(fullInputtedDateTime.date(), "1")
    print(today.date(), "2")
    return fullInputtedDateTime.date() > today.date()


# verify named entity as location/dummy ticket purchase before moving on to the next step? so user can instantly
# try another location?

# change so that opening text is it explaining its functions?
