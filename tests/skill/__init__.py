# -*- coding: utf-8 -*-
"""This module contains the SkillApplication demo application"""

import os

from webex_assistant_sdk import SkillApplication
from webex_assistant_sdk.crypto import load_private_key_from_file

secret = 'some secret'
key = load_private_key_from_file(
    os.path.join(os.path.realpath(os.path.dirname(__file__)), 'id_rsa'), password=None
)
app = SkillApplication(__name__, secret=secret, private_key=key)

__all__ = ['app']


@app.introduce
@app.handle(intent='greet')
def welcome(request, responder):
    del request
    responder.reply('Hello. I am a third party skill. What would you like to do?')
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
