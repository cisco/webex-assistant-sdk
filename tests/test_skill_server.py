import json

from webex_assistant_sdk import SkillApplication
from webex_assistant_sdk.crypto import generate_signature


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


def test_parse_endpoint_success(client):
    test_request = {'text': 'hi', 'challenge': 'a challenge'}

    secret = 'some secret'
    signature = generate_signature(secret, json.dumps(test_request))
    response = client.post(
        '/parse',
        data=json.dumps(test_request),
        content_type='application/json',
        headers={'X-Webex-Assistant-Signature': signature},
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


def test_health_endpoint(client):
    response = client.get('/parse')
    assert response.status_code == 200
    assert set(json.loads(response.data.decode('utf8')).keys()) == {'api_version', 'status'}
