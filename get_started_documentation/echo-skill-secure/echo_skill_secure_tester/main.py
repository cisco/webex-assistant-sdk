import base64

import aiohttp
import asyncio
import json
import os

from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP

PUBLIC_KEY = os.getenv('ECHO_PUBLIC_KEY')
SECRET = os.getenv('ECHO_SECRET')


def encrypt_payload(message: bytes, key: bytes) -> bytes:
    padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    public_key = serialization.load_ssh_public_key(key)
    return public_key.encrypt(message, padding)


def sign_message(message: bytes, secret: bytes) -> bytes:
    _hmac = hmac.HMAC(secret, hashes.SHA256())
    _hmac.update(message)
    return _hmac.finalize()


challenge = os.urandom(32).hex()
message_body = {
    "text": ["Hello world!"],
    "context": {},
    "params": {},
    "frame": {},
    "history": {},
    "challenge": challenge
}

encrypted_message = encrypt_payload(json.dumps(message_body).encode('utf-8'), PUBLIC_KEY.encode('utf-8'))
encoded_message = base64.b64encode(encrypted_message)

sig = sign_message(encoded_message, SECRET.encode('utf-8'))
encoded_sig = base64.b64encode(sig)
request = {
    'signature': encoded_sig.decode('utf-8'),
    'message': encoded_message.decode('utf-8')
}


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://0.0.0.0:8080/', json=request) as resp:
            print(f'Status: {resp.status}')
            response = await resp.json()
            pretty_response = json.dumps(response, indent=4)
            print(f'Response:\n{pretty_response}')

            assert challenge == response['challenge']


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
