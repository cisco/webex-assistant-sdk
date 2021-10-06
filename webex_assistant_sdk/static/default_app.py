from webex_assistant_sdk.api import API
from webex_assistant_sdk.models.http import SkillInvokeRequest, SkillInvokeResponse

api = API()


@api.post('/parse')
def parse_things(invoke_request: SkillInvokeRequest) -> SkillInvokeResponse:
    directives = [
        {'name': 'reply', 'type': 'view', 'payload': {'text': invoke_request.text}},
        {'name': 'speak', 'type': 'action', 'payload': {'text': invoke_request.text}},
        {'name': 'sleep', 'type': 'action', 'payload': {}},
    ]
    return SkillInvokeResponse(challenge=invoke_request.challenge, directives=directives)
