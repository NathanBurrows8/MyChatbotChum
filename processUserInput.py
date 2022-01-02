import spacy

frequency = {}



def getUserInput(text):
    dictionary = {}
    nlp = spacy.load("en_core_web_sm")
    nlptext = nlp(text)
    #text = text.lower()
    #text = text.translate(str.maketrans('','', string.punctuation))
    for token in nlptext:
        print(token.text, token.pos_, token.dep_)







    return dictionary

