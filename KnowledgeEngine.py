# the original plan was to use PyKE but this only works on Python 2.x and is deprecated - as this had the most documentation/was most popular
# now the plan is to use Experta which is a fork for PyKnow (also deprecated). Can be pip installed
# Experta is a Python library based on the CLIPS programming language.
import random
from experta import *
import json
import userInterface

with open("./static/intents.json") as json_file:
    jsondata = json.load(json_file)


class Bot(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        userInterface.send_response(random.choice(jsondata["hello"]))
        yield Fact(action="unknown")

    @Rule(Fact(action="unknown"), salience=97)
    def initialGreeting(self):
        userInterface.send_response(random.choice(jsondata["hello"]))
        yield Fact(said="hello")

    @Rule(NOT(Fact(said="hello")),
          salience=1)
    def panic(self):
        userInterface.send_response(random.choice(jsondata["unable_to_parse"]))
        yield Fact(said="panic")


def finalResponseText(nlp):
    bot = Bot()
    bot.dictionary = nlp
    bot.reset()
    bot.run()

# this is an example from the experta website, read the documentation https://experta.readthedocs.io/en/latest/
