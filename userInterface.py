import json
from flask import Flask, render_template, jsonify, request
from processUserInput import getUserInput
from KnowledgeEngine import finalResponseText
app = Flask(__name__)
app.debug = True

@app.route("/")
def get_data():
    return render_template('index.html')

#using POST to get the users text from the Javascript file and feed this into python, and vice versa
@app.route("/post", methods=['POST'])
def method():
    data = request.get_json()
    humanText = data['text']
    getUserInput(humanText)
    return finalResponseText()
