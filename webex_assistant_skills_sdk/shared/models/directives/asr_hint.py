from typing import List, Optional

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.directives.base_directive import Directive


class ASRHintPayload(BaseModel):
    texts: Optional[List[str]]


class ASRHint(Directive):
    name: str = 'asr-hint'
    payload: Optional[ASRHintPayload]
