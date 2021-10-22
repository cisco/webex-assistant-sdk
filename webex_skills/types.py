from typing import Awaitable, Callable, Dict, Union

from .dialogue.rules import MMDialogueStateRule, SimpleDialogueStateRule
from .models.mindmeld import DialogueState, ProcessedQuery

DialogueQuery = Union[ProcessedQuery, str]
SimpleHandler = Callable[[DialogueState], Awaitable[DialogueState]]
QueryHandler = Callable[[DialogueState, DialogueQuery], Awaitable[DialogueState]]

DialogueHandler = Union[SimpleHandler, QueryHandler]
DialogueRule = Union[SimpleDialogueStateRule, MMDialogueStateRule]

RuleMap = Dict[DialogueRule, DialogueHandler]
