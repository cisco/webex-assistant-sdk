from __future__ import annotations

from datetime import datetime
import os
from typing import Optional, Tuple

from dependency_injector.wiring import Provide
import httpx

from webex_assistant_skills_sdk.shared.models import (
    AugmentedSkillResponse,
    CheckResponse,
    DeviceContext,
    Dialogue,
    DialogueParams,
    DialogueTurn,
    EncryptedPayload,
    InvokeRequest,
    InvokeResponse,
)
from webex_assistant_skills_sdk.shared.services import CryptoService
from webex_assistant_skills_sdk.types import Types


class Invoker():
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

    def check(self) -> Tuple[CheckResponse, bool]:
        challenge = self._generate_challenge_string()

        if not self.use_encryption:
            # fake encrypted payload
            params_dict = EncryptedPayload(
                signature='',
                message='challenge',
            ).dict()
        else:
            params_dict = self._crypto_service.prepare_payload(
                payload=challenge,
                public_key=self.public_key,
                secret=self.secret,
            ).dict()

        response = httpx.get(self.url, params=params_dict)

        response.raise_for_status()

        check_response = CheckResponse(**response.json())

        success = check_response.challenge == challenge

        return (check_response, success)

    def do_turn(
        self,
        dialogue: Dialogue,
        query: str,
        params: Optional[DialogueParams] = None,
    ) -> Invoker:
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

        response = httpx.post(self.url, data=request_json)

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
