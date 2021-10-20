# Home for the various response directives
from typing import Any, Dict
from typing import List as _List
from typing import Optional, Union

from pydantic import BaseModel

PayloadDict = Dict[str, Any]
Payload = Union[PayloadDict, _List[Any]]

# TODO: Look at possibility of validating types for payload arguments


class SkillDirective(BaseModel):
    name: str
    type: str
    payload: Optional[Payload]

    def dict(self, *args, exclude_none=True, **kwargs) -> PayloadDict:
        return super().dict(*args, **kwargs, exclude_none=True)


class ViewDirective(SkillDirective):
    type: str = 'view'


class ActionDirective(SkillDirective):
    type: str = 'action'


class List(ViewDirective):
    payload: str


class Listen(ActionDirective):
    name: str = 'listen'


class Reply(ActionDirective):
    name: str = 'reply'

    def __init__(self, text: str):
        super().__init__(payload={'text': text})


class Reset(ActionDirective):
    pass


class Speak(ActionDirective):
    name: str = 'speak'

    def __init__(self, text):
        super().__init__(payload={'text': text})


class Suggest(ViewDirective):
    name: str = 'suggest'


class Sleep(ActionDirective):
    name: str = 'sleep'
    payload: Dict[str, int]

    def __init__(self, delay: int = 0):
        super().__init__(payload={'delay': delay})


class DisplayWebView(ActionDirective):
    pass


class ClearWebView(ActionDirective):
    pass


class UIHint(ViewDirective):
    pass


class AsrHint(ActionDirective):
    pass


class LongReply(ViewDirective):
    pass


class Display(ViewDirective):
    pass


class AssistantEvent(ActionDirective):
    pass
