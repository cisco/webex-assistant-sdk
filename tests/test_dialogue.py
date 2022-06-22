import pytest

from webex_skills.dialogue.manager import SimpleDialogueManager


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
