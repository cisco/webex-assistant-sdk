from webex_assistant_sdk.api import MindmeldAPI
from webex_assistant_sdk.dialogue import responses
from webex_assistant_sdk.models.mindmeld import DialogueState

api = MindmeldAPI()


@api.handle(intent='greet')
async def greet(current_state: DialogueState) -> DialogueState:
    text = 'Hello I am a super simple skill using NLP'
    new_state = current_state.copy()

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.Sleep(10),
    ]

    return new_state
