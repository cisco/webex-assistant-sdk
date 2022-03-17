import base64
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseSettings
from starlette.middleware import Middleware
from starlette.responses import JSONResponse

from ..crypto import verify_signature
from ..crypto.messages import decrypt, load_private_key
from ..models.http import SkillInvokeRequest, SkillInvokeResponse
from ..settings import SkillSettings
from .middlewares import DecryptionMiddleware
from .middlewares.signing import SignatureMiddleware


class BaseAPI(FastAPI):
    def __init__(self, nlp=None, dialogue_manager=None, settings: Optional[BaseSettings] = None, **kwargs):
        self.settings = settings or SkillSettings()
        self.private_key = None
        self.secret = None
        self.nlp = nlp
        self.dialogue_manager = dialogue_manager

        middleware = kwargs.pop('middlewares', [])

        if self.settings.use_encryption:
            self.private_key = load_private_key(self.settings.private_key_path.read_bytes())
            self.secret = self.settings.secret.encode('utf-8')
            # NOTE: The order here is significant. We sign the encrypted message so we want our signature
            # verification to run _before_ the decryption middleware which will alter the message to the
            # decrypted version.
            middleware = [
                Middleware(SignatureMiddleware, secret=self.secret),
                Middleware(DecryptionMiddleware, private_key=self.private_key),
                *middleware,
            ]

        super().__init__(**kwargs, middleware=middleware)
        self.router.add_api_route('/parse', self.parse, methods=['POST'], response_model=SkillInvokeResponse)
        self.router.add_api_route('/parse', self.check, methods=['GET'])

    async def parse(self, request: SkillInvokeRequest):
        pass

    # This essentially only works because there's no body and thus no call to receive()
    # we should revisit this after seeing if the middlewares can be replaced with custom request types
    async def check(self, signature: str, message: str):
        message_bytes = message.encode('utf-8')
        signature: bytes = base64.b64decode(signature.encode('utf-8'))

        if not verify_signature(secret=self.secret, message=message_bytes, signature=signature):
            return JSONResponse({'message': 'Failed to verify signature'}, status_code=400)
        try:
            challenge = decrypt(private_key=self.private_key, message=message_bytes)
        except ValueError:
            return JSONResponse({'message': 'Failed to decrypt message'}, status_code=400)
        return {'challenge': challenge}
