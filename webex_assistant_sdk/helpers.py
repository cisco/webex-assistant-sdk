import base64
import json
import logging
import os
from typing import Mapping, Tuple, Union

from cryptography.exceptions import InvalidSignature
import requests

from . import crypto
from .exceptions import (
    ClientChallengeValidationError,
    RequestValidationError,
    ResponseValidationError,
    ServerChallengeValidationError,
    SignatureValidationError,
)

logger = logging.getLogger(__name__)


def validate_request(
        secret: str,
        private_key: str,
        body: Union[str, bytes]) -> Tuple[Mapping, str]:
    """Validates a request to an agent

    Args:
        secret (str): The configured secret for the skill
        private_key (str): The private key for this skill
        body (str or bytes): The request body

    Returns:
        Tuple[Mapping, str]: The decrypted request body and a challenge string

    Raises:
        RequestValidationError: raised when request data cannot be decrypted or decoded
        ServerChallengeValidationError: raised when request is missing challenge
        SignatureValidationError: raised when signature cannot be validated
    """
    try:
        if not body:
            raise SignatureValidationError('Missing body')

        json_body = json.loads(body)

        encoded_signature = json_body.get('signature', '')
        encoded_cipher = json_body.get('message', '')
        if not encoded_signature:
            raise SignatureValidationError('Missing signature')
        if not encoded_cipher:
            raise SignatureValidationError('Missing message')

        # Convert our encoded signature and body to bytes
        encoded_cipher_bytes: bytes = encoded_cipher.encode("utf-8")

        # We sign the encoded cipher text so we decode our signature, but not our cipher text yet
        decoded_sig_bytes: bytes = base64.b64decode(encoded_signature)

        try:
            # Cryptography's verify method throws rather than returning false.
            crypto.verify_signature(secret, encoded_cipher_bytes, decoded_sig_bytes)
        except InvalidSignature as exc:
            raise SignatureValidationError('Invalid signature') from exc

        # Now that we've verified our signature we decode our cipher to get the raw bytes
        decrypted_body = crypto.decrypt(private_key, encoded_cipher)

        try:
            request_json = json.loads(decrypted_body)
        except json.JSONDecodeError as exc:
            raise RequestValidationError('Invalid request data') from exc

        challenge = request_json.get('challenge')
        if not challenge:
            raise ServerChallengeValidationError('Missing challenge')

    except RequestValidationError:
        raise
    except Exception as exc:
        logger.exception('Unexpected error validating request')
        raise RequestValidationError('Cannot validate request') from exc

    return request_json, challenge


def make_request(
    secret,
    public_key,
    text,
    url='http://0.0.0.0:7150/parse',
    context=None,
    params=None,
    frame=None,
    history=None,
):
    challenge = os.urandom(64).hex()

    context = context or {
        'orgId': 'fake-org-id',
        'userId': 'fake-user-id',
        'userType': 'fake',
        'supportedDirectives': ['reply', 'speak', 'display-web-view', 'sleep', 'listen'],
    }

    request = {
        k: v
        for k, v in {
            'challenge': challenge,
            'text': text,
            'context': context,
            'params': params,
            'frame': frame,
            'history': history,
        }.items()
        if v is not None
    }

    payload = crypto.prepare_payload(json.dumps(request), public_key, secret)

    res = requests.post(url, json=payload)

    if res.status_code != 200:
        raise ResponseValidationError('Request failed')

    response_body = res.json()

    if response_body.get('challenge') != challenge:
        raise ClientChallengeValidationError('Response failed challenge')

    return response_body


def make_health_check(secret, public_key, url='http://0.0.0.0:7150/parse'):
    challenge = os.urandom(32).hex()
    token = crypto.generate_token(challenge, public_key)
    signature = crypto.sign_token(token, secret)

    query_params = {
        'signature': signature,
        'message': token
    }
    res = requests.get(url, params=query_params)

    if res.status_code != 200:
        raise ResponseValidationError('Health check failed')

    json_resp = res.json()

    if json_resp.pop('challenge', None) != challenge:
        raise ClientChallengeValidationError('Response failed challenge')

    return json_resp
