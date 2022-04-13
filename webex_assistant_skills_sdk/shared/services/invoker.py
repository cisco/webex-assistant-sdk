from __future__ import annotations

from typing import Tuple

from dependency_injector.wiring import Provide
import httpx

from webex_assistant_skills_sdk.shared.models import CheckResponse, EncryptedPayload
from webex_assistant_skills_sdk.shared.services.base_invoker import BaseInvoker
from webex_assistant_skills_sdk.shared.services.crypto import CryptoService
from webex_assistant_skills_sdk.types import Types


class Invoker(BaseInvoker):
    _crypto_service: CryptoService =  Provide[Types.CRYPTO_SERVICE]

    def check(self) -> Tuple[CheckResponse, bool]:
        challenge = self._generate_challenge_string()

        if not self.use_encryption:
            # fake encrypted payload
            params_dict = EncryptedPayload(
                signature='',
                message=challenge,
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

    def post_request(self, request_json: str) -> httpx.Response:
        return httpx.post(self.url, data=request_json)
