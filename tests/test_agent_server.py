import json
import os

from webex_assistant_sdk import AgentApplication
from webex_assistant_sdk.crypto import (
    encrypt,
    generate_signature,
    get_file_contents,
    load_public_key,
)


def test_agent_key(agent_app: AgentApplication):
    assert agent_app.private_key
    assert agent_app._server._private_key


def test_parse_endpoint_fail(client):
    test_request = {'text': 'hi'}
    response = client.post(
        '/parse',
        data=json.dumps(test_request),
        content_type='application/json',
        follow_redirects=True,
    )
    assert response.status_code == 403

    response = client.post('/parse')
    assert response.status_code == 403


def test_parse_endpoint_success(client, agent_dir):
    test_request = {'text': 'hi', 'challenge': 'a challenge'}

    key = load_public_key(get_file_contents(os.path.join(agent_dir, 'id_rsa.pub')))
    secret = 'some secret'
    encrypted_msg = encrypt(message=json.dumps(test_request), public_key=key)
    signature = generate_signature(secret, json.dumps(test_request))
    response = client.post(
        '/parse',
        data=encrypted_msg,
        content_type='text',
        headers={'X-Webex-Assistant-Signature': signature},
        follow_redirects=True,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf8'))
    assert response_data['dialogue_state'] == 'welcome'
    assert response_data['challenge'] == 'a challenge'
    assert set(response_data.keys()) == {
        'history',
        'params',
        'frame',
        'dialogue_state',
        'request_id',
        'response_time',
        'request',
        'directives',
        'slots',
        'challenge',
    }


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert set(json.loads(response.data.decode('utf8')).keys()) == {'package_version', 'status'}
