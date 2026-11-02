from __future__ import annotations

import certifi

from typing import Any, cast

from sendmux_core import AccessToken, RetryOptions, configure_auth
from sendmux_core.auth import resolve_access_token, validate_auth
from sendmux_core.environment import env_value
from sendmux_core.errors import map_api_exception
from sendmux_core.retry import RetryingRestClient

from sendmux_mailbox.api_client import ApiClient
from sendmux_mailbox.configuration import Configuration
from sendmux_mailbox.exceptions import ApiException

DEFAULT_BASE_URL = "https://app.sendmux.ai/api/v1"


class SendmuxMailboxApiClient(ApiClient):
    def __init__(
        self,
        configuration: Configuration,
        *,
        access_token: AccessToken | None = None,
        retry_options: RetryOptions | None = None,
    ) -> None:
        configuration.retries = False
        super().__init__(configuration=configuration)
        self._access_token = access_token
        self.rest_client = cast(Any, RetryingRestClient(self.rest_client, retry_options=retry_options))

    def update_params_for_auth(
        self,
        headers: Any,
        queries: Any,
        auth_settings: Any,
        resource_path: Any,
        method: Any,
        body: Any,
        request_auth: Any = None,
    ) -> None:
        if (
            self._access_token is not None
            and any(name not in ("UploadTokenQubrics", "UploadTokenSendmux") for name in auth_settings or ())
            and not request_auth
        ):
            request_auth = {
                "type": "bearer",
                "in": "header",
                "key": "Authorization",
                "value": "Bearer " + resolve_access_token(self._access_token),
            }
        super().update_params_for_auth(
            headers, queries, auth_settings, resource_path, method, body, request_auth=request_auth,
        )

    def call_api(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return super().call_api(*args, **kwargs)
        except ApiException as exc:
            raise map_api_exception(exc) from exc

    def response_deserialize(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return super().response_deserialize(*args, **kwargs)
        except ApiException as exc:
            raise map_api_exception(exc) from exc


def create_mailbox_client(
    *,
    api_key: str | None = None,
    access_token: AccessToken | None = None,
    base_url: str | None = None,
    retry_options: RetryOptions | None = None,
) -> SendmuxMailboxApiClient:
    if api_key is None and access_token is None:
        api_key = env_value("SENDMUX_API_KEY")
        access_token = env_value("SENDMUX_ACCESS_TOKEN")
    validate_auth(api_key=api_key, access_token=access_token, surface="mailbox")
    configuration = Configuration(host=base_url or env_value("SENDMUX_BASE_URL") or DEFAULT_BASE_URL, ssl_ca_cert=certifi.where())
    if api_key is not None:
        configure_auth(configuration, api_key=api_key)
    return SendmuxMailboxApiClient(configuration, access_token=access_token, retry_options=retry_options)


configure_mailbox = create_mailbox_client
