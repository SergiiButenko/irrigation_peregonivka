from flask import Flask
from flask_socketio import SocketIO, emit
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(
        app,
        async_mode="eventlet",
        logger=True, engineio_logger=True
    )
# logging.getLogger("socketio").setLevel(logging.ERROR)
# logging.getLogger("engineio").setLevel(logging.ERROR)


@socketio.on('connect')
def test_connect():
    emit('connect', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on("my event")
def handle_my_custom_event(json):
    print("received json: " + str(json))


@app.route("/notify", methods=["POST"])
def notify():
    pass