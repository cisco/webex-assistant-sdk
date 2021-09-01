import json
import os

from aiohttp import web
from cryptography.hazmat.primitives import hashes, hmac, serialization

DEV_MODE = os.getenv('ECHO_RUN_DEV_MODE', False)
PRIVATE_KEY = os.getenv('ECHO_PRIVATE_KEY')
SECRET = os.getenv('ECHO_SECRET')


routes = web.RouteTableDef()


def decrypt_body(body: str) -> dict:
    pass


def verify_signature(signature: str, body: dict) -> bool:
    _hmac = hmac.HMAC(json.dumps(body), hashes.SHA256())
    _hmac.update(SECRET)
    created_signature = _hmac.finalize().hex()
    return created_signature == signature


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
        req_body = await request.read()
        req_body = decrypt_body(req_body)
        signature = request.headers['X-Webex-Assistant-Signature']
        valid_signature = verify_signature(signature, req_body)
        if not valid_signature:
            return web.json_response({"message": "bad request"}, 400)

    response = handle_message(req_body)
    return web.json_response(response)

app = web.Application()
app.add_routes(routes)
web.run_app(app)
