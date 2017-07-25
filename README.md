# Google Assistant SDK Implementation

*TODO: Come up with a better name for this project*

This is a basic implementation of the [Google Assistant SDK](https://developers.google.com/assistant/sdk/) for a Raspberry PI 3. It starts a Flask web server and the Google Assistant SDK, which sends events to a front-end UI for display purposes.

## Setup Notes

The Google SDK Credentials must be created following [this guide](https://developers.google.com/assistant/sdk/develop/python/config-dev-project-and-account). This script looks for the credentials in `$HOME/.config/google-oauthlib-tool/credentials.json` but a custom location can be specified by passing a different location to `start_assistant`.

This script depends on following the Python virtualenv setup directions [here](https://developers.google.com/assistant/sdk/develop/python/run-sample) for Python 2. As well as the additional pip packages:
- gevent (Use this over eventlet, which I haven't gotten to work with multithreading)
- gevent-websocket
