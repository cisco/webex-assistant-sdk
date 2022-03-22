from typing import Optional

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.directives.base_directive import Directive


class DisplayWebViewPayload(BaseModel):
    url: str
    title: Optional[str]


class DisplayWebView(Directive):
    name: str = 'display-web-view'
    payload: DisplayWebViewPayload
