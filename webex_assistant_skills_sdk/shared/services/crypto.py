import base64
from typing import cast

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from webex_assistant_skills_sdk.shared.models import EncryptedPayload


class CryptoService():
    def prepare_payload(self, payload: str, public_key: str, secret: str) -> EncryptedPayload:
        token = self.__generate_token(payload, public_key)
        signature = self.__sign_token(token, secret)

        return EncryptedPayload(
            signature=signature,
            message=token,
        )

    def __encrypt_fernet_key(self, fernet_key: bytes, public_key: bytes) -> bytes:
        """Encrypts a fernet key with an RSA private key"""
        padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)

        public_key = cast(RSAPublicKey, serialization.load_pem_public_key(public_key))

        return public_key.encrypt(fernet_key, padding)

    def __generate_token(self, payload: str, public_key: str) -> str:
         # Encode our message and keys to bytes up front so it's clear what we're working with
        pub_key_bytes = public_key.encode('utf-8')
        message_bytes = payload.encode('utf-8')

        # Generate a temporary fernet key, essentially two 128 bit AES keys mushed together
        fernet_key = Fernet.generate_key()

        # Encrypt our fernet key with our RSA public key
        encrypted_fernet_key = self.__encrypt_fernet_key(fernet_key, pub_key_bytes)

        # Encrypt our message using the temporary encryption key
        encrypted_message = Fernet(fernet_key).encrypt(message_bytes)

        # Format our key/message combo for transmitting over the wire. b64encode the bytes then
        # encode the base64 as a utf-8 string
        encoded_fernet_key = base64.b64encode(encrypted_fernet_key).decode('utf-8')
        encoded_message = base64.b64encode(encrypted_message).decode('utf-8')

        # Our final token format is a string of base64 bytes representing
        # our key/message, delineated by a '.'
        return f'{encoded_fernet_key}.{encoded_message}'

    def __sign_token(self, token: str, secret: str) -> str:
        secret_bytes = secret.encode('utf-8')
        message_bytes = token.encode('utf-8')

        signature = hmac.HMAC(secret_bytes, hashes.SHA256())
        signature.update(message_bytes)
        signature_bytes = signature.finalize()

        return base64.b64encode(signature_bytes).decode('utf-8')
