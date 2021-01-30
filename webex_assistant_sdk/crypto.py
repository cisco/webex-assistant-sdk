import base64
import binascii
from typing import Optional, Sequence

from cryptography import fernet
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa

from .exceptions import EncryptionKeyError, SignatureGenerationError


def encrypt(public_key, message: str) -> str:
    """Encrypts a message using the given public key"""
    temp_key: bytes = fernet.Fernet.generate_key()
    cipher: fernet.Fernet = fernet.Fernet(temp_key)
    encrypted_temp_key: str = base64.b64encode(
        public_key.encrypt(
            temp_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
            ),
        )
    ).decode('utf-8')

    encrypted_message: str = cipher.encrypt(message.encode('utf-8')).decode('utf-8')
    return f'{encrypted_temp_key}.{encrypted_message}'


def decrypt(private_key, cipher_string: str) -> str:
    """Decrypes a cypher using the given private key"""
    encrypted_components: Sequence[str] = cipher_string.split('.')
    encrypted_temp_key: str = encrypted_components[0]
    # only the first '.' character is special -- we should treat the remainder as the content
    encrypted_message: str = '.'.join(encrypted_components[1:])
    try:
        decoded_temp_key = base64.b64decode(encrypted_temp_key.encode('utf-8'))
    except binascii.Error as exc:
        raise EncryptionKeyError('Message cannot be decoded') from exc
    pad = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
    )

    try:
        temp_key: bytes = private_key.decrypt(decoded_temp_key, pad)
    except ValueError as exc:
        raise EncryptionKeyError('Invalid key') from exc

    cipher: fernet.Fernet
    try:
        cipher = fernet.Fernet(temp_key)
    except (binascii.Error, ValueError) as exc:
        raise EncryptionKeyError('Invalid key') from exc
    return cipher.decrypt(encrypted_message.encode('utf-8')).decode('utf-8')


def load_private_key(data: bytes, password=None):
    """Loads a private key in PEM format"""
    try:
        private_key = serialization.load_pem_private_key(
            data, password=password, backend=default_backend()
        )
        return private_key
    except (binascii.Error, ValueError, UnsupportedAlgorithm) as ex:
        raise EncryptionKeyError('Unable to load private key') from ex


def get_file_contents(filename: str) -> bytes:
    with open(filename, 'rb') as f:
        data = f.read()
    return data


def load_private_key_from_file(filename: str, password: Optional[str] = None):
    key_data = get_file_contents(filename)
    private_key = load_private_key(key_data, password=password)
    return private_key


def load_public_key(data: bytes):
    """Loads a public key in OpenSSH format"""
    try:
        return serialization.load_ssh_public_key(data, backend=default_backend())
    except (binascii.Error, ValueError, UnsupportedAlgorithm) as ex:
        raise EncryptionKeyError('Unable to load public key') from ex


def load_public_key_from_file(filename: str):
    key_data: bytes = get_file_contents(filename)
    public_key = load_public_key(key_data)
    return public_key


def _generate_hmac(secret: str, message: str) -> hmac.HMAC:
    h: hmac.HMAC = hmac.HMAC(secret.encode('utf-8'), hashes.SHA256(), backend=default_backend())
    h.update(message.encode('utf-8'))
    return h


def generate_signature(secret: str, message: str) -> str:
    """Generates a message authentication code
    Args:
        secret (str): The secret used to sign the message.
        message (str): The message to be signed.
    Returns:
        str: The signature. If the secret or message is None return None.
    """
    if not (secret and message):
        raise SignatureGenerationError('The secret or message is not valid.')

    h: hmac.HMAC = _generate_hmac(secret, message)
    return h.finalize().hex()


def verify_signature(secret: str, message: str, signature: str) -> bool:
    """Verifies a message authentication code
    Args:
        secret (str): The secret used to verify the signature.
        message (str): The message which was signed.
        signature (str): The signature to verify.
    Returns:
        bool: True if the signature is valid and not None, False otherwise
    """
    if not signature:
        return False

    h: hmac.HMAC = _generate_hmac(secret, message)
    try:
        h.verify(bytes.fromhex(signature))
    except InvalidSignature:
        return False

    return True


def generate_keys(filename: str, key_type: str, password: Optional[str] = None):
    if key_type not in {'rsa', 'ed25519'}:
        raise ValueError(f"Invalid key type: {key_type}")

    if key_type == 'rsa':
        private_key = rsa.generate_private_key(65537, 4096, default_backend())
    else:
        private_key = ed25519.Ed25519PrivateKey.generate()

    if password:
        encryption = serialization.BestAvailableEncryption(password)
    else:
        encryption = serialization.NoEncryption()

    with open(filename, 'wb') as key_file:
        key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption,
            )
        )

    public_key = private_key.public_key()
    with open(f'{filename}.pub', 'wb') as key_file:
        key_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.OpenSSH, format=serialization.PublicFormat.OpenSSH
            )
        )
