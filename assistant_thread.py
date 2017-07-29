#!/usr/bin/env python

from threading import Thread

import google.oauth2.credentials
import json

from os import path
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

class AssistantThread(Thread):

    _assistant = None
    _eventCallback = None

    # Starts Google assistant on current thread with the passed in callback function
    def run(self):
        credentials_path = default=path.join(
            path.expanduser('~/.config'),
            'google-oauthlib-tool',
            'credentials.json')

        with open(credentials_path, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))

        with Assistant(credentials) as assistant:
            self._assistant = assistant
            for event in assistant.start():
                if self._eventCallback:
                    self._eventCallback(event)

    def setEventCallback(self, callback):
        self._eventCallback = callback

    def assistant(self):
        return self._assistant
