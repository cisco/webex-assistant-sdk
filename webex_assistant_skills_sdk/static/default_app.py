from webex_assistant_skills_sdk.api import SimpleAPI
from webex_assistant_skills_sdk.dialogue import responses
from webex_assistant_skills_sdk.models.mindmeld import DialogueState

api = SimpleAPI()


@api.handle(default=True)
async def greet(current_state: DialogueState) -> DialogueState:
    text = 'Hello I am a super simple skill'
    new_state = current_state.copy()

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.Sleep(10),
    ]

    return new_state
