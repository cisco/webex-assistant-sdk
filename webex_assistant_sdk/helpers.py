import json
import logging
import os
from typing import Mapping, Tuple, Union

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


def validate_request(secret: str, headers: Mapping, body: Union[str, bytes]) -> Tuple[Mapping, str]:
    """Validates a request to an agent

    Args:
        headers (Mapping): The request headers
        body (str or bytes): The request body
        secret (str): The configured secret for the skill

    Returns:
        Tuple[Mapping, str]: The decrypted request body and a challenge string

    Raises:
        RequestValidationError: raised when request data cannot be decrypted or decoded
        ServerChallengeValidationError: raised when request is missing challenge
        SignatureValidationError: raised when signature cannot be validated
    """
    try:
        signature = headers.get('X-Webex-Assistant-Signature')
        if not signature:
            raise SignatureValidationError('Missing signature')
        if not body:
            raise SignatureValidationError('Missing body')

        if not crypto.verify_signature(secret, body, signature):
            raise SignatureValidationError('Invalid signature')

        try:
            request_json = json.loads(body)
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

    headers = {
        'X-Webex-Assistant-Signature': crypto.generate_signature(secret, encoded_request),
        'Content-Type': 'application/octet-stream',
        'Accept': 'application/json',
    }
    res = requests.post(url, headers=headers, data=encoded_request)

    if res.status_code != 200:
        raise ResponseValidationError('Request failed')

    response_body = res.json()

    if response_body.get('challenge') != challenge:
        raise ClientChallengeValidationError('Response failed challenge')

    return response_body


def make_health_check(secret, url='http://0.0.0.0:7150/parse'):
    challenge = os.urandom(64).hex()
    headers = {
        'X-Webex-Assistant-Signature': crypto.generate_signature(secret, challenge),
        'Accept': 'application/json',
    }
    res = requests.get(url, headers=headers, params={'payload': challenge})

    if res.status_code != 200:
        raise ResponseValidationError('Health check failed')

    response_body = res.json()

    if response_body.get('challenge') != challenge:
        raise ClientChallengeValidationError('Response failed challenge')

    return response_body
