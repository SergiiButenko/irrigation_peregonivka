from flask import Flask
from flask_socketio import SocketIO, emit
import logging
import eventlet
eventlet.monkey_patch()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(
        app,
        async_mode="eventlet",
        logger=True, engineio_logger=True,
        message_queue='redis://'
    )


@socketio.on('connect')
def test_connect():
    emit('connect', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@app.route("/notify", methods=["POST"])
def notify():
    emit('component_update', {'test': 'test'})
    return 'ok'