from typing import Any

from fastapi import FastAPI
from starlette.middleware import Middleware

from webex_assistant_sdk.config import SkillSettings
from webex_assistant_sdk.crypto.messages import load_private_key

from .middlewares import DecryptionMiddleware


# TODO: Figure out dialogue manager stuff
class API(FastAPI):
    def __init__(self, *args, **extra: Any) -> None:
        # TODO: Add signature validation/challenge middleware
        # TODO: Add Response serialization -- Handled by FastAPI for non-mm cases
        self.settings = SkillSettings()
        middleware = extra.get('middlewares', [])

        if self.settings.use_encryption:
            private_key = load_private_key(self.settings.private_key_path.read_bytes())
            secret = self.settings.secret.encode('utf-8')
            middleware = [Middleware(DecryptionMiddleware, private_key=private_key, secret=secret), *middleware]

        super().__init__(*args, **extra, middleware=middleware)
        self.mindmeld = self.settings.mindmeld
        if self.mindmeld:
            # TODO: Update routes so parse_mm handles the /parse endpoint
            # TODO: Initialize NLP and DM
            pass
        self._mm_app = None
        self.skill_name = self.settings.skill_name

    def parse_mm(self):
        """A default parse method for mindmeld apps so the user only has to handle dialogue stuff"""
        pass

    def handle(self):
        """Wraps a function to behave as a dialogue handler"""
        pass

    @property
    def is_mm(self):
        return self._mm_app is None
