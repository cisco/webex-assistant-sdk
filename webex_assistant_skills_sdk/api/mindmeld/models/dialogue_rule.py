from __future__ import annotations

from functools import total_ordering
from typing import Optional, Set

from webex_assistant_skills_sdk.api.mindmeld.models.processed_query import ProcessedQuery
from webex_assistant_skills_sdk.api.shared.models import DialogueRule


@total_ordering
class MindmeldDialogueRule(DialogueRule[ProcessedQuery]):
    domain: Optional[str] = None
    intent: Optional[str] = None
    entities: Optional[Set[str]] = None
    targeted_only: bool = False

    def match(self, processed_query: ProcessedQuery) -> bool:
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

    @property
    def specificity(self):
        specificity = 0
        if self.domain is not None:
            specificity += 1

        if self.intent is not None:
            specificity += 1

        if self.entities is not None:
            specificity += len(self.entities)

        return specificity

    def __gt__(self, other: MindmeldDialogueRule):
        return self.specificity > other.specificity
    