#!/usr/bin/env python

# Test Google Assistant

from __future__ import print_function
from __future__ import division

import google.oauth2.credentials
import json
import math
import os.path

from assistant_thread import AssistantThread
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from gevent import monkey
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from threading import Thread

# Create web server to display info
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
socketio = SocketIO(app)
assistant_thread = None

# This is so the background thread runs correctly with the socketio async model.
monkey.patch_all()

# Flask routes
@app.route("/")
def index():
    return app.send_static_file('index.html' )

@app.route("/js/<path:path>")
def serve_js(path):
    return send_from_directory('static/js', path)

# SocketIO events
@socketio.on('connect')
def api_connect():
    global assistant_thread

    if assistant_thread.isStarted():
        emit('assistant_ready')

    print('Client connected')

@socketio.on('assistant_trigger')
def api_trigger():

    print ("Assistant triggered, starting conversation")
    assistant_thread.assistant().start_conversation()

@socketio.on('disconnect')
def api_disconnect():
    print('Client disconnected')

# Handles Google assistant events
def process_event (event):
    print(event)
    
    # This is where we emit a socket.io event to the client side
    socketio.emit('assistant_event', {
        'type': event.type.name,
        'args': event.args });

    # Let client know assistant is ready
    if event.type == EventType.ON_START_FINISHED:
        socketio.emit('assistant_ready')
        print ("Assistant started")


if __name__ == '__main__':
    
    # Start assistant thread 
    assistant_thread = AssistantThread()
    assistant_thread.setEventCallback(process_event)
    assistant_thread.setDaemon(True)
    assistant_thread.start()
    print("Starting Assistant...")

    # Start web server and Socket.io
    socketio.run(app, host="0.0.0.0", port=5000)

    print ("Shutting down")
