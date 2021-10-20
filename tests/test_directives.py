from webex_assistant_sdk.dialogue.responses import Listen, Reply


def test_reply():
    assert Reply('test').dict() == {'name': 'reply', 'type': 'action', 'payload': {'text': 'test'}}


def test_listen():
    assert Listen().dict() == {'name': 'listen', 'type': 'action'}
