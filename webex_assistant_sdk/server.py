import json
import logging
import time
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from mindmeld import DialogueResponder
from mindmeld.app_manager import ApplicationManager
from mindmeld.exceptions import BadMindMeldRequestError
from mindmeld.server import MindMeldRequest

from ._version import api_version
from .exceptions import (
    RequestValidationError,
    ServerChallengeValidationError,
    SignatureValidationError,
)
from .helpers import validate_request

logger = logging.getLogger(__name__)


def create_skill_server(app_manager: ApplicationManager, secret: str) -> Flask:
    server = Flask('mindmeld')
    CORS(server)

    server.request_class = MindMeldRequest
    server._secret = secret

    # pylint: disable=unused-variable
    @server.route('/parse', methods=['POST'])
    def parse():
        """The main endpoint for the skill API"""

        start_time = time.time()
        try:
            request_json, challenge = validate_request(
                secret, request.headers, request.get_data().decode('utf-8')
            )
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
        response = {'status': 'up', 'api_version': '.'.join((str(i) for i in api_version))}
        return jsonify(response)

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
