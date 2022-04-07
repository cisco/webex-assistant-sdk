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
    __crypto_service: CryptoService = Provide[Types.CRYPTO_SERVICE]
    __settings: Settings = Provide[Types.SETTINGS]

    __private_key: Optional[str] = None
    __secret: Optional[str] = None

    def __init__(self, **kwargs) -> None:
        middleware = kwargs.pop('middlewares', [])

        if self.__settings.use_encryption:
            self.__private_key = self.__crypto_service.load_private_key(self.__settings.private_key_path.read_bytes())
            self.__secret = self.__settings.secret.encode('utf-8')
            # NOTE: The order here is significant. We sign the encrypted message so we want our signature
            # verification to run _before_ the decryption middleware which will alter the message to the
            # decrypted version.
            middleware = [
                Middleware(SignatureMiddleware, secret=self.__secret),
                Middleware(DecryptionMiddleware, private_key=self.__private_key),
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
        if not self.__settings.use_encryption:
            return CheckResponse(
                challenge=message,
            )

        message_bytes = message.encode('utf-8')
        signature = base64.b64decode(signature.encode('utf-8'))

        signature_valid = self.__crypto_service.verify_signature(
            secret=self.__secret,
            message=message_bytes,
            signature=signature,
        )

        if not signature_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed to verify signature',
            )
            
        try:
            challenge = self.__crypto_service.decrypt(
                private_key=self.__private_key,
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
