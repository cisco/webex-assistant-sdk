import re

import pytest

from webex_skills.dialogue.rules import SimpleDialogueStateRule
from webex_skills.models.mindmeld import DialogueState

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def dialogue_state():
    return DialogueState(
        text='test',
        context={},
        params={'time_zone': 'thing', 'timestamp': 12345, 'language': 'en'},
        frame={},
    )


@pytest.fixture
def test_rule():
    return SimpleDialogueStateRule(re.compile('.*test.*'), 'test')
