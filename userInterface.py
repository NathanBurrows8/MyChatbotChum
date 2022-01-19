from flask import Flask, render_template
from flask_socketio import SocketIO

import KnowledgeEngine
import processUserInput

app = Flask(__name__)
app.debug = True


@app.route("/")
def get_data(): #display index.html as the webpage
    return render_template('index.html')


socketio = SocketIO(app, cors_allowed_origins='*')

# when the page first connects, display the robot's intro message
@socketio.on("connect")
def intro():
    send_response(KnowledgeEngine.getIntroText())

# using websockets to send the users message from javascript to python. This input is processed via processUserInput
@socketio.on("message_from_javascript")
def handle_message(data):
    processUserInput.labelUserInput(data)

# when the page reloads/refreshes, reset the variables thus resetting the conversation
@socketio.on("page_reload")
def reload(data):
    processUserInput.resetStrings()

# using websockets to send the final robot response from python to javascript
def send_response(text):
    socketio.emit("message_from_python", text)


if __name__ == "__main__":
    socketio.run(app)
