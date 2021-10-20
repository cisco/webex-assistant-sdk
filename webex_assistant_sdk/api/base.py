from typing import Optional

from fastapi import FastAPI
from pydantic import BaseSettings
from starlette.middleware import Middleware

from webex_assistant_sdk.crypto.messages import load_private_key
from webex_assistant_sdk.settings import SkillSettings

from ..models.http import SkillInvokeRequest, SkillInvokeResponse
from .middlewares import DecryptionMiddleware
from .middlewares.signing import SignatureMiddleware


# TODO: Disable OpenAPI by default
class BaseAPI(FastAPI):
    def __init__(self, nlp=None, dialogue_manager=None, settings: Optional[BaseSettings] = None, **kwargs):
        self.settings = settings or SkillSettings()
        middleware = kwargs.pop('middlewares', [])

        self.nlp = nlp
        self.dialogue_manager = dialogue_manager

        if self.settings.use_encryption:
            private_key = load_private_key(self.settings.private_key_path.read_bytes())
            secret = self.settings.secret.encode('utf-8')
            middleware = [
                Middleware(SignatureMiddleware, secret=secret),
                Middleware(DecryptionMiddleware, private_key=private_key),
                *middleware,
            ]

        super().__init__(**kwargs, middleware=middleware)
        self.router.add_api_route('/parse', self.parse, methods=['POST'], response_model=SkillInvokeResponse)

    async def parse(self, request: SkillInvokeRequest):
        pass
