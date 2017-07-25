#!/usr/bin/env python

# Test Google Assistant

from __future__ import print_function
from __future__ import division

import google.oauth2.credentials
import json
import math
import os.path

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

    # Start assistant thread if it isn't already. This is stupid but the only way to 
    # emit messages from another thread
    if assistant_thread is None:
        assistant_thread = socketio.start_background_task(target=start_assistant)
        print("Started")

    print('Client connected')

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

    if event.type == EventType.ON_START_FINISHED:
        print ("Assistant started")

# Starts Google assistant on current thread with the passed in callback function
def start_assistant(callback=process_event, credentials_path=None):
    if not credentials_path:
        credentials_path = default=os.path.join(
            os.path.expanduser('~/.config'),
            'google-oauthlib-tool',
            'credentials.json')

    with open(credentials_path, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))

    with Assistant(credentials) as assistant:
        for event in assistant.start():
            callback(event)


if __name__ == '__main__':
    
    # Start assistant thread
    # assistant = Thread(target = start_assistant, args = (process_event, ))
    # assistant.setDaemon(True)
    # assistant.start()

    # Start web server and Socket.io
    socketio.run(app, host="0.0.0.0", port=5000)

    print ("Shutting down")
