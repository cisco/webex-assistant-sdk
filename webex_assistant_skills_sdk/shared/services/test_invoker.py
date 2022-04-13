from __future__ import annotations

from dependency_injector.wiring import Provide
from fastapi.testclient import TestClient
from fastapi import Response

from webex_assistant_skills_sdk.shared.models import DeviceContext
from webex_assistant_skills_sdk.shared.services.base_invoker import BaseInvoker
from webex_assistant_skills_sdk.shared.services.settings import Settings
from webex_assistant_skills_sdk.types import Types


class TestInvoker(BaseInvoker):
    _client = TestClient()
    _settings: Settings =  Provide[Types.SETTINGS]

    def __init__(
        self,
        device_context: DeviceContext = DeviceContext.construct_default_context(),
    ) -> None:
        super().__init__(
            device_context=device_context,
            use_encryption=False,
            url='/parse',
        )

    def post_request(self, request_json: str) -> Response:
        return self._client.post(self.url, data=request_json)
