# the original plan was to use PyKE but this only works on Python 2.x and is deprecated - as this had the most documentation/was most popular
# now the plan is to use Experta which is a fork for PyKnow (also deprecated). Can be pip installed
# Experta is a Python library based on the CLIPS programming language.
import random
from experta import *
import json
import getTicketData
import userInterface
import processUserInput

with open("./static/intents.json") as json_file:
    jsondata = json.load(json_file)

class Bot(KnowledgeEngine):
    #put invalid error catching stuff at the top

    @Rule(salience=53)
    def invalid_time(self):
        if "invalidTime" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["validation_invalid_time"]))
            self.declare(Fact(said="invalid_time"))
            self.declare(Fact(messageSend="true"))

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
          salience=2)
    def panic(self):
        if len(processUserInput.givenTicket) == 0:
            userInterface.send_response(random.choice(jsondata["unable_to_parse"]))
            self.declare(Fact(said="panic"))
            self.declare(Fact(messageSent="true"))

def finalResponseText(nlp):
    bot = Bot()
    bot.dictionary = nlp
    print(nlp)
    bot.reset()
    watch('RULES')
    bot.run()


def getIntroText():
    return random.choice(jsondata["question_type_of_booking"])

# this is an example from the experta website, read the documentation https://experta.readthedocs.io/en/latest/
