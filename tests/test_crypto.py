import json

import pytest

from webex_assistant_sdk.crypto import (
    SignatureGenerationError,
    generate_signature,
    verify_signature,
)


@pytest.fixture(scope='session', name='temp_dir')
def _temp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("tmp")


def test_signatures():
    secret = 'top secret'
    message = json.dumps({'hello': 'this is a message'})

    signature = generate_signature(secret, message)
    assert verify_signature(secret, message, signature)

    with pytest.raises(SignatureGenerationError):
        generate_signature('', message)

    with pytest.raises(SignatureGenerationError):
        generate_signature(secret, '')
