from uuid import UUID
from dependency_injector.wiring import Provide

from webex_assistant_skills_sdk.cli.shared.services.config import ConfigService
from webex_assistant_skills_sdk.cli.types import Types
from webex_assistant_skills_sdk.shared.models import DeviceContext
from webex_assistant_skills_sdk.shared.services import Invoker


class CliInvoker(Invoker):
    __cli_config_service: ConfigService = Provide[Types.CONFIG_SERVICE]

    def __init__(
        self,
        skill_name: str,
        use_encryption: bool,
        org_id: UUID,
        user_id: UUID,
        device_id: UUID,
    ):
        skill_config = self.__cli_config_service.get_skill_config(skill_name)

        if skill_config is None:
            # TODO: custom exception
            raise Exception()

        super().__init__(
            url=skill_config.url,
            device_context=DeviceContext(
                org_id=org_id,
                user_id=user_id,
                device_developer_id=device_id,
                supported_directives=[],    # TODO: add default supported directives
            ),
            use_encryption=use_encryption,
            public_key=skill_config.public_key,
            secret=skill_config.secret,
        )
