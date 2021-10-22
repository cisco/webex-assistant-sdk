from pathlib import Path
import secrets
from typing import Optional, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, NoEncryption

EncryptionTypes = Union[BestAvailableEncryption, NoEncryption]


def generate_keys(priv_path: Path, pub_path: Path, encryption: Optional[EncryptionTypes] = None):

    if not encryption:
        encryption = NoEncryption()
    private_key = rsa.generate_private_key(65537, 4096)
    public_key: rsa.RSAPublicKey = private_key.public_key()

    priv_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption,
        )
    )

    pub_path.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )


def generate_secret():
    return secrets.token_urlsafe(16)
