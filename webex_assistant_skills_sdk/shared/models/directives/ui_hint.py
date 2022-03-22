from typing import List, Optional

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.directives.base_directive import Directive


class UIHintPayload(BaseModel):
    texts: Optional[List[str]]
    prompt: Optional[str]


class UIHint(Directive):
    name: str = 'ui-hint'
    payload: Optional[UIHintPayload]
