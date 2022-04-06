import json
import logging

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from dependency_injector.wiring import Provide
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from webex_assistant_skills_sdk.api.middlewares.base import BaseReceiver
from webex_assistant_skills_sdk.api.shared.services import CryptoService
from webex_assistant_skills_sdk.api.types import Types
from webex_assistant_skills_sdk.shared.models import EncryptedInvokeRequest


logger = logging.getLogger(__name__)

class DecryptionError(Exception):
    pass


class DecryptionMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        private_key: RSAPrivateKey,
    ):
        self.app = app
        self.private_key = private_key

    async def __call__(
        self, scope: Scope,
        receive: Receive,
        send: Send,
    ):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        receiver = DecryptingReceiver(self.private_key, self.app, receive, send)
        response = receiver(scope, receive, send)

        await response 


class DecryptingReceiver(BaseReceiver):
    __crypto_service: CryptoService = Provide[Types.CRYPTO_SERVICE]

    def __init__(
        self,
        private_key: RSAPrivateKey,
        app: ASGIApp,
        receive: Receive,
        send: Send,
    ):
        super().__init__(app=app, receive=receive, send=send)

        self.private_key = private_key

    async def __call__(self, scope, _: Receive, send: Send):
        await self.app(scope, self.receive_decrypted, send)

    async def receive_decrypted(self) -> Message:
        message = await self.receive()

        assert message["type"] == "http.request"

        message_body = await self.message_body(message)
        encrypted_message = EncryptedInvokeRequest(
            **json.loads(message_body),
        )

        try:
            message["body"] = self.__crypto_service.decrypt(
                self.private_key,
                encrypted_message.message.encode('utf-8'),
            )
        except ValueError as value_exc:
            msg = 'Failed to decrypt payload'
            logger.error(msg)
            raise DecryptionError(msg) from value_exc

        return message
