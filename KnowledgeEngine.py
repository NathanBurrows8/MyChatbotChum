# the original plan was to use PyKE but this only works on Python 2.x and is deprecated - as this had the most documentation/was most popular
# now the plan is to use Experta which is a fork for PyKnow (also deprecated). Can be pip installed
# Experta is a Python library based on the CLIPS programming language.
import random
from experta import *
import json
import userInterface
import processUserInput

with open("./static/intents.json") as json_file:
    jsondata = json.load(json_file)


# conversation flow: ask for each of these, and when gathered, put into these strings. Rules can then be checked
# against the length of these strings to determine if gathered yet or not


class Bot(KnowledgeEngine):
    #put invalid error catching stuff at the top
    @Rule(salience=50)
    def initialGreeting(self):  # and no strings gathered
        if "hello" in self.dictionary:
            userInterface.send_response(random.choice(jsondata["hello"]))
            self.declare(Fact(said="hello"))

    @Rule(salience=49)
    def ask_if_return(self):  # and no strings gathered
        if "booking" in self.dictionary:
            processUserInput.isBooking = "true"
            userInterface.send_response(random.choice(jsondata["question_ticket_type"]))
            self.declare(Fact(said="ask_if_return"))

    @Rule(NOT(Fact(said="ask_if_return")),
          salience=48)
    def ask_departure_location(self):
        if processUserInput.isBooking == "true":
            if processUserInput.websiteDeparture == "":
                if "single" in self.dictionary:
                    processUserInput.isReturn = "false"
                    userInterface.send_response(random.choice(jsondata["question_departure_location"]))
                    self.declare(Fact(said="ask_departure_location"))
                elif "return" in self.dictionary:
                    processUserInput.isReturn = "true"
                    userInterface.send_response(random.choice(jsondata["question_departure_location"]))
                    self.declare(Fact(said="ask_departure_location"))

    @Rule(NOT(Fact(said="ask_departure_location")),
          salience=47)
    def ask_departure_date(self):
        if len(processUserInput.websiteDeparture) > 0:
            if len(processUserInput.websiteDate) == 0:
                userInterface.send_response(random.choice(jsondata["question_departure_date"]))
                self.declare(Fact(said="ask_departure_date"))

    @Rule(NOT(Fact(said="ask_departure_date")),
          salience=46)
    def ask_departure_time(self):
        if len(processUserInput.websiteDate) > 0:
            userInterface.send_response(random.choice(jsondata["question_departure_time"]))
            self.declare(Fact(said="ask_departure_time"))

    @Rule(NOT(Fact(said="ask_departure_time")),
          salience=45)
    def ask_arrival_location(self):
        if len(processUserInput.websiteTime) > 0:
            userInterface.send_response(random.choice(jsondata["question_arrival_location"]))
            self.declare(Fact(said="ask_arrival_location"))



    @Rule(NOT(Fact(said="hello")),
          (NOT(Fact(said="ask_if_return"))),
          (NOT(Fact(said="ask_departure_date"))),
          (NOT(Fact(said="ask_departure_location"))),
          (NOT(Fact(said="ask_departure_time"))),
          salience=2)
    def panic(self):
        userInterface.send_response(random.choice(jsondata["unable_to_parse"]))
        self.declare(Fact(said="panic"))

    @Rule(NOT(Fact(type="delay")),
          (NOT(Fact(said="hello"))),
          salience=1)
    def ask_type(self):
        if processUserInput.isBooking == "":
            userInterface.send_response(random.choice(jsondata["question_type_of_booking"]))
            self.declare(Fact(said="ask_type"))


def finalResponseText(nlp):
    bot = Bot()
    bot.dictionary = nlp
    print(nlp)
    bot.reset()
    watch('RULES')
    bot.run()

# this is an example from the experta website, read the documentation https://experta.readthedocs.io/en/latest/
