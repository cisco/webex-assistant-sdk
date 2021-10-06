import base64
import json

import pytest

from webex_assistant_sdk.crypto import sign_token, verify_signature


@pytest.fixture(scope='session', name='temp_dir')
def _temp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("tmp")


def test_signatures():
    secret = b'top secret'
    message = json.dumps({'hello': 'this is a message'})

    signature = sign_token(message, secret.decode('utf-8'))
    try:
        verify_signature(secret, message.encode('utf-8'), base64.b64decode(signature))
    except Exception as exc:  # pylint:disable=broad-except
        pytest.fail(f"Signature mismatch: {exc}")
