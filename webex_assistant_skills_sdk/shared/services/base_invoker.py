from __future__ import annotations

from datetime import datetime
import os
from typing import Optional

from dependency_injector.wiring import Provide
from requests import Response

from webex_assistant_skills_sdk.shared.models import (
    AugmentedSkillResponse,
    DeviceContext,
    Dialogue,
    DialogueParams,
    DialogueTurn,
    InvokeRequest,
    InvokeResponse,
)
from webex_assistant_skills_sdk.shared.services import CryptoService
from webex_assistant_skills_sdk.types import Types


class BaseInvoker:
    _crypto_service: CryptoService =  Provide[Types.CRYPTO_SERVICE]

    url: str
    device_context: DeviceContext
    use_encryption: bool
    public_key: Optional[str]
    secret: Optional[str]

    def __init__(
        self,
        url: str,
        device_context: DeviceContext,
        use_encryption: bool,
        public_key: Optional[str] = None,
        secret: Optional[str] = None,
    ) -> None:
        self.url = url
        self.device_context = device_context
        self.use_encryption = use_encryption
        self.public_key = public_key
        self.secret = secret

    def post_request(self, data: str) -> Response:
        '''Override in sublcass'''
        pass 

    def do_turn(
        self,
        dialogue: Dialogue,
        query: str,
        params: Optional[DialogueParams] = None,
    ) -> BaseInvoker:
        if params is None:
            params = self._get_default_dialogue_params()

        challenge = self._generate_challenge_string()

        request = InvokeRequest(
            challenge=challenge,
            text=query,
            context=self.device_context,
            params=params,
            frame=dialogue.get_last_frame(),
            history=dialogue.get_last_history(),
        )

        request_json = request.json()

        if self.use_encryption:
            request_json = self._crypto_service.prepare_payload(
                request_json,
                self.public_key,
                self.secret,
            ).json()

        response = self.post_request(request_json)

        response.raise_for_status()

        invoke_response = InvokeResponse(**response.json())

        if invoke_response.challenge != challenge:
            # TODO: raise challenge exception
            raise Exception()

        skill_response = AugmentedSkillResponse(**invoke_response.dict())

        dialogue.add_turn(DialogueTurn(
            request=request,
            response=skill_response,
        ))

        return self # allow chaining

    def _generate_challenge_string(self) -> str:
        return os.urandom(32).hex()

    def _get_default_dialogue_params(self) -> DialogueParams:
        return DialogueParams(
            time_zone='UTC',
            timestamp=datetime.utcnow().timestamp(),
            language='en'
        )
