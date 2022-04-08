from typing import Optional

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models import Directive


class DisplayWebViewPayload(BaseModel):
    url: str
    title: Optional[str]


class DisplayWebView(Directive):
    name: str = 'display-web-view'
    payload: DisplayWebViewPayload

    def __init__(
        self,
        url: str,
        title: Optional[str],
    ) -> None:
        super().__init__(payload=DisplayWebViewPayload(
            url=url,
            title=title,
        ))
