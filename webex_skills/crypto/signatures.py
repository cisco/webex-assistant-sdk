import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, hmac


def verify_signature(secret: bytes, message: bytes, signature: bytes) -> bool:
    sig = hmac.HMAC(secret, hashes.SHA256())
    sig.update(message)
    try:
        sig.verify(signature)
        return True
    except InvalidSignature:
        return False


def sign_token(message: str, secret: str) -> str:
    secret_bytes = secret.encode('utf-8')
    message_bytes = message.encode('utf-8')
    sig = hmac.HMAC(secret_bytes, hashes.SHA256())
    sig.update(message_bytes)
    sig_bytes = sig.finalize()
    return base64.b64encode(sig_bytes).decode('utf-8')
