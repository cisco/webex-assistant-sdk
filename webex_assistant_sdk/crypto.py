import binascii

from cryptography.exceptions import UnsupportedAlgorithm, InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric import padding


class EncryptionKeyError(Exception):
    pass


def encrypt(message: str, public_key) -> str:
    """Encrypts a message using the given public key"""
    return public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
        ),
    ).hex()


def decrypt(cipher_hex: str, private_key) -> str:
    """Decrypes a cypher using the given private key"""
    return private_key.decrypt(
        bytes.fromhex(cipher_hex),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
        ),
    ).decode('utf-8')


def load_private_key(data, password=None):
    """Loads a private key in PEM format"""
    try:
        private_key = serialization.load_pem_private_key(
            data, password=password, backend=default_backend()
        )
        return private_key
    except (binascii.Error, ValueError, UnsupportedAlgorithm) as ex:
        raise EncryptionKeyError('Unable to load private key') from ex


def load_public_key(data):
    """Loads a public key in OpenSSH format"""
    try:
        return serialization.load_ssh_public_key(data, backend=default_backend())
    except (binascii.Error, ValueError, UnsupportedAlgorithm) as ex:
        raise EncryptionKeyError('Unable to load public key') from ex


def _generate_hmac(secret: str, message: str) -> hmac.HMAC:
    h: hmac.HMAC = hmac.HMAC(secret.encode('utf-8'), hashes.SHA256(), backend=default_backend())
    h.update(message.encode('utf-8'))
    return h


def generate_signature(secret: str, message: str) -> str:
    """Generates a message authentication code
    Args:
        secret (str): The secret used to sign the message
        message (str): The message to be signed
    Returns:
        str: the signature
    """
    h: hmac.HMAC = _generate_hmac(secret, message)
    return h.finalize().hex()


def verify_signature(secret: str, message: str, signature: str) -> bool:
    """Verifies a message authentication code
    Args:
        secret (str): The secret used to verify the signature
        message (str): The message which was signed
        signature (str): The signature to verify
    Returns:
        bool: True if the signature is valid
    """
    h: hmac.HMAC = _generate_hmac(secret, message)
    try:
        h.verify(bytes.fromhex(signature))
    except InvalidSignature:
        return False

    return True

