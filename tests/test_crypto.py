import binascii
import json
import os
from unittest.mock import patch

from cryptography.exceptions import UnsupportedAlgorithm
import pytest

from webex_assistant_sdk.crypto import (
    EncryptionKeyError,
    SignatureGenerationError,
    decrypt,
    encrypt,
    generate_signature,
    get_file_contents,
    load_private_key,
    load_public_key,
    verify_signature,
)

KEYS = [
    'id_rsa',
    'id_rsa.encrypted',
    # ED25519 is inconsistently supported
    # we often fail to load keys not generated using python's cryptography module
    # 'id_ed25519',
    # 'id_ed25519.encrypted',
]


@pytest.mark.parametrize('key_type', KEYS)
def test_load_private_key(key_type, keys_dir, passphrase):
    key_data = get_file_contents(os.path.join(keys_dir, key_type))
    password = passphrase if key_type.endswith('.encrypted') else None
    private_key = load_private_key(key_data, password=password)

    assert private_key


@pytest.mark.parametrize('key_type', KEYS)
def test_load_public_key(key_type, keys_dir):
    key_data = get_file_contents(os.path.join(keys_dir, f'{key_type}.pub'))
    public_key = load_public_key(key_data)

    assert public_key


@pytest.mark.parametrize('exc_type', (ValueError, UnsupportedAlgorithm, binascii.Error))
def test_load_private_key_negative(exc_type):
    with patch(
        'cryptography.hazmat.primitives.serialization.load_pem_private_key',
        side_effect=exc_type('some error'),
    ):
        with pytest.raises(EncryptionKeyError):
            load_private_key(b'not a private key')


@pytest.mark.parametrize('exc_type', (ValueError, UnsupportedAlgorithm, binascii.Error))
def test_load_public_key_negative(exc_type):
    with patch(
        'cryptography.hazmat.primitives.serialization.load_ssh_public_key',
        side_effect=exc_type('some error'),
    ):
        with pytest.raises(EncryptionKeyError):
            load_public_key(b'not a public key')


@pytest.fixture(name='private_key')
def _private_key(keys_dir):
    key_data = get_file_contents(os.path.join(keys_dir, 'id_rsa'))
    private_key = load_private_key(key_data)
    return private_key


@pytest.fixture(name='public_key')
def _public_key(keys_dir):
    key_data = get_file_contents(os.path.join(keys_dir, 'id_rsa.pub'))
    public_key = load_public_key(key_data)
    return public_key


def test_asymmetric_encryption(public_key, private_key):
    message = 'hello'
    cipher_text = encrypt(message, public_key)

    assert isinstance(cipher_text, str)

    decrypted = decrypt(cipher_text, private_key)

    assert message != cipher_text
    assert message == decrypted


def test_signatures():
    secret = 'top secret'
    message = json.dumps({'hello': 'this is a message'})

    signature = generate_signature(secret, message)
    assert verify_signature(secret, message, signature)

    with pytest.raises(SignatureGenerationError):
        generate_signature('', message)

    with pytest.raises(SignatureGenerationError):
        generate_signature(secret, '')
