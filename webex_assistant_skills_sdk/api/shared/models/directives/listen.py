from webex_assistant_skills_sdk.shared.models import Directive


class Listen(Directive):
    name: str = 'listen'

    def __init__(self) -> None:
        super().__init__()
