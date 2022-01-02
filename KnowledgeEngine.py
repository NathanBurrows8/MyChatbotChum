#the original plan was to use PyKE but this only works on Python 2.x and is deprecated - as this had the most documentation/was most popular
#now the plan is to use Experta which is a fork for PyKnow (also deprecated). Can be pip installed
#Experta is a Python library based on the CLIPS programming language.
import random
from random import choice
from experta import *
import json


with open("./static/intents.json") as json_file:
    jsondata = json.load(json_file)

class Light(Fact):
    """Info about the traffic light"""
    pass

class RobotCrossStreet(KnowledgeEngine):
    @Rule(Light(colour='green'))
    def green_light(self):
        print("Walk")

    @Rule(Light(colour='red'))
    def red_light(self):
        print("Dont walk")

    @Rule(AS.light << Light(colour=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is", light['colour'])

def addRobotMessage(event):
    finalResponse = random.choice(jsondata[event])
    return finalResponse

def finalResponseText():
    return addRobotMessage("hello")

if __name__ == '__main__':
    engine = RobotCrossStreet()
    engine.reset()
    engine.declare(Light(colour=choice(['green', 'yellow', 'blinking-yellow', 'red'])))
    engine.run()

#this is an example from the experta website, read the documentation https://experta.readthedocs.io/en/latest/
