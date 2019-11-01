import pytest

from webex_assistant_sdk import AssistantDialogueResponder
from webex_assistant_sdk.dialogue import DirectiveFormatError


@pytest.mark.parametrize(
    "query, remove_hyphens, text",
    [
        ("is this room open for an hour", False, "is this room open for an hour"),
        ("spark-assistant", True, "spark assistant"),
        ("spark-assistant", False, "spark-assistant"),
        ("speak-to webex-assistant", True, "speak to webex assistant"),
    ],
)
def test_speak(responder: AssistantDialogueResponder, query: str, remove_hyphens: bool, text: str):
    responder.speak(text=query, remove_hyphens=remove_hyphens)
    assert responder.directives[0]['payload']['text'] == text
    assert responder.directives[0]['name'] == 'speak'
    assert responder.directives[0]['type'] == 'action'


@pytest.mark.parametrize(
    "key, value",
    [('pload', 'view'), ('url', 'www.google.com'), (1, 2), ('texts', ['hello', 'world'])],
)
def test_display(responder: AssistantDialogueResponder, key, value):
    responder.display('display', {key: value})
    assert responder.directives[0]['payload'][key] == value
    assert responder.directives[0]['name'] == 'display'
    assert responder.directives[0]['type'] == 'view'


def test_display_web_view(responder: AssistantDialogueResponder):
    responder.display_web_view(url='some-url')
    assert responder.directives[0]['name'] == 'display-web-view'
    assert responder.directives[0]['payload']['url'] == 'some-url'
    assert responder.directives[0]['type'] == 'action'


def test_ui_hints(responder: AssistantDialogueResponder):
    responder.ui_hints(['go back', 'see more'], prompt='speak carefully', display_immediately=True)
    assert responder.directives[0]['name'] == 'ui-hint'
    assert responder.directives[0]['payload']['text'] == ['go back', 'see more']
    assert responder.directives[0]['payload']['prompt'] == 'speak carefully'
    assert responder.directives[0]['payload']['displayImmediately']
    assert responder.directives[0]['type'] == 'view'


def test_asr_hints(responder: AssistantDialogueResponder):
    responder.asr_hints(['go back', 'see more'])
    assert responder.directives[0]['name'] == 'asr-hint'
    assert responder.directives[0]['payload']['text'] == ['go back', 'see more']
    assert responder.directives[0]['type'] == 'action'


@pytest.mark.parametrize(
    "query, remove_hyphens, text",
    [
        ("is this room open for an hour", False, "is this room open for an hour"),
        ("spark-assistant", True, "spark assistant"),
        ("spark-assistant", False, "spark-assistant"),
        ("speak-to webex-assistant", True, "speak to webex assistant"),
    ],
)
def test_reply(responder: AssistantDialogueResponder, query: str, remove_hyphens: bool, text: str):
    responder.reply(query, is_spoken=True, remove_hyphens=remove_hyphens)
    assert responder.directives[0]['payload']['text'] == query
    assert responder.directives[0]['name'] == 'reply'
    assert responder.directives[0]['type'] == 'view'
    assert responder.directives[1]['payload']['text'] == text
    assert responder.directives[1]['name'] == 'speak'
    assert responder.directives[1]['type'] == 'action'


def test_reply_incrementing_group(responder: AssistantDialogueResponder):
    responder.reply('hello', increment_group=True, is_spoken=False)
    responder.reply('world', increment_group=True, is_spoken=False)
    assert responder.directives[0]['payload']['text'] == 'hello'
    assert responder.directives[0]['payload']['group'] == 1
    assert responder.directives[0]['name'] == 'reply'
    assert responder.directives[0]['type'] == 'view'
    assert responder.directives[1]['payload']['text'] == 'world'
    assert responder.directives[1]['payload']['group'] == 2
    assert responder.directives[1]['name'] == 'reply'
    assert responder.directives[1]['type'] == 'view'
    with pytest.raises(DirectiveFormatError) as ex:
        responder.reply('again', increment_group=True, is_spoken=False)
    assert 'reply directive can only support two groups.' in str(ex)


@pytest.mark.parametrize(
    "query, remove_hyphens, text",
    [
        ("is this room open for an hour", False, "is this room open for an hour"),
        ("spark-assistant", True, "spark assistant"),
        ("spark-assistant", False, "spark-assistant"),
        ("speak-to webex-assistant", True, "speak to webex assistant"),
    ],
)
def test_long_reply(
    responder: AssistantDialogueResponder, query: str, remove_hyphens: bool, text: str
):
    responder.long_reply(query, is_spoken=True, remove_hyphens=remove_hyphens)
    assert responder.directives[0]['payload']['text'] == query
    assert responder.directives[0]['name'] == 'long-reply'
    assert responder.directives[0]['type'] == 'view'
    assert responder.directives[1]['payload']['text'] == text
    assert responder.directives[1]['name'] == 'speak'
