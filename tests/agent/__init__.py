# -*- coding: utf-8 -*-
"""This module contains the AgentApplication demo application"""

import os

from webex_assistant_sdk import AgentApplication
from webex_assistant_sdk.crypto import load_private_key_from_directory

secret = 'some secret'
key = load_private_key_from_directory(os.path.realpath(os.path.dirname(__file__)), password=None)
app = AgentApplication(__name__, secret=secret, private_key=key)

__all__ = ['app']


@app.handle(intent='greet')
def welcome(request, responder):
    del request
    responder.reply('Hello. I am agent who can help you.')
    responder.listen()


@app.handle(intent='exit')
def say_goodbye(request, responder):
    del request
    responder.reply(['Bye', 'Goodbye', 'Have a nice day.'])


@app.handle(intent='help')
def provide_help(request, responder):
    del request
    prompts = ["I can help you with your personal tasks.'"]
    responder.reply(prompts)
    responder.listen()
