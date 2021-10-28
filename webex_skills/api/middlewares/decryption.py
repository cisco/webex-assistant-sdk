import json
import logging

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from ...crypto import decrypt
from .base import BaseReceiver

logger = logging.getLogger(__name__)


class DecryptionError(Exception):
    pass


class DecryptionMiddleware:
    def __init__(self, app: ASGIApp, private_key: RSAPrivateKey):
        self.app = app
        self.private_key = private_key

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        receiver = DecryptingReceiver(self.private_key, self.app, receive, send)
        response = receiver(scope, receive, send)
        await response


class DecryptingReceiver(BaseReceiver):
    def __init__(self, private_key: RSAPrivateKey, app: ASGIApp, receive: Receive, send: Send):
        super().__init__(app=app, receive=receive, send=send)
        self.private_key = private_key

    async def __call__(self, scope, receive: Receive, send: Send):
        await self.app(scope, self.receive_decrypted, send)

    async def receive_decrypted(self) -> Message:
        message = await self.receive()

        assert message["type"] == "http.request"
        message_body = await self.message_body(message)
        encrypted_message = json.loads(message_body)
        try:
            message["body"] = decrypt(self.private_key, encrypted_message['message'].encode('utf-8'))
        except ValueError as value_exc:
            # We log with error rather than exception here because the exception raised by cryptography
            # if decryption fails doesn't provide useful information, and the stack trace is largely unhelpful
            msg = 'Failed to decrypt payload'
            logger.error(msg)
            raise DecryptionError(msg) from value_exc

        return message
