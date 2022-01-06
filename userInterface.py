from flask import Flask, render_template
from flask_socketio import SocketIO

import KnowledgeEngine
import processUserInput

app = Flask(__name__)
app.debug = True


@app.route("/")
def get_data():
    return render_template('index.html')


socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on("connect")
def intro():
    send_response(KnowledgeEngine.getIntroText())

# using websockets to send data between javascript and python
@socketio.on("message_from_javascript")
def handle_message(data):
    processUserInput.getUserInput(data)


@socketio.on("page_reload")
def reload(data):
    processUserInput.resetStrings()


def send_response(text):
    socketio.emit("message_from_python", text)


if __name__ == "__main__":
    socketio.run(app)
