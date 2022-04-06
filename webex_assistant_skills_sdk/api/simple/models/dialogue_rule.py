import re
from typing import Optional

from webex_assistant_skills_sdk.api.shared.models import DialogueRule


class SimpleDialogueRule(DialogueRule[str]):
    regex: Optional[re.Pattern] = None

    def match(self, text: str) -> bool:
        if self.regex is None:
            return False

        return bool(self.regex.match(text))

    class Config:
        arbitrary_types_allowed = True
