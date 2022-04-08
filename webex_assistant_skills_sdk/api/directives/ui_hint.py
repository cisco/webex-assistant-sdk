from typing import List, Optional

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models import Directive


class UIHintPayload(BaseModel):
    texts: Optional[List[str]]
    prompt: Optional[str]


class UIHint(Directive):
    name: str = 'ui-hint'
    payload: Optional[UIHintPayload]

    def __init__(
        self,
        texts: Optional[List[str]],
        prompt: Optional[str],
    ):
        super().__init__(payload=UIHintPayload(
            texts=texts,
            prompt=prompt,
        ))
