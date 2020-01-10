from flask import Flask
from mindmeld import Application

from .dialogue import SkillResponder
from .server import create_skill_server


class SkillApplication(Application):
    """
    SkillApplication extends MindMeld application with the appropriate encryption protocols.
    """

    def __init__(
        self, import_name, *, secret, private_key, responder_class=SkillResponder, **kwargs,
    ):

        super().__init__(import_name, responder_class=responder_class, **kwargs)
        self.secret = secret
        self.private_key = private_key

    def lazy_init(self, nlp=None):
        Application.lazy_init(self, nlp)
        self._server = create_skill_server(self.app_manager, self.secret, self.private_key)

    @property
    def web_app(self) -> Flask:
        return self._server
