import base64
import binascii

from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_ssh_private_key

from webex_assistant_sdk.exceptions import EncryptionKeyError, SignatureGenerationError


def decrypt(private_key: RSAPrivateKey, message: str) -> str:
    padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()),
                   algorithm=hashes.SHA256(), label=None)

    encrypted_fernet_key, fernet_token = message.split(".")
    encrypted_fernet_key_bytes = base64.b64decode(
        encrypted_fernet_key.encode("utf-8"))

    fernet_key = private_key.decrypt(encrypted_fernet_key_bytes, padding)

    fernet_token_bytes = base64.b64decode(fernet_token)
    payload = Fernet(fernet_key).decrypt(fernet_token_bytes)
    return payload.decode("utf-8")


def verify_signature(secret: str, message: bytes, signature: bytes) -> None:
    secret_bytes = secret.encode("utf-8")

    sig = hmac.HMAC(secret_bytes, hashes.SHA256())
    sig.update(message)
    sig.verify(signature)


def load_private_key(private_key_bytes: bytes):
    """Loads a private key in PEM format"""
    try:
        private_key: RSAPrivateKey = load_ssh_private_key(private_key_bytes, None)
        return private_key
    except (binascii.Error, ValueError, UnsupportedAlgorithm) as ex:
        raise EncryptionKeyError('Unable to load private key') from ex


def get_file_contents(filename: str) -> bytes:
    with open(filename, 'rb') as f:
        data = f.read()
    return data


def load_private_key_from_file(filename: str):
    key_data = get_file_contents(filename)
    private_key = load_private_key(key_data)
    return private_key
