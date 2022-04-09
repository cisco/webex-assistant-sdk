from __future__ import annotations
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.skill_dialogue import AugmentedSkillResponse, SkillRequest


class DialogueTurn(BaseModel):
    request: SkillRequest
    response: AugmentedSkillResponse


class Dialogue(BaseModel):
    turns: List[DialogueTurn] = []
    
    def add_turn(self, turn: DialogueTurn):
        self.turns.append(turn)

    def get_last_turn(self) -> Optional[DialogueTurn]:
        if len(self.turns) == 0:
            return None

        return self.turns[-1]

    def get_last_history(self) -> List[DialogueTurn]:
        last_turn = self.get_last_turn()

        if last_turn is None:
            return []

        return last_turn.response.history

    def get_last_frame(self) -> Dict[str, Any]:
        last_turn = self.get_last_turn()

        if last_turn is None:
            return {}

        return last_turn.response.frame
