from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, hmac

from webex_assistant_sdk.exceptions import SignatureGenerationError


def _generate_hmac(secret: str, message: str) -> hmac.HMAC:
    h: hmac.HMAC = hmac.HMAC(secret.encode('utf-8'), hashes.SHA256())
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
