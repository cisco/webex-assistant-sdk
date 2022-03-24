from webex_assistant_skills_sdk.shared.models import Directive


class ClearWebView(Directive):
    name: str = 'clear-web-view'

    def __init__(self) -> None:
        super().__init__()
