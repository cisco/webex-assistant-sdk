import pytest

from webex_assistant_sdk import AssistantDialogueResponder


@pytest.fixture
def responder():
    return AssistantDialogueResponder()
