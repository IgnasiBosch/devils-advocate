from typing import Optional

from fastapi import Request
from fastapi.security import OAuth2
from fastapi.openapi.models import (
    OAuthFlows as OAuthFlowsModel,
    OAuthFlowImplicit,
    OAuthFlowPassword,
    OAuthFlowClientCredentials,
)


class UserSession(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowClientCredentials(
            password={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        pass


# oauth2_scheme = UserSession(tokenUrl="/token")
