import base64
import binascii

from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from webex_assistant_skills_sdk.shared.services import CryptoService as BaseCryptoService


class CryptoService(BaseCryptoService):
    def decrypt(private_key: RSAPrivateKey, message: bytes) -> bytes:
        padding = OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )

        encrypted_fernet_key, fernet_token = message.split(b".")
        encrypted_fernet_key_bytes = base64.b64decode(encrypted_fernet_key)

        fernet_key = private_key.decrypt(encrypted_fernet_key_bytes, padding)

        fernet_token_bytes = base64.b64decode(fernet_token)
        payload = Fernet(fernet_key).decrypt(fernet_token_bytes)

        return payload

    def load_private_key(self, private_key_bytes: bytes) -> str:
        """Loads a private key in PEM format"""
        try:
            return load_pem_private_key(private_key_bytes, None)
        except (binascii.Error, ValueError, UnsupportedAlgorithm) as e:
            # TODO: raise custom exception
            raise Exception('Unable to load private key') from e

    def verify_signature(secret: bytes, message: bytes, signature: bytes) -> bool:
        sig = hmac.HMAC(secret, hashes.SHA256())
        sig.update(message)

        try:
            sig.verify(signature)
            return True
        except InvalidSignature:
            return False
