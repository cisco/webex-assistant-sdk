import json
import typing

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from starlette.requests import ClientDisconnect
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from webex_assistant_sdk.crypto import decrypt


class DecryptionMiddleware:
    def __init__(self, app: ASGIApp, private_key: RSAPrivateKey, secret: bytes):
        self.app = app
        self.private_key = private_key
        self.secret = secret

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        receiver = DecryptingReceiver(self.private_key, self.app, receive, send)
        response = receiver(scope, receive, send)
        await response


class DecryptingReceiver:
    def __init__(self, private_key: RSAPrivateKey, app: ASGIApp, receive: Receive, send: Send):
        self.private_key = private_key
        self.app = app
        self.send = send
        self.receive = receive

    async def __call__(self, scope, receive: Receive, send: Send):
        await self.app(scope, self.receive_decrypted, send)

    async def receive_decrypted(self) -> Message:
        message = await self.receive()

        assert message["type"] == "http.request"
        message_body = await self.message_body(message)
        encrypted_message = json.loads(message_body)
        message["body"] = decrypt(self.private_key, encrypted_message['message'].encode('utf-8'))

        return message

    async def stream_body(self, message: Message) -> typing.AsyncGenerator[bytes, None]:
        while True:
            if message["type"] == "http.disconnect":
                raise ClientDisconnect()
            body = message.get("body", b"")
            if body:
                yield body
            if not message.get("more_body", False):
                break

            message = await self.receive()
        yield b""

    async def message_body(self, message: Message) -> bytes:
        chunks = [chunk async for chunk in self.stream_body(message)]
        return b"".join(chunks)
