import json
import logging
import time
import uuid

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from flask import Flask, jsonify, request
from flask_cors import CORS
from mindmeld import DialogueResponder
from mindmeld.app_manager import ApplicationManager
from mindmeld.exceptions import BadMindMeldRequestError
from mindmeld.server import MindMeldRequest

from ._version import current as __version__
from .crypto import decrypt, verify_signature

logger = logging.getLogger(__name__)


def create_agent_server(
    app_manager: ApplicationManager, secret: str, private_key: RSAPrivateKey
) -> Flask:
    server = Flask('mindmeld')
    CORS(server)

    server.request_class = MindMeldRequest
    server._private_key = private_key
    server._secret = secret

    # pylint: disable=unused-variable
    @server.route('/parse', methods=['POST'])
    def parse():
        """The main endpoint for the MindMeld API"""
        start_time = time.time()
        signature = request.headers.get('X-Webex-Assistant-Signature')
        data = request.get_data().decode('utf-8')
        if not (signature and data):
            msg = "Invalid Request Signature or Data"
            raise BadMindMeldRequestError(msg, status_code=403)

        json_str = decrypt(data, private_key)
        if not verify_signature(secret, json_str, signature):
            msg = "Invalid Request Signature"
            raise BadMindMeldRequestError(msg, status_code=403)

        request_json = json.loads(json_str)
        if request_json is None:
            msg = "Invalid Content."
            raise BadMindMeldRequestError(msg, status_code=415)

        challenge = request_json.get('challenge')
        if not challenge:
            msg = 'Bad Request'
            raise BadMindMeldRequestError(msg, status_code=400)

        safe_request = {}
        for key in ['text', 'params', 'context', 'frame', 'history', 'verbose']:
            if key in request_json:
                safe_request[key] = request_json[key]

        response = app_manager.parse(**safe_request)
        # add request id to response
        # use the passed in id if any
        request_id = request_json.get('request_id', str(uuid.uuid4()))
        response.request_id = request_id
        response.response_time = time.time() - start_time
        response.challenge = challenge
        return jsonify(DialogueResponder.to_json(response))

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

    @server.route('/health', methods=['GET'])
    def status_check():
        body = {'status': 'OK', 'package_version': __version__}
        return jsonify(body)

    return server
