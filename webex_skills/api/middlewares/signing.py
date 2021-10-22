import base64
import json
import logging

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from ...crypto import verify_signature
from .base import BaseReceiver

logger = logging.getLogger(__name__)


class SignatureVerificationError(Exception):
    pass


class SignatureMiddleware:
    def __init__(self, app: ASGIApp, secret: bytes):
        self.app = app
        self.secret = secret

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        receiver = SignatureReceiver(self.secret, self.app, receive, send)
        response = receiver(scope, receive, send)
        await response


class SignatureReceiver(BaseReceiver):
    def __init__(self, secret: bytes, app: ASGIApp, receive: Receive, send: Send):
        super().__init__(app, receive, send)
        self.secret = secret

    async def __call__(self, scope, receive: Receive, send: Send):
        await self.app(scope, self.verify_signature, send)

    async def verify_signature(self) -> Message:
        message = await self.receive()

        assert message["type"] == "http.request"
        message_body = await self.message_body(message)
        encrypted_body = json.loads(message_body)
        encrypted_message = encrypted_body['message']
        signature = encrypted_body['signature']

        signature: bytes = base64.b64decode(signature)

        if not verify_signature(self.secret, encrypted_message.encode('utf-8'), signature):
            msg = 'Failed to validate signature'
            logger.error(msg)
            raise SignatureVerificationError(msg)
        return message
