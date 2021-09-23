import json
import os
from pathlib import Path

from webex_assistant_sdk.app import SkillApplication
from webex_assistant_sdk.crypto import (
    generate_token,
    load_public_key_from_file,
    prepare_payload,
    sign_token,
)


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


def test_parse_endpoint_success(skill_app, client):
    test_request = {'text': 'hi', 'challenge': 'a challenge'}

    public_key = load_public_key_from_file(
        str(Path(__file__).resolve().parent / 'skill/id_rsa.pub')
    )
    payload = prepare_payload(json.dumps(test_request), public_key, skill_app.secret)
    response = client.post(
        '/parse',
        data=json.dumps(payload),
        content_type='application/json',
        follow_redirects=True,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf8'))
    assert response_data['dialogue_state'] == 'welcome'
    assert response_data['challenge'] == 'a challenge'
    # Use >= set comparison as newer versions of mindmeld may add fields
    assert set(response_data.keys()) >= {
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


def test_health_endpoint(skill_app, client):
    challenge = os.urandom(32).hex()
    public_key = load_public_key_from_file(
        str(Path(__file__).resolve().parent / 'skill/id_rsa.pub')
    )
    token = generate_token(challenge, public_key)
    signature = sign_token(token, skill_app.secret)

    query_params = {
        'signature': signature,
        'message': token
    }
    response = client.get('/parse', query_string=query_params)
    assert response.status_code == 200
    resp_set = set(json.loads(response.data.decode('utf8')).keys())
    assert resp_set == {'api_version', 'challenge', 'status'}
