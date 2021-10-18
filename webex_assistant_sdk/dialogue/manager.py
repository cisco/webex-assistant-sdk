import re
from typing import Dict, Optional

from ..models.mindmeld import DialogueState, ProcessedQuery
from ..types import DialogueHandler
from .rules import MMDialogueStateRule, SimpleDialogueStateRule


class MissingHandler(Exception):
    pass


RuleMap = Dict[SimpleDialogueStateRule, DialogueHandler]


class MMDialogueManager:
    def __init__(self, rules=None, default_handler=None):
        self.rules = rules or {}
        self.default_handler = default_handler

    async def handle(self, processed_query, current_state):
        # Iterate over our rules, taking the first match
        handler = self.get_dialogue_state(processed_query, current_state.params.target_dialogue_state)
        handler = handler or self.default_handler

        if not handler:
            raise MissingHandler('No handler found')

        return await handler(current_state)

    def get_dialogue_state(
        self, query: ProcessedQuery, dialogue_state: Optional[str] = None
    ) -> Optional[DialogueHandler]:
        # TODO: this needs to iterate over a sorted list of rules by specificity to determine
        # which rule matches.
        for rule, handler in self.rules.items():
            if dialogue_state and rule.dialogue_state == dialogue_state:
                return handler
            if not dialogue_state and rule.match(query):
                return handler
        return None

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

            return handler

        return decorator


class SimpleDialogueManager:
    def __init__(self, rules: Optional[RuleMap] = None, default_handler: Optional[DialogueHandler] = None):
        self.rules = rules or {}
        self.default_handler = default_handler

    async def handle(self, current_state: DialogueState):
        # Iterate over our rules, taking the first match
        handler = self.get_dialogue_state(current_state.text, current_state.params.target_dialogue_state)
        handler = handler or self.default_handler

        if not handler:
            # TODO: Different message
            raise MissingHandler('No handler found')

        return await handler(current_state)

    def get_dialogue_state(self, query: str, target_state: Optional[str] = None) -> Optional[DialogueHandler]:
        for rule, handler in self.rules.items():
            if target_state and rule.dialogue_state == target_state:
                return handler
            if not target_state and rule.match(query):
                return handler
        return None

    def add_rule(
        self, *, name: Optional[str] = None, pattern: Optional[str] = None, default=False, targeted_only=False
    ):
        """Wraps a function to behave as a dialogue handler"""

        # TODO: Take a closer look at the setup here, I'd like to have type hinting
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
