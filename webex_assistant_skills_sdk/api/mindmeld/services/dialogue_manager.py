from typing import Awaitable, Callable, Optional, Union

from webex_assistant_skills_sdk.api.mindmeld.models import MindmeldDialogueRule, ProcessedQuery
from webex_assistant_skills_sdk.api.shared.services import DialogueManager
from webex_assistant_skills_sdk.shared.models import SkillRequest, SkillResponse



MindmeldDialogueHandler = Union[
    Callable[[SkillRequest], Awaitable[SkillResponse]],
    Callable[[SkillRequest, ProcessedQuery], Awaitable[SkillResponse]],
]

class MindmeldDialogueManager(DialogueManager[ProcessedQuery]):
    def add_rule(
        self,
        *,
        name: Optional[str] = None,
        default=False,
        domain=None,
        intent=None,
        entities=None,
        targeted_only=False,
    ) -> Callable[[MindmeldDialogueHandler], MindmeldDialogueHandler]:
        """Wraps a function to behave as a dialogue handler"""

        def decorator(handler: MindmeldDialogueHandler) -> MindmeldDialogueHandler:
            if default:
                self.default_handler = handler
                return handler

            rule_name = name or handler.__name__.lower()

            skill_rule = MindmeldDialogueRule(
                domain=domain,
                intent=intent,
                entities=entities,
                dialogue_state=rule_name,
                targeted_only=targeted_only,
            )
            self.rules[skill_rule] = handler

            # Order rules by highest to lowest specificity
            existing_rules = list(self.rules.items())
            self.rules = dict(sorted(existing_rules, reverse=True))

            return handler

        return decorator
