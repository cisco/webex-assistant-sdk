import base64
from typing import Optional

from dependency_injector.wiring import Provide
from fastapi import FastAPI, HTTPException, status
from starlette.middleware import Middleware

from webex_assistant_skills_sdk.api.middlewares import DecryptionMiddleware, SignatureMiddleware
from webex_assistant_skills_sdk.api.shared.services import CryptoService
from webex_assistant_skills_sdk.api.types import Types
from webex_assistant_skills_sdk.shared.models import CheckResponse, InvokeRequest, InvokeResponse
from webex_assistant_skills_sdk.shared.services import Settings


class BaseAPI(FastAPI):
    _crypto_service: CryptoService = Provide[Types.CRYPTO_SERVICE]
    _settings: Settings = Provide[Types.SETTINGS]

    _private_key: Optional[str] = None
    _secret: Optional[str] = None

    def __init__(self, **kwargs) -> None:
        middleware = kwargs.pop('middlewares', [])

        if self._settings.use_encryption:
            self._private_key = self._crypto_service.load_private_key(self._settings.private_key_path.read_bytes())
            self._secret = self._settings.secret.encode('utf-8')
            # NOTE: The order here is significant. We sign the encrypted message so we want our signature
            # verification to run _before_ the decryption middleware which will alter the message to the
            # decrypted version.
            middleware = [
                Middleware(SignatureMiddleware, secret=self._secret),
                Middleware(DecryptionMiddleware, private_key=self._private_key),
                *middleware,
            ]

        super().__init__(**kwargs, middleware=middleware)

        self.router.add_api_route('/parse', self.parse, methods=['POST'], response_model=InvokeResponse)
        self.router.add_api_route('/parse', self.check, methods=['GET'], response_model=CheckResponse)


    async def parse(self, _: InvokeRequest):
        '''Override in subclass'''
        pass

    # This essentially only works because there's no body and thus no call to receive()
    # we should revisit this after seeing if the middlewares can be replaced with custom request types
    async def check(self, signature: str, message: str):
        if not self._settings.use_encryption:
            return CheckResponse(
                challenge=message,
            )

        message_bytes = message.encode('utf-8')
        signature = base64.b64decode(signature.encode('utf-8'))

        signature_valid = self._crypto_service.verify_signature(
            secret=self._secret,
            message=message_bytes,
            signature=signature,
        )

        if not signature_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed to verify signature',
            )
            
        try:
            challenge = self._crypto_service.decrypt(
                private_key=self._private_key,
                message=message_bytes,
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed to decrypt message',
            )

        return CheckResponse(
            challenge=challenge,
        )
