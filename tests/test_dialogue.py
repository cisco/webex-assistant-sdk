from mock import AsyncMock
import pytest

from webex_assistant_sdk.dialogue.manager import MissingHandler, SimpleDialogueManager
from webex_assistant_sdk.dialogue.rules import SimpleDialogueStateRule
from webex_assistant_sdk.models.mindmeld import DialogueState

pytestmark = pytest.mark.asyncio


async def test_rule_matching(dialogue_state, test_rule):
    mock_handler = AsyncMock()
    manager = SimpleDialogueManager(rules={test_rule: mock_handler})

    state = DialogueState()
    await manager.handle(state)
    assert mock_handler.called


async def test_rule_ordering(dialogue_state: DialogueState, test_rule: SimpleDialogueStateRule):
    mock_handler1 = AsyncMock()
    mock_handler2 = AsyncMock()
    test_rule2 = SimpleDialogueStateRule(test_rule.regex)

    manager = SimpleDialogueManager(rules={test_rule: mock_handler1, test_rule2: mock_handler2})
    await manager.handle(dialogue_state)
    assert mock_handler1.called
    assert not mock_handler2.called

    # Reorder and make sure the first is still called
    mock_handler1.reset_mock()
    mock_handler2.reset_mock()

    manager = SimpleDialogueManager(rules={test_rule: mock_handler2, test_rule2: mock_handler1})
    await manager.handle(dialogue_state)
    assert mock_handler2.called
    assert not mock_handler1.called


def test_add_rule():
    manager = SimpleDialogueManager()

    @manager.add_rule(pattern=".*test.*")
    def test_func(state):
        pass

    assert test_func in manager.rules.values()


def test_add_default():
    manager = SimpleDialogueManager()

    @manager.add_rule(default=True)
    async def test_func(state):
        pass

    assert test_func not in manager.rules.values()
    assert manager.default_handler == test_func


async def test_no_match_with_default(dialogue_state: DialogueState):
    manager = SimpleDialogueManager()

    default_mock = AsyncMock()
    manager.add_rule(default=True)(default_mock)

    @manager.add_rule(pattern=".*test.*")
    async def pattern_test(state):
        pass

    dialogue_state.text = "something that won't match"
    await manager.handle(dialogue_state)
    assert default_mock.called


async def test_no_match_no_default(dialogue_state):
    manager = SimpleDialogueManager()
    with pytest.raises(MissingHandler):
        await manager.handle(dialogue_state)
