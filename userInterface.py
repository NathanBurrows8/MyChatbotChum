from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from processUserInput import getUserInput
app = Flask(__name__)
app.debug = True


@app.route("/")
def get_data():
    return render_template('index.html')


socketio = SocketIO(app, cors_allowed_origins='*')

#using websockets to send data between javascript and python
@socketio.on("message_from_javascript")
def handle_message(data):
    getUserInput(data)

def send_response(text):
    socketio.emit("message_from_python", text)

if __name__ == "__main__":
    socketio.run(app)

