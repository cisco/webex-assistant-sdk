from typing import Awaitable, Callable

from webex_assistant_sdk.models.mindmeld import DialogueState

DialogueHandler = Callable[[DialogueState], Awaitable[DialogueState]]
