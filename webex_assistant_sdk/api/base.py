from typing import TYPE_CHECKING, Coroutine, Optional

from fastapi import FastAPI
from pydantic import BaseSettings
from starlette.middleware import Middleware
from starlette.routing import Route

from webex_assistant_sdk.config import SkillSettings
from webex_assistant_sdk.crypto.messages import load_private_key

from ..models.http import SkillInvokeRequest
from .middlewares import DecryptionMiddleware
from .middlewares.signing import SignatureMiddleware

if TYPE_CHECKING:
    from mindmeld import DialogueResponder

    AsyncHandler = Coroutine[DialogueResponder]


class BaseAPI(FastAPI):
    def __init__(self, *args, settings: Optional[BaseSettings] = None, **extra):
        # TODO: Add Response serialization -- Handled by FastAPI for non-mm cases
        # TODO: Support additional passed in routes
        self.settings = settings or SkillSettings()
        middleware = extra.get('middlewares', [])

        if self.settings.use_encryption:
            private_key = load_private_key(self.settings.private_key_path.read_bytes())
            secret = self.settings.secret.encode('utf-8')
            middleware = [
                Middleware(SignatureMiddleware, secret=secret),
                Middleware(DecryptionMiddleware, private_key=private_key),
                *middleware,
            ]

        # routes = [Route('/parse', self.parse, methods=['POST'])]
        super().__init__(*args, **extra, middleware=middleware)

    def handle(self):
        pass

    def parse(self, request: SkillInvokeRequest):
        pass
