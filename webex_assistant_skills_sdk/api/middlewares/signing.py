import base64
import json
import logging

from dependency_injector.wiring import Provide
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from webex_assistant_skills_sdk.api.middlewares.base import BaseReceiver
from webex_assistant_skills_sdk.api.shared.services import CryptoService
from webex_assistant_skills_sdk.api.types import Types
from webex_assistant_skills_sdk.shared.models.invoke import EncryptedPayload


logger = logging.getLogger(__name__)


class SignatureVerificationError(Exception):
    pass


class SignatureMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        secret: bytes,
    ):
        self.app = app
        self.secret = secret

    async def __call__(
        self,
        scope: Scope, 
        receive: Receive,
        send: Send,
    ):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        receiver = SignatureReceiver(self.secret, self.app, receive, send)
        response = receiver(scope, receive, send)
        await response


class SignatureReceiver(BaseReceiver):
    _crypto_service: CryptoService = Provide[Types.CRYPTO_SERVICE]

    def __init__(
        self, 
        secret: bytes,
        app: ASGIApp,
        receive: Receive,
        send: Send,
    ):
        super().__init__(app, receive, send)
        self.secret = secret

    async def __call__(self, scope, _: Receive, send: Send):
        await self.app(scope, self.verify_signature, send)

    async def verify_signature(self) -> Message:
        message = await self.receive()

        assert message["type"] == "http.request"

        message_body = await self.message_body(message)
        encrypted_body = EncryptedPayload(
            **json.loads(message_body),
        )

        signature: bytes = base64.b64decode(encrypted_body.signature)

        signature_vaid = self._crypto_service.verify_signature(
            self.secret,
            encrypted_body.message.encode('utf-8'),
            signature,
        )

        if not signature_vaid:
            msg = 'Failed to validate signature'
            logger.error(msg)
            raise SignatureVerificationError(msg)

        return message
