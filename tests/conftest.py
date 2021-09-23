import os

from mindmeld import NaturalLanguageProcessor
import pytest

from webex_assistant_sdk.app import SkillApplication
from webex_assistant_sdk.dialogue import SkillResponder

from .skill import app


@pytest.fixture(name='skill_dir')
def _skill_dir():
    return os.path.join(os.path.realpath(os.path.dirname(__file__)), 'skill')


@pytest.fixture
def responder():
    return SkillResponder()


@pytest.fixture(name='skill_nlp')
def _skill_nlp(skill_dir) -> NaturalLanguageProcessor:
    """Provides a built processor instance"""
    nlp = NaturalLanguageProcessor(app_path=skill_dir)
    nlp.build()
    nlp.dump()
    return nlp


@pytest.fixture(name='skill_app')
def _skill_app(skill_nlp) -> SkillApplication:
    app.lazy_init(nlp=skill_nlp)
    return app


@pytest.fixture(name='client')
def _client(skill_app: SkillApplication):
    server = skill_app._server.test_client()
    yield server
