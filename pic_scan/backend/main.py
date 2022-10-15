from eventlet import wsgi
import eventlet
import socketio
import sys
from engineio.async_drivers import gevent

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.on('message')
def mess(event, data):
    print("Recieved: " + data)
    sio.emit("message", "Hello")


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    print("Backend On")
    wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)
