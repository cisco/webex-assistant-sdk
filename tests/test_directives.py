from typing import Any, Dict, Optional

from webex_skills.dialogue import responses


def assert_format(response: responses.SkillDirective, payload: Optional[Dict[str, Any]] = None):
    expected = {'name': response.name, 'type': response.type}
    if payload:
        expected['payload'] = payload
    assert response.dict() == expected


def test_reply():
    assert_format(responses.Reply('test'), {'text': 'test'})


def test_listen():
    assert_format(responses.Listen())


def test_speak():
    assert_format(responses.Speak('sup'), {'text': 'sup'})


def test_sleep():
    assert_format(responses.Sleep(10), {'delay': 10})
    assert_format(responses.Sleep(), {'delay': 0})


def test_display_webview():
    url = 'https://cisco.com'
    title = 'Cisco'
    assert_format(responses.DisplayWebView(url=url, title=title), {'url': url, 'title': title})


def test_clear_webview():
    assert_format(responses.ClearWebView())


def test_ui_hint():
    hints = ['hint1', 'hint2']
    prompt = 'try'

    expected = {'text': hints, 'prompt': prompt}
    assert_format(responses.UIHint(texts=hints, prompt=prompt), expected)


def test_ui_hint_no_prompt():
    hints = ['hint1', 'hint2']

    expected = {'text': hints}
    assert_format(responses.UIHint(texts=hints), expected)


def test_asr_hint():
    assert_format(responses.AsrHint(texts=['hint1', 'hint2']), {'text': ['hint1', 'hint2']})
