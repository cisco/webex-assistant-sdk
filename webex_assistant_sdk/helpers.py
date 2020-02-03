import json
import logging
import os
from typing import Mapping, Tuple, Union

import requests

from . import crypto
from .exceptions import (
    ClientChallengeValidationError,
    EncryptionKeyError,
    RequestValidationError,
    ResponseValidationError,
    ServerChallengeValidationError,
    SignatureValidationError,
)

logger = logging.getLogger(__name__)


def validate_request(
    secret: str, private_key, headers: Mapping, body: Union[str, bytes]
) -> Tuple[Mapping, str]:
    """Validates a request to an agent

    Args:
        headers (Mapping): The request headers
        body (str or bytes): The request body
        secret (str): The configured secret for the skill
        private_key (TYPE): The configured private key for the skill

    Returns:
        Tuple[Mapping, str]: The decrypted request body and a challenge string

    Raises:
        RequestValidationError: Description
        ServerChallengeValidationError: Description
        SignatureValidationError: Description
    """
    try:
        signature = headers.get('X-Webex-Assistant-Signature')
        if not signature:
            raise SignatureValidationError('Missing signature')
        if not body:
            raise SignatureValidationError('Missing body')

        try:
            json_str = crypto.decrypt(private_key, body)
        except EncryptionKeyError as exc:
            raise RequestValidationError('Invalid payload encryption') from exc

        if not crypto.verify_signature(secret, json_str, signature):
            raise SignatureValidationError('Invalid signature')

        try:
            request_json = json.loads(json_str)
        except json.JSONDecodeError as exc:
            raise RequestValidationError('Invalid request data') from exc

        challenge = request_json.get('challenge')
        if not challenge:
            raise ServerChallengeValidationError('Bad request')

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

    encoded_request = json.dumps(request)
    encrypted_request = crypto.encrypt(public_key, encoded_request)

    headers = {
        'X-Webex-Assistant-Signature': crypto.generate_signature(secret, encoded_request),
        'Content-Type': 'application/octet-stream',
        'Accept': 'application/json',
    }
    res = requests.post(url, headers=headers, data=encrypted_request)

    if res.status_code != 200:
        raise ResponseValidationError('Request failed')

    response_body = res.json()

    if response_body.get('challenge') != challenge:
        raise ClientChallengeValidationError('Response failed challenge')

    return res.json()
