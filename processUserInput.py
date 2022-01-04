import spacy
frequency = {}
import KnowledgeEngine

def getUserInput(text):
    dictionary = {}
    nlp = spacy.load("en_core_web_sm")
    nlptext = nlp(text)
    for token in nlptext:
        print(token.text, token.pos_, token.dep_)
    KnowledgeEngine.finalResponseText(nlptext)

