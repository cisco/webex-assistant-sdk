import json
import os
import requests

from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP

PUBLIC_KEY = os.getenv('ECHO_PUBLIC_KEY')
SECRET = os.getenv('ECHO_SECRET')


def encrypt_payload(message: str, key: str) -> bytes:
    msg_bytes = message.encode('utf-8')
    key_bytes = key.encode('utf-8')

    padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    public_key = serialization.load_ssh_public_key(key_bytes)
    return public_key.encrypt(msg_bytes, padding)


def sign_message(message: bytes, secret: bytes) -> str:
    _hmac = hmac.HMAC(message, hashes.SHA256())
    _hmac.update(secret)
    signature = _hmac.finalize().hex()
    return signature


message_body = {
    "text": ["Hello world!"],
    "context": {},
    "params": {},
    "frame": {},
    "history": {}
}

encrypted_request = encrypt_payload(json.dumps(message_body), PUBLIC_KEY)

sig = sign_message(encrypted_request, SECRET.encode('utf-8'))
headers = {
    'X-Webex-Assistant-Signature': sig,
    'Content-Type': 'application/octet-stream',
    'Accept': 'application/json',
}

response = requests.post('http://0.0.0.0:8080/', headers=headers, data=encrypted_request)
print(response.json())
