# -*- coding: utf-8 -*-
"""This module contains an empty application container.
It is defined here to avoid circular imports
"""
from pathlib import Path

from webex_assistant_sdk import SkillApplication
from webex_assistant_sdk.crypto import load_private_key_from_file

secret = '{{cookiecutter.app_secret}}'

key = load_private_key_from_file(str(Path(__file__).resolve().parent / 'id_rsa'))
app = SkillApplication(__name__, secret=secret, private_key=key)


@app.introduce()
@app.handle(intent='greet')
def greet(request, responder):
    del request
    responder.reply('Hi, I am {{cookiecutter.skill_name}}!')


@app.handle(intent='exit')
def exit_(request, responder):
    del request
    responder.reply('Bye!')


@app.middleware
def add_sleep(request, responder, handler):
    handler(request, responder)
    # ensure response ends with `listen` or `sleep`
    if responder.directives[-1]['name'] not in {'listen', 'sleep'}:
        responder.sleep()


__all__ = ['app']
