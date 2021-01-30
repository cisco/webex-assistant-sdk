import json
import os
from urllib.request import quote

from webex_assistant_sdk import SkillApplication
from webex_assistant_sdk.crypto import (
    encrypt,
    generate_signature,
    get_file_contents,
    load_public_key,
)


def test_skill_key(skill_app: SkillApplication):
    assert skill_app.private_key
    assert skill_app._server._private_key


def test_skill_intro(skill_app: SkillApplication):
    response = skill_app.app_manager.parse('', params={'target_dialogue_state': 'skill_intro'})
    assert response.dialogue_state == 'skill_intro'


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


def test_parse_endpoint_success(client, skill_dir):
    test_request = {'text': 'hi', 'challenge': 'a challenge'}

    key = load_public_key(get_file_contents(os.path.join(skill_dir, 'id_rsa.pub')))
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
    response = client.get('/parse')
    assert response.status_code == 200
    assert set(json.loads(response.data.decode('utf8')).keys()) == {'api_version', 'status'}


def test_health_endpoint_check(client, skill_dir):
    key = load_public_key(get_file_contents(os.path.join(skill_dir, 'id_rsa.pub')))
    secret = 'some secret'
    challenge = 'challenge'
    encrypted_challenge = encrypt(message=challenge, public_key=key)
    signature = generate_signature(secret, challenge)
    response = client.get(
        f'/parse?challenge={quote(encrypted_challenge)}',
        headers={'X-Webex-Assistant-Signature': signature},
    )

    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf8'))

    assert response_data == {
        'status': 'up',
        'api_version': '1.0',
        'validated': True,
        'challenge': challenge,
    }


def test_health_endpoint_check_failed(client, skill_dir):
    key = load_public_key(get_file_contents(os.path.join(skill_dir, 'id_rsa.pub')))
    secret = 'wrong secret'
    challenge = 'challenge'
    encrypted_challenge = encrypt(message=challenge, public_key=key)
    signature = generate_signature(secret, challenge)
    response = client.get(
        f'/parse?challenge={quote(encrypted_challenge)}',
        headers={'X-Webex-Assistant-Signature': signature},
    )

    assert response.status_code == 400
    response_data = json.loads(response.data.decode('utf8'))

    assert response_data == {'status': 'error', 'error': 'Invalid signature', 'api_version': '1.0'}
