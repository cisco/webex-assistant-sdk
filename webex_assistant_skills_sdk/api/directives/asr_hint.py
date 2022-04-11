from typing import List, Optional

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models import Directive


class ASRHintPayload(BaseModel):
    texts: Optional[List[str]]


class ASRHint(Directive):
    name: str = 'asr-hint'
    payload: Optional[ASRHintPayload]

    def __init__(
        self,
        texts: Optional[List[str]] = None
    ) -> None:
        super().__init__(payload=ASRHintPayload(
            texts=texts,
        ))
