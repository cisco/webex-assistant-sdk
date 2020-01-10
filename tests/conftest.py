import os

from mindmeld import NaturalLanguageProcessor
import pytest

from webex_assistant_sdk import SkillApplication, SkillResponder

from .skill import app


@pytest.fixture
def skill_dir():
    return os.path.join(os.path.realpath(os.path.dirname(__file__)), 'skill')


@pytest.fixture
def keys_dir(skill_dir):  # pylint: disable=redefined-outer-name
    return skill_dir


@pytest.fixture
def passphrase():
    return b'passphrase'


@pytest.fixture
def responder():
    return SkillResponder()


@pytest.fixture
def skill_nlp(skill_dir) -> NaturalLanguageProcessor:  # pylint: disable=redefined-outer-name
    """Provides a built processor instance"""
    nlp = NaturalLanguageProcessor(app_path=skill_dir)
    nlp.build()
    nlp.dump()
    return nlp


# pylint: disable=redefined-outer-name
@pytest.fixture
def skill_app(skill_nlp) -> SkillApplication:
    app.lazy_init(nlp=skill_nlp)
    return app


@pytest.fixture
def client(skill_app: SkillApplication):  # pylint: disable=redefined-outer-name
    server = skill_app._server.test_client()
    yield server
