import base64

import aiohttp
import asyncio
import json
import os

from typing import cast

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

PUBLIC_KEY = os.getenv('ECHO_PUBLIC_KEY')
SECRET = os.getenv('ECHO_SECRET')


def encrypt_fernet_key(fernet_key: bytes, pub_key: bytes) -> bytes:
    """Encrypts a fernet key with an RSA private key"""
    padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    public_key = cast(RSAPublicKey, serialization.load_ssh_public_key(pub_key))
    return public_key.encrypt(fernet_key, padding)


def generate_token(message: str, pub_key: str) -> str:
    # Encode our message and keys to bytes up front so it's clear what we're working with
    pub_key_bytes = pub_key.encode('utf-8')
    message_bytes = message.encode('utf-8')

    # Generate a temporary fernet key, essentially two 128 bit AES keys mushed together
    fernet_key = Fernet.generate_key()

    # Encrypt our fernet key with our RSA public key
    encrypted_fernet_key = encrypt_fernet_key(fernet_key, pub_key_bytes)

    # Encrypt our message using the temporary encryption key
    encrypted_message = Fernet(fernet_key).encrypt(message_bytes)

    # Format our key/message combo for transmitting over the wire. b64encode the bytes then
    # encode the base64 as a utf-8 string
    encoded_fernet_key = base64.b64encode(encrypted_fernet_key).decode('utf-8')
    encoded_message = base64.b64encode(encrypted_message).decode('utf-8')

    # Our final token format is a string of base64 bytes representing our key/message, delineated by a '.'
    return f'{encoded_fernet_key}.{encoded_message}'


def prepare_payload(message: str, pub_key: str, secret: str) -> dict:
    token = generate_token(message, pub_key)
    signature = sign_token(token, secret)

    return {
        'signature': signature,
        'message': token,
    }


def sign_token(message: str, secret: str) -> str:
    secret_bytes = secret.encode('utf-8')
    message_bytes = message.encode('utf-8')
    sig = hmac.HMAC(secret_bytes, hashes.SHA256())
    sig.update(message_bytes)
    sig_bytes = sig.finalize()
    return base64.b64encode(sig_bytes).decode('utf-8')


challenge = os.urandom(32).hex()
message_body = {
    "text": ["Hello world!"],
    "context": {},
    "params": {},
    "frame": {},
    "history": {},
    "challenge": challenge
}

request = prepare_payload(json.dumps(message_body), PUBLIC_KEY, SECRET)


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
