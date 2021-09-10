import base64
import json
import logging
import os
import time
import uuid

from cryptography.exceptions import InvalidSignature
from flask import Flask, jsonify, request
from flask_cors import CORS
from mindmeld import DialogueResponder
from mindmeld.app_manager import ApplicationManager
from mindmeld.exceptions import BadMindMeldRequestError
from mindmeld.server import MindMeldRequest

from . import crypto
from ._version import api_version
from .exceptions import (
    RequestValidationError,
    ServerChallengeValidationError,
    SignatureValidationError,
)
from .helpers import validate_request

logger = logging.getLogger(__name__)


def create_skill_server(
        app_manager: ApplicationManager,
        secret: str,
        private_key: str) -> Flask:
    server = Flask('mindmeld')
    CORS(server)

    server.request_class = MindMeldRequest
    server._secret = secret
    server._private_key = private_key

    # pylint: disable=unused-variable
    @server.route('/parse', methods=['POST'])
    def parse():
        """The main endpoint for the skill API"""

        start_time = time.time()
        try:
            use_encryption = not os.environ.get('WXA_SKILL_DEBUG', False)
            if use_encryption:
                request_json, challenge = validate_request(
                    secret, private_key, request.get_data().decode('utf-8')
                )
            else:
                request_json = json.loads(request.data)
                challenge = None
        except SignatureValidationError as exc:
            raise BadMindMeldRequestError(exc.args[0], status_code=403) from exc
        except (RequestValidationError, ServerChallengeValidationError) as exc:
            raise BadMindMeldRequestError(exc.args[0], status_code=400) from exc

        safe_request = {}
        for key in ['text', 'params', 'context', 'frame', 'history', 'verbose']:
            if key in request_json:
                safe_request[key] = request_json[key]

        response = app_manager.parse(**safe_request)
        try:
            res = DialogueResponder.to_json(response)
        except AttributeError:
            res = dict(response)
        # add request id to response
        # use the passed in id if any
        request_id = request_json.get('request_id', str(uuid.uuid4()))
        res.update(
            {
                'request_id': request_id,
                'response_time': time.time() - start_time,
                'challenge': challenge,
            }
        )
        return res

    @server.route('/parse', methods=['GET'])
    def health_check():
        # Our signature and cipher bytes are expected to be base64 encoded byte strings
        encoded_signature: str = request.args.get("signature")
        encoded_cipher: str = request.args.get("message")

        # Bail on missing signature
        if not encoded_signature:
            return jsonify({"error": "Missing signature"}, 400)

        # And on a missing message
        if not encoded_cipher:
            return jsonify({"error": "Missing message"}, 400)

        # Convert our encoded signature and body to bytes
        encoded_cipher_bytes: bytes = encoded_cipher.encode("utf-8")

        # We sign the encoded cipher text so we decode our signature, but not our cipher text yet
        decoded_sig_bytes: bytes = base64.b64decode(encoded_signature)

        try:
            # Cryptography's verify method throws rather than returning false.
            crypto.verify_signature(secret, encoded_cipher_bytes, decoded_sig_bytes)
        except InvalidSignature:
            return jsonify({"error": "Invalid signature"}, 400)

        # Now that we've verified our signature we decode our cipher to get the raw bytes
        decrypted_challenge = crypto.decrypt(private_key, encoded_cipher)

        return jsonify(
            {
                'challenge': decrypted_challenge,
                'status': 'OK',
                'api_version': '.'.join((str(i) for i in api_version))
            }
        )

    # handle exceptions
    @server.errorhandler(BadMindMeldRequestError)
    def handle_bad_request(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        logger.error(json.dumps(error.to_dict()))
        return response

    @server.errorhandler(500)
    def handle_server_error(error):
        response_data = {'error': error.message}
        response = jsonify(response_data)
        response.status_code = 500
        logger.error(json.dumps(response_data))
        return response

    return server
