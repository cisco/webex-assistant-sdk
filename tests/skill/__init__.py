# -*- coding: utf-8 -*-
"""This module contains the SkillApplication demo application"""
from pathlib import Path

from webex_assistant_sdk.crypto import load_private_key_from_file
from webex_assistant_sdk.mindmeld.app import SkillApplication

secret = 'some secret'
key = load_private_key_from_file(str(Path(__file__).resolve().parent / 'id_rsa.pem'))
app = SkillApplication(__name__, secret=secret, private_key=key)

__all__ = ['app']


@app.introduce
@app.handle(pattern=)
def welcome(request, responder):
    del request
    responder.reply('Hello. I am a third party skill. What would you like to do?')
    responder.listen()


@app.handle(pattern=)
def say_goodbye(request, responder):
    del request
    responder.reply(['Bye', 'Goodbye', 'Have a nice day.'])
    responder.sleep()


@app.handle(pattern=)
def provide_help(request, responder):
    del request
    prompts = ["I can help you with your personal tasks.'"]
    responder.reply(prompts)
    responder.listen()
