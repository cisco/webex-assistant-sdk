from __future__ import annotations
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr

from webex_assistant_skills_sdk.shared.models.context import DeviceContext
from webex_assistant_skills_sdk.shared.models.base_directive import Directive


class DialogueParams(BaseModel):
    time_zone: str
    timestamp: int
    # We enforce length via min/max length in addition to the regex so we get a more
    # useful error message if the length is wrong.
    language: constr(min_length=2, max_length=2, regex="^[a-zA-Z]{2}$")  # type: ignore  # noqa
    target_dialogue_state: Optional[str]
    locale: Optional[constr(regex="^[a-z]{2}([-_][A-Z]{2})?$")]  # type: ignore  # noqa
    dynamic_resource: Optional[Dict[Any, Any]] = {}
    allowed_intents: Optional[List[str]] = []


class DialogueEventBase(BaseModel):
    directives: Optional[List[Directive]]
    frame: Dict[str, Any] = []
    params: DialogueParams = {}
    history: List[DialogueTurn] = []

class DialogueTurn(DialogueEventBase):
    text: str
    context: Optional[DeviceContext] = None

    def update_history(self, last_turn: DialogueTurn):
        self.history.append(DialogueTurn(
            **last_turn.dict(exclude={'history'}),
        ))


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

        return last_turn.history

    def get_last_frame(self) -> Dict[str, Any]:
        last_turn = self.get_last_turn()

        if last_turn is None:
            return {}

        return last_turn.frame

DialogueEventBase.update_forward_refs()
