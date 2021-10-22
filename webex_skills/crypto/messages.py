import base64
import binascii
from typing import cast

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from ..exceptions import EncryptionKeyError
from .signatures import sign_token


def encrypt_fernet_key(fernet_key: bytes, pub_key: bytes) -> bytes:
    """Encrypts a fernet key with an RSA private key"""
    padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    public_key = cast(RSAPublicKey, serialization.load_pem_public_key(pub_key))
    return public_key.encrypt(fernet_key, padding)


def generate_token(message: str, pub_key: str) -> str:
    # Encode our message and keys to bytes up front so it's clear what we're working with
    pub_key_bytes = pub_key.encode('utf-8')
    message_bytes = message.encode('utf-8')

    # Generate a temporary fernet key, essentially two 128 bit AES keys mushed together
    fernet_key = Fernet.generate_key()

    # Encrypt our fernet key with our RSA public key
    encrypted_fernet_key = encrypt_fernet_key(fernet_key, pub_key_bytes)

    # Encrypt our message using the temporary encryption key
    encrypted_message = Fernet(fernet_key).encrypt(message_bytes)

    # Format our key/message combo for transmitting over the wire. b64encode the bytes then
    # encode the base64 as a utf-8 string
    encoded_fernet_key = base64.b64encode(encrypted_fernet_key).decode('utf-8')
    encoded_message = base64.b64encode(encrypted_message).decode('utf-8')

    # Our final token format is a string of base64 bytes representing
    # our key/message, delineated by a '.'
    return f'{encoded_fernet_key}.{encoded_message}'


def prepare_payload(message: str, pub_key: str, secret: str) -> dict:
    token = generate_token(message, pub_key)
    signature = sign_token(token, secret)

    return {
        'signature': signature,
        'message': token,
    }


def decrypt(private_key: RSAPrivateKey, message: bytes) -> bytes:

    padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)

    encrypted_fernet_key, fernet_token = message.split(b".")
    encrypted_fernet_key_bytes = base64.b64decode(encrypted_fernet_key)

    fernet_key = private_key.decrypt(encrypted_fernet_key_bytes, padding)

    fernet_token_bytes = base64.b64decode(fernet_token)
    payload = Fernet(fernet_key).decrypt(fernet_token_bytes)
    return payload


def load_private_key(private_key_bytes: bytes):
    """Loads a private key in PEM format"""
    try:
        private_key: RSAPrivateKey = load_pem_private_key(private_key_bytes, None)
        return private_key
    except (binascii.Error, ValueError, UnsupportedAlgorithm) as ex:
        raise EncryptionKeyError('Unable to load private key') from ex
