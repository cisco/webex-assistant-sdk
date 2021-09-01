from aiohttp import web

routes = web.RouteTableDef()


def directive(name: str, dtype: str, payload: dict = None) -> dict:
    return {
        'name': name,
        'type': dtype,
        'payload': payload or {}
    }


def build_response(text: str, should_listen: bool = False) -> dict:
    return {
        'directives': [
            directive('reply', 'view', {'text': text}),
            directive('speak', 'action', {'text': text}),
            directive('listen' if should_listen else 'sleep', 'action')
        ]
    }


def handle_message(req_body: dict):
    should_listen = False
    if req_body.get('params', {}).get('target_dialogue_state') == 'skill_intro':
        text = 'This is the echo skill. Say something and I will echo it back.'
        should_listen = True
    else:
        text = req_body.get('text', ["Hmm... I didn't get anything to echo"])
        text = text[0]

    return build_response(text, should_listen)


@routes.post('/')
async def echo(request: web.BaseRequest) -> web.Response:
    req_body = await request.json()
    response = handle_message(req_body)
    return web.json_response(response)

app = web.Application()
app.add_routes(routes)
web.run_app(app)
