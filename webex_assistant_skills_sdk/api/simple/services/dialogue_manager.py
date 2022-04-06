import re
from typing import Awaitable, Callable, Optional

from webex_assistant_skills_sdk.api.shared.dialogue import DialogueManager
from webex_assistant_skills_sdk.api.simple.models.dialogue_rule import SimpleDialogueRule
from webex_assistant_skills_sdk.shared.models import DialogueTurn


SimpleDialogueHandler = Callable[[str], Awaitable[DialogueTurn]]

class SimpleDialogueManager(DialogueManager[str]):
    def add_rule(
        self,
        *,
        name: Optional[str] = None,
        pattern: Optional[str] = None,
        default=False,
        targeted_only=False,
    ) -> Callable[[SimpleDialogueHandler], SimpleDialogueHandler]:
        """Wraps a function to behave as a dialogue handler"""

        # TODO: Take a closer look at the setup here, I'd like to have type hinting  # pylint:disable=fixme
        # catch if a function doesn't meet what's expected as a DialogueHandler
        # Just checking if handler is a coroutine is also an option
        def decorator(handler: SimpleDialogueHandler) -> SimpleDialogueHandler:
            if default:
                self.default_handler = handler
                return handler

            rule_name = name or handler.__name__.lower()
            if targeted_only:
                skill_rule = SimpleDialogueRule(None, rule_name)
                self.rules[skill_rule] = handler
            else:
                skill_rule = SimpleDialogueRule(re.compile(pattern), rule_name)
                self.rules[skill_rule] = handler

            return handler

        return decorator
