from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr


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
