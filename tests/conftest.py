import os

from mindmeld import NaturalLanguageProcessor
import pytest

from webex_assistant_sdk import AgentApplication, AssistantDialogueResponder

from .agent import app


@pytest.fixture
def agent_dir():
    return os.path.join(os.path.realpath(os.path.dirname(__file__)), 'agent')


@pytest.fixture
def keys_dir(agent_dir: str):  # pylint: disable=redefined-outer-name
    return agent_dir


@pytest.fixture
def passphrase():
    return b'passphrase'


@pytest.fixture
def responder():
    return AssistantDialogueResponder()


@pytest.fixture
def agent_nlp(agent_dir: str) -> NaturalLanguageProcessor:  # pylint: disable=redefined-outer-name
    """Provides a built processor instance"""
    nlp = NaturalLanguageProcessor(app_path=agent_dir)
    nlp.build()
    nlp.dump()
    return nlp


# pylint: disable=redefined-outer-name
@pytest.fixture
def agent_app(agent_nlp: NaturalLanguageProcessor) -> AgentApplication:
    app.lazy_init(nlp=agent_nlp)
    return app


@pytest.fixture
def client(agent_app: AgentApplication):  # pylint: disable=redefined-outer-name
    server = agent_app._server.test_client()
    yield server
