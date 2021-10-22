from typing import Awaitable, Callable, Dict, Union

from webex_assistant_sdk.dialogue.rules import MMDialogueStateRule, SimpleDialogueStateRule
from webex_assistant_sdk.models.mindmeld import DialogueState, ProcessedQuery

DialogueQuery = Union[ProcessedQuery, str]
SimpleHandler = Callable[[DialogueState], Awaitable[DialogueState]]
QueryHandler = Callable[[DialogueState, DialogueQuery], Awaitable[DialogueState]]

DialogueHandler = Union[SimpleHandler, QueryHandler]
DialogueRule = Union[SimpleDialogueStateRule, MMDialogueStateRule]

RuleMap = Dict[DialogueRule, DialogueHandler]
