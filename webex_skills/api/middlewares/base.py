import typing

from starlette.requests import ClientDisconnect
from starlette.types import ASGIApp, Message, Receive, Send


class BaseReceiver:
    def __init__(self, app: ASGIApp, receive: Receive, send: Send) -> None:
        self.app = app
        self.receive = receive
        self.send = send

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
