import re
from typing import Awaitable, Callable, Optional, Union

from webex_assistant_skills_sdk.api.shared.services import DialogueManager
from webex_assistant_skills_sdk.api.simple.models import SimpleDialogueRule
from webex_assistant_skills_sdk.shared.models import SkillRequest, SkillResponse


SimpleDialogueHandler = Union[
    Callable[[SkillRequest], Awaitable[SkillResponse]],
    Callable[[SkillRequest, str], Awaitable[SkillResponse]]
]

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

        def decorator(handler: SimpleDialogueHandler) -> SimpleDialogueHandler:
            if default:
                self.default_handler = handler
                return handler

            rule_name = name or handler.__name__.lower()
            if targeted_only:
                skill_rule = SimpleDialogueRule(
                    regex=None,
                    dialogue_state=rule_name,
                )
                self.rules[skill_rule] = handler
            else:
                skill_rule = SimpleDialogueRule(
                    regex=re.compile(pattern),
                    dialogue_state=rule_name,
                )
                self.rules[skill_rule] = handler

            return handler

        return decorator
