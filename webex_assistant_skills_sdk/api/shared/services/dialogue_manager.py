import inspect
from typing import Any, Awaitable, Callable, Dict, Generic, Optional, TypeVar

from webex_assistant_skills_sdk.api.shared.models import DialogueRule
from webex_assistant_skills_sdk.shared.models import DialogueTurn


T = TypeVar('T')

DialogueHandler = Callable[..., Awaitable[DialogueTurn]]
RuleMap = Dict[DialogueRule[T], DialogueHandler]

class DialogueManager(Generic[T]):
    default_handler: Optional[DialogueHandler] = None
    rules: RuleMap[T] = {}

    def __init__(
        self,
        rules: Optional[RuleMap[T]] = None,
        default_handler: Optional[DialogueHandler] = None
    ) -> None:
        if rules is not None:
            self.rules = rules

        if default_handler is not None:
            self.default_handler = default_handler

    def get_handler(
        self,
        query: T,
        target_state: Optional[str] = None,
        default_handler: Optional[Any] = None,
    ) -> Optional[DialogueHandler]:
        for rule, handler in self.rules.items():
            if target_state is not None and rule.dialogue_state == target_state:
                return handler

            if target_state is None and rule.match(query):
                return handler

        return default_handler

    async def handle(
        self,
        query: T,
        turn: DialogueTurn,
    ) -> DialogueTurn:
        # Iterate over our rules, taking the first match
        handler = self.get_handler(
            query,
            turn.params.target_dialogue_state,
            self.default_handler,
        )

        if handler is None:
            # TODO: custom exception
            raise Exception('No handler found')

        # TODO: Use annotated types rather than length  # pylint:disable=fixme
        handler_args = inspect.signature(handler)
        if len(handler_args.parameters) == 2:
            next_turn = await handler(turn, query)
        else:
            next_turn = await handler(turn)

        next_turn.update_history(last_turn=turn)

        return next_turn
