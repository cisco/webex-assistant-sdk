# pylint:disable=no-name-in-module

from __future__ import annotations

from typing import Any, Dict, ForwardRef, List, Optional

from pydantic import BaseModel, constr

# Mindmeld's Request object is essentially just a ProcessedQuery object + the dialogue manager stuff


class Params(BaseModel):
    target_dialogue_state: Optional[str]
    time_zone: str
    timestamp: int
    # We enforce length via min/max length in addition to the regex so we get a more
    # useful error message if the length is wrong.
    language: constr(min_length=2, max_length=2, regex="^[a-zA-Z]{2}$")  # type: ignore  # noqa
    locale: Optional[constr(regex="^[a-z]{2}([-_][A-Z]{2})?$")]  # type: ignore  # noqa
    dynamic_resource: Optional[Dict[Any, Any]] = {}
    allowed_intents: Optional[List[str]] = []


class ProcessedQuery(BaseModel):
    # This is a subset of the fields on ProcessedQuery. We will only ever receive a single transcript
    # So we don't need to include any of the nbest_* fields or the confidence
    text: str
    domain: Optional[str]
    intent: Optional[str]
    # TODO: Add proper typing for entities (dict with keys for entity types and values)   # pylint:disable=fixme
    entities: Optional[List[Dict[str, Any]]] = []


_DialogueState = ForwardRef('DialogueState')


class DialogueState(BaseModel):
    text: Optional[str]
    context: Dict[Any, Any]
    params: Params
    frame: Dict[Any, Any]
    history: Optional[List[_DialogueState]] = []
    # TODO: Unsure if I should put this directly on the State object or  # pylint:disable=fixme
    #  if our method should just be required
    # to return a state and a list of directives
    directives: Optional[List[Dict[Any, Any]]] = []

    def update_history(self, old_state: DialogueState):
        old_state_dict = DialogueState(**old_state.dict(exclude={'history'}))
        self.history.append(old_state_dict)


DialogueState.update_forward_refs()
