import json
from typing import Optional

from dependency_injector.wiring import Provide

from webex_assistant_skills_sdk.shared.models import Dialogue
from webex_assistant_skills_sdk.shared.services import CryptoService, Settings
from webex_assistant_skills_sdk.types import Types


class Invoker():
    __crypto_service: CryptoService =  Provide[Types.CRYPTO_SERVICE]
    __settings: Settings = Provide[Types.SETTINGS]

    def do_turn(self, dialogue: Dialogue, query: str) -> Dialogue:
        new_dialogue = dialogue.copy()

        request = {
            'text': query,
        }

        if self.encryption_enabled:
            request = self.__crypto_service.prepare_payload(
                json.dumps(request),
                self.__settings.key,
                self.secret,
            )

        return new_dialogue()
