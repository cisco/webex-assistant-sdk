import base64
import json
import os

from aiohttp import web

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.serialization import load_ssh_private_key


DEV_MODE = os.getenv('ECHO_RUN_DEV_MODE', False)
PRIVATE_KEY = os.getenv('ECHO_PRIVATE_KEY')
SECRET = os.getenv('ECHO_SECRET')


routes = web.RouteTableDef()


def decrypt(message: bytes):
    # We expect our message to be a base64 encoded byte string of our cipher text
    key_bytes = PRIVATE_KEY.encode('utf-8')
    private_key = load_ssh_private_key(key_bytes, None)
    padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()),
                   algorithm=hashes.SHA256(), label=None)
    return private_key.decrypt(message, padding)


def verify_signature(message: bytes, signature: bytes):
    secret_bytes = SECRET.encode('utf-8')
    _hmac = hmac.HMAC(secret_bytes, hashes.SHA256())
    _hmac.update(message)
    _hmac.verify(signature)


def directive(name: str, dtype: str, payload: dict = None) -> dict:
    return {
        'name': name,
        'type': dtype,
        'payload': payload or {}
    }


def build_response(text: str, challenge: str, should_listen: bool = False) -> dict:
    response = {
        'directives': [
            directive('reply', 'view', {'text': text}),
            directive('speak', 'action', {'text': text}),
            directive('listen' if should_listen else 'sleep', 'action')
        ]
    }

    if not DEV_MODE:
        response['challenge'] = challenge

    return response


def handle_message(req_body: dict):
    should_listen = False
    if req_body.get('params', {}).get('target_dialogue_state') == 'skill_intro':
        text = 'This is the echo skill. Say something and I will echo it back.'
        should_listen = True
    else:
        text = req_body.get('text', ["Hmm... I didn't get anything to echo"])
        text = text[0]

    return build_response(text, req_body.get('challenge', ''), should_listen)


@routes.post('/')
async def echo(request: web.BaseRequest) -> web.Response:
    if DEV_MODE:
        req_body = await request.json()
    else:
        request_body: bytes = await request.json()

        # Our signature and cipher bytes are expected to be base64 encoded byte strings
        encoded_signature: str = request_body.get('signature')
        encoded_cipher: str = request_body.get('message')

        # Bail on missing signature
        if not encoded_signature:
            return web.json_response({"error": "Missing signature"}, 400)

        # And on a missing message
        if not encoded_cipher:
            return web.json_response({"error": "Missing message"}, 400)

        # Convert our encoded signature and body to bytes
        encoded_cipher_bytes: bytes = encoded_cipher.encode('utf-8')

        # We sign the encoded cipher text so we decode our signature, but not our cipher text yet
        decoded_sig_bytes: bytes = base64.b64decode(encoded_signature)

        try:
            # Cryptography's verify method throws rather than returning false..thanks jerks.
            verify_signature(encoded_cipher_bytes, decoded_sig_bytes)
        except InvalidSignature:
            return web.json_response({"error": "Invalid signature"}, 400)

        # Now that we've verified our signature we decode our cipher to get the raw bytes
        decoded_cipher = base64.b64decode(encoded_cipher_bytes)
        decrypted_body = decrypt(decoded_cipher)

        # The decrypted cipher text is a json string representing our MindMeld style message
        req_body = json.loads(decrypted_body)

    response = handle_message(req_body)
    return web.json_response(response)

app = web.Application()
app.add_routes(routes)
web.run_app(app)
