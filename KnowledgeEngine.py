#This file is the Knowledge Engine. A dictionary is passed to it from processUserInput, with the text and what
#labels that text has. Based on those labels, and the rules detailed below, this is the file that determines
#what robot response should be displayed.


# the original plan was to use PyKE but this only works on Python 2.x and is deprecated - as this had the most documentation/was most popular
# now the plan is to use Experta which is a fork for PyKnow (also deprecated). Can be pip installed
# Experta is a Python library based on the CLIPS programming language.
import random
from experta import *
import json
import getTicketData
import predictDelay
import userInterface
import processUserInput

with open("./static/intents.json") as json_file:    # this data is intents.json, the robots vocabulary
    jsondata = json.load(json_file)

class Bot(KnowledgeEngine):
# This is the rule based KE. The validation functions have the highest salience, which means they are prioritised
# and fired first. Each function gives a different robot response based on certain conditions.

    @Rule(salience=57)
    def unable_to_parse_time(self):
        if "invalidDelayTime" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["validation_unable_to_parse_time"]))
            self.declare(Fact(said="invalid_delay_time"))
            self.declare(Fact(messageSent="true"))

    @Rule(salience=56)
    def station_not_found_delay(self):
        if "noStationFound" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["validation_no_station_found"]))
            self.declare(Fact(said="no_station_found"))
            self.declare(Fact(messageSent="true"))


    @Rule(salience=55)
    def duplicate_station_delay(self):
        if "duplicateStation" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["validation_duplicate_station"]))
            self.declare(Fact(said="duplicate_station_delay"))
            self.declare(Fact(messageSent="true"))

    @Rule(salience=54)
    def outgoing_date_before_incoming(self):
        if "outgoingDateBeforeIncoming" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["outgoing_date_before_incoming"]))
            self.declare(Fact(said="outgoing_date_before_incoming"))
            self.declare(Fact(messageSent="true"))

    @Rule(salience=53)
    def invalid_time(self):
        if "invalidTime" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["validation_invalid_time"]))
            self.declare(Fact(said="invalid_time"))
            self.declare(Fact(messageSent="true"))

    @Rule(salience=52)
    def date_in_future(self):
        if "dateTooFarInFuture" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["validation_future_date"]))
            self.declare(Fact(said="date_in_future"))
            self.declare(Fact(messageSent="true"))

    @Rule(salience=51)
    def invalid_date(self):
        if "invalidDate" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["validation_invalid_date"]))
            self.declare(Fact(said="invalid_date"))
            self.declare(Fact(messageSent="true"))

    @Rule(salience=50)
    def initial_greeting(self):  # and no strings gathered
        if "hello" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["hello"]))
            self.declare(Fact(said="hello"))
            self.declare(Fact(messageSent="true"))

    @Rule(salience=49)
    def ask_if_return(self):  # and no strings gathered
        if "booking" in self.dictionary:
            if "single" not in self.dictionary and "return" not in self.dictionary:
                userInterface.send_response(random.choice(jsondata["question_ticket_type"]))
                self.declare(Fact(said="ask_if_return"))
                self.declare(Fact(messageSent="true"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=48)
    def ask_departure_location(self):
        if processUserInput.isBooking == "true":
            if processUserInput.websiteDeparture == "":
                userInterface.send_response(random.choice(jsondata["question_departure_location"]))
                self.declare(Fact(said="ask_departure_location"))
                self.declare(Fact(messageSent="true"))


    @Rule(NOT(Fact(messageSent="true")),
          salience=45)
    def ask_arrival_location(self):
        if len(processUserInput.websiteDeparture) > 0:
            if processUserInput.websiteDestination == "":
                userInterface.send_response(random.choice(jsondata["question_arrival_location"]))
                self.declare(Fact(said="ask_arrival_location"))
                self.declare(Fact(messageSent="true"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=47)
    def ask_departure_date(self):
        if len(processUserInput.websiteDestination) > 0:
            if len(processUserInput.websiteDate) == 0:
                userInterface.send_response(random.choice(jsondata["question_departure_date"]))
                self.declare(Fact(said="ask_departure_date"))
                self.declare(Fact(messageSent="true"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=46)
    def ask_departure_time(self):
        if len(processUserInput.websiteDate) > 0:
            if len(processUserInput.websiteTime) == 0:
                userInterface.send_response(random.choice(jsondata["question_departure_time"]))
                self.declare(Fact(said="ask_departure_time"))
                self.declare(Fact(messageSent="true"))


    @Rule(NOT(Fact(messageSent="true")),
          salience=45)
    def complete_single_ticket(self):
        if processUserInput.isBooking == "true":
            if processUserInput.isReturn == "false":
                if len(processUserInput.websiteDeparture) > 0 and len(processUserInput.websiteDestination) > 0 and \
                        len(processUserInput.websiteDate) > 0 and len(processUserInput.websiteTime) > 0:
                    if len(processUserInput.websiteType) == 0:
                        processUserInput.websiteType = "dep"
                    getTicketData.formWebsite(processUserInput.websiteDeparture, processUserInput.websiteDestination,
                                              processUserInput.websiteDate, processUserInput.websiteTime,
                                              processUserInput.websiteType)
                    self.declare(Fact(messageSent="true"))
                    processUserInput.resetStrings()

    @Rule(NOT(Fact(messageSent="true")),
          salience=44)
    def ask_arrival_date(self):
        if processUserInput.isReturn == "true":
            if len(processUserInput.websiteReturnDate) == 0:
                userInterface.send_response(random.choice(jsondata["question_return_date"]))
                self.declare(Fact(said="ask_arrival_date"))
                self.declare(Fact(messageSent="true"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=43)
    def ask_arrival_time(self):
        if len(processUserInput.websiteReturnDate) > 0:
            if len(processUserInput.websiteReturnTime) == 0:
                userInterface.send_response(random.choice(jsondata["question_return_time"]))
                self.declare(Fact(said="ask_arrival_time"))
                self.declare(Fact(messageSent="true"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=42)
    def complete_return_ticket(self):
        if processUserInput.isBooking == "true":
            if processUserInput.isReturn == "true":
                if len(processUserInput.websiteDeparture) > 0 and len(processUserInput.websiteDestination) > 0 and \
                        len(processUserInput.websiteDate) > 0 and len(processUserInput.websiteTime) > 0 and \
                        len(processUserInput.websiteReturnDate) > 0 and len(processUserInput.websiteReturnTime) > 0:
                    if len(processUserInput.websiteType) == 0:
                        processUserInput.websiteType = "dep"
                    if len(processUserInput.websiteReturnType) == 0:
                        processUserInput.websiteReturnType = "dep"
                    getTicketData.formWebsiteReturn(processUserInput.websiteDeparture,
                                                    processUserInput.websiteDestination, processUserInput.websiteDate,
                                                    processUserInput.websiteTime, processUserInput.websiteType,
                                                    processUserInput.websiteReturnDate,
                                                    processUserInput.websiteReturnTime,
                                                    processUserInput.websiteReturnType)
                    self.declare(Fact(messageSent="true"))
                    processUserInput.resetStrings()

    @Rule(NOT(Fact(messageSent="true")),
          salience=41)
    def ask_departure_station_delay(self):
        if "delay" in self.dictionary:
            if len(processUserInput.delayDestinationStation) == 0:
                userInterface.send_response(random.choice(jsondata["question_departure_station_delay"]))
                self.declare(Fact(messageSent="true"))
                self.declare(Fact(said="ask_departure_station_delay"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=40)
    def ask_destination_station_delay(self):
        if len(processUserInput.delayDepartureStation) > 0 and len(processUserInput.delayDestinationStation) == 0:
            userInterface.send_response(random.choice(jsondata["question_destination_station_delay"]))
            self.declare(Fact(messageSent="true"))
            self.declare(Fact(said="ask_destination_station_delay"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=39)
    def ask_current_station_delay(self):
        if len(processUserInput.delayDestinationStation) > 0 and len(processUserInput.delayStationUserIsAt) == 0:
            userInterface.send_response(random.choice(jsondata["question_current_station_delay"]))
            self.declare(Fact(messageSent="true"))
            self.declare(Fact(said="ask_current_station_delay"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=38)
    def ask_delay_time(self):
        if len(processUserInput.delayStationUserIsAt) > 0 and len(processUserInput.delayTimeFromUser) == 0:
            userInterface.send_response(random.choice(jsondata["question_delay_time"]))
            self.declare(Fact(messageSent="true"))
            self.declare(Fact(said="ask_delay_time"))

    @Rule(NOT(Fact(messageSent="true")),
          salience=37)
    def calculate_delay(self):
        if "readyToCalculate" in self.dictionary:
            predictDelay.predict(processUserInput.delayDepartureStation, processUserInput.delayDestinationStation,
                                    processUserInput.delayStationUserIsAt, int(processUserInput.delayTimeFromUser))
            self.declare(Fact(messageSent="true"))


    @Rule(NOT(Fact(messageSent="true")),
          salience=2)
    def panic(self):
        if len(processUserInput.givenTicket) == 0:
            userInterface.send_response(random.choice(jsondata["unable_to_parse"]))
            self.declare(Fact(said="panic"))
            self.declare(Fact(messageSent="true"))

def finalResponseText(nlp):
    #This is called from processUserInput. The dictionary is passed to the KE, and the KE is run. This is the last step
    #before the final response text is sent back to the javascript file to be displayed.
    bot = Bot()
    bot.dictionary = nlp
    print(nlp)
    bot.reset()
    bot.run()


def getIntroText():
    return random.choice(jsondata["question_type_of_booking"])
