# -*- coding: utf-8 -*-
"""This module contains the SkillApplication demo application"""

from webex_assistant_sdk import SkillApplication

secret = 'some secret'
app = SkillApplication(__name__, secret=secret)

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
    responder.sleep()


@app.handle(intent='help')
def provide_help(request, responder):
    del request
    prompts = ["I can help you with your personal tasks.'"]
    responder.reply(prompts)
    responder.listen()
