import json

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from webex_assistant_sdk.api.middlewares.base import BaseReceiver
from webex_assistant_sdk.crypto import decrypt


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

    # TODO: Properly handle a failed decryption
    async def receive_decrypted(self) -> Message:
        message = await self.receive()

        assert message["type"] == "http.request"
        message_body = await self.message_body(message)
        encrypted_message = json.loads(message_body)
        message["body"] = decrypt(self.private_key, encrypted_message['message'].encode('utf-8'))

        return message
