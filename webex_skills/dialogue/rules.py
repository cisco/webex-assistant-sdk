from functools import total_ordering
import re
from typing import Optional

from ..models.mindmeld import ProcessedQuery


@total_ordering
class MMDialogueStateRule:
    def __init__(self, domain, intent, entities, dialogue_state, targeted_only):
        self.domain = domain
        self.intent = intent

        if entities:
            entities = set(entities)

        self.entities = entities
        self.targeted_only = targeted_only
        self.dialogue_state = dialogue_state

    def match(self, processed_query: ProcessedQuery):
        if self.targeted_only:
            return False

        if self.domain is not None and self.domain != processed_query.domain:
            return False

        # check intent is correct
        if self.intent is not None and self.intent != processed_query.intent:
            return False

        # check expected entity types are present
        if self.entities is not None:
            entity_types = set(entity['type'] for entity in processed_query.entities)
            if len(self.entities & entity_types) < len(self.entities):
                return False

        return True

    def __gt__(self, other: "MMDialogueStateRule"):
        return self.specificity > other.specificity

    @property
    def specificity(self):
        value = 0
        if self.domain:
            value += 1
        if self.intent:
            value += 1
        if self.entities:
            value += len(self.entities)
        return value


class SimpleDialogueStateRule:
    def __init__(self, regex: Optional[re.Pattern], dialogue_state: str):
        self.regex = regex
        self.dialogue_state = dialogue_state

    def match(self, text) -> Optional[re.Match]:
        if not self.regex:
            return None
        return self.regex.match(text)
