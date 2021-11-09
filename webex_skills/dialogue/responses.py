# pylint:disable=no-name-in-module

from typing import Any, Dict
from typing import List as _List
from typing import Optional, Union

from pydantic import BaseModel

PayloadDict = Dict[str, Any]
Payload = Union[PayloadDict, _List[Any]]


class SkillDirective(BaseModel):
    name: str
    type: str
    payload: Optional[Payload]

    def dict(  # pylint:disable=useless-super-delegation, unused-argument
        self, *args, exclude_none=True, **kwargs
    ) -> PayloadDict:
        return super().dict(*args, **kwargs, exclude_none=True)


class ViewDirective(SkillDirective):
    type: str = 'view'


class ActionDirective(SkillDirective):
    type: str = 'action'


class Listen(ActionDirective):
    name: str = 'listen'


class Reply(ActionDirective):
    name: str = 'reply'

    def __init__(self, text: str):
        super().__init__(payload={'text': text})


class Speak(ActionDirective):
    name: str = 'speak'

    def __init__(self, text):
        super().__init__(payload={'text': text})


class Sleep(ActionDirective):
    name: str = 'sleep'
    payload: Dict[str, int]

    def __init__(self, delay: int = 0):
        super().__init__(payload={'delay': delay})


class DisplayWebView(ActionDirective):
    name: str = 'display-web-view'

    def __init__(self, url: str, title: Optional[str]):
        super().__init__(payload={'url': url, 'title': title})


class ClearWebView(ActionDirective):
    name: str = 'clear-web-view'


class UIHint(ViewDirective):
    name: str = 'ui-hint'

    def __init__(self, texts, prompt, display_immediately):
        super().__init__(payload={'texts': texts, 'prompt': prompt, 'display_immediately': display_immediately})


class AsrHint(ActionDirective):
    name: str = 'asr-hint'

    def __init__(self, texts):
        super().__init__(payload={'texts': texts})


class AssistantEvent(ActionDirective):
    name: str = 'assistant-event'
