import inspect
import re
from typing import List, Optional

from ..models.mindmeld import DialogueState
from ..types import DialogueHandler, DialogueQuery, RuleMap
from .rules import MMDialogueStateRule, SimpleDialogueStateRule


class MissingHandler(Exception):
    pass


class DialogueManager:
    def __init__(self, rules: Optional[RuleMap] = None, default_handler: Optional[DialogueHandler] = None):
        self.rules = rules or {}
        self.default_handler = default_handler

    def get_handler(self, query: DialogueQuery, target_state: Optional[str] = None) -> Optional[DialogueHandler]:
        for rule, handler in self.rules.items():
            if target_state and rule.dialogue_state == target_state:
                return handler
            if not target_state and rule.match(query):
                return handler
        return None

    async def handle(self, query: DialogueQuery, current_state: DialogueState):
        # Iterate over our rules, taking the first match
        handler = self.get_handler(query, current_state.params.target_dialogue_state)
        handler = handler or self.default_handler

        if not handler:
            # TODO: Different message  # pylint:disable=fixme
            raise MissingHandler('No handler found')

        # TODO: Use annotated types rather than length  # pylint:disable=fixme
        handler_args = inspect.signature(handler)
        if len(handler_args.parameters) == 2:
            new_state = await handler(current_state, query)
        else:
            new_state = await handler(current_state)
        new_state.update_history(old_state=current_state)
        return new_state


class MMDialogueManager(DialogueManager):
    def add_rule(
        self,
        *,
        name: Optional[str] = None,
        default=False,
        domain=None,
        intent=None,
        entities=None,
        targeted_only=False,
    ):
        """Wraps a function to behave as a dialogue handler"""

        def decorator(handler: DialogueHandler) -> DialogueHandler:
            if default:
                self.default_handler = handler
                return handler

            rule_name = name or handler.__name__.lower()
            skill_rule = MMDialogueStateRule(domain, intent, entities, rule_name, targeted_only=targeted_only)
            self.rules[skill_rule] = handler
            existing_rules: List[(MMDialogueStateRule, DialogueHandler)] = list(self.rules.items())
            self.rules = dict(sorted(existing_rules, reverse=True))

            return handler

        return decorator


class SimpleDialogueManager(DialogueManager):
    def add_rule(
        self, *, name: Optional[str] = None, pattern: Optional[str] = None, default=False, targeted_only=False
    ):
        """Wraps a function to behave as a dialogue handler"""

        # TODO: Take a closer look at the setup here, I'd like to have type hinting  # pylint:disable=fixme
        # catch if a function doesn't meet what's expected as a DialogueHandler
        # Just checking if handler is a coroutine is also an option
        def decorator(handler: DialogueHandler) -> DialogueHandler:
            if default:
                self.default_handler = handler
                return handler

            rule_name = name or handler.__name__.lower()
            if targeted_only:
                skill_rule = SimpleDialogueStateRule(None, rule_name)
                self.rules[skill_rule] = handler
            else:
                compiled = re.compile(pattern)
                skill_rule = SimpleDialogueStateRule(compiled, rule_name)
                self.rules[skill_rule] = handler

            return handler

        return decorator
