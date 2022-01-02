import re
import string
import nltk

frequency = {}

def getUserInput(text):
    text = text.lower()
    text = text.translate(str.maketrans('','', string.punctuation))
    print(text)


#bag of words? stemming?
