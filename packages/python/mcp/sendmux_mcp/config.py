from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal, Mapping, Sequence, cast, overload

from sendmux_core import validate_api_key

Surface = Literal["mailbox", "management", "sending"]
Transport = Literal["stdio", "http", "streamable-http"]
KeySurface = Literal["root", "mailbox", "sending"]

SURFACES: tuple[Surface, ...] = ("mailbox", "management", "sending")

DEFAULT_APP_BASE_URL = "https://app.sendmux.ai/api/v1"
DEFAULT_SENDING_BASE_URL = "https://smtp.sendmux.ai/api/v1"


@overload
def env_value(name: str, default: str) -> str: ...


@overload
def env_value(name: str, default: None = None) -> str | None: ...


def env_value(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name.replace("SENDMUX_", "QUBRICS_", 1))
    if value:
        return value
    return os.environ.get(name, default)


@dataclass(frozen=True)
class RetryConfig:
    max_attempts: int = 3
    base_delay_seconds: float = 0.25
    max_delay_seconds: float = 8.0
    max_elapsed_seconds: float | None = None


@dataclass(frozen=True)
class ServerConfig:
    surfaces: tuple[Surface, ...] = ("mailbox",)
    api_key: str | None = None
    api_keys: Mapping[Surface, str] = field(default_factory=dict)
    app_base_url: str = DEFAULT_APP_BASE_URL
    sending_base_url: str = DEFAULT_SENDING_BASE_URL
    transport: Transport = "stdio"
    host: str = "127.0.0.1"
    port: int = 8765
    path: str = "/mcp"
    openapi_input_dir: str | None = None
    app_openapi: str | None = None
    sending_openapi: str | None = None
    allowed_origins: tuple[str, ...] = ()
    http_bearer_token: str | None = None
    allow_unauthenticated_http: bool = False
    timeout_seconds: float = 30.0
    stateless_http: bool = True
    retry: RetryConfig = RetryConfig()

    @property
    def selected_surfaces(self) -> tuple[Surface, ...]:
        return normalise_surfaces(self.surfaces)

    @property
    def required_key_surface(self) -> KeySurface:
        return self.required_key_surface_for(self.only_surface())

    @staticmethod
    def required_key_surface_for(surface: Surface) -> KeySurface:
        if surface == "management":
            return "root"
        if surface == "sending":
            return "sending"
        return "mailbox"

    @property
    def api_base_url(self) -> str:
        return self.api_base_url_for(self.only_surface())

    def api_base_url_for(self, surface: Surface) -> str:
        return self.sending_base_url if surface == "sending" else self.app_base_url

    def api_key_for(self, surface: Surface) -> str | None:
        if surface in self.api_keys:
            return self.api_keys[surface]
        if surface == "sending" and "mailbox" in self.api_keys:
            return self.api_keys["mailbox"]
        return self.api_key

    def only_surface(self) -> Surface:
        surfaces = self.selected_surfaces
        if len(surfaces) != 1:
            raise ValueError("This operation requires exactly one selected surface.")
        return surfaces[0]

    def validate(self, *, require_api_key: bool = True) -> None:
        for surface in self.selected_surfaces:
            api_key = self.api_key_for(surface)
            if api_key:
                validate_api_key(api_key, surface=self.required_key_surface_for(surface))
            elif require_api_key:
                raise ValueError(
                    f"API key for {surface} is required. Set QUBRICS_{surface.upper()}_API_KEY"
                    " or QUBRICS_API_KEY for a single-key setup. SENDMUX_ names remain supported."
                )
        if self.transport in {"http", "streamable-http"} and not self.allow_unauthenticated_http:
            if not self.http_bearer_token:
                raise ValueError(
                    "HTTP transport requires QUBRICS_MCP_HTTP_BEARER_TOKEN (SENDMUX_MCP_HTTP_BEARER_TOKEN is also supported) or --allow-unauthenticated-http."
                )


def config_from_env(
    surfaces: Surface | Sequence[Surface] | None = None,
    *,
    api_key: str | None = None,
    require_api_key: bool = True,
) -> ServerConfig:
    transport = normalise_transport(env_value("SENDMUX_MCP_TRANSPORT", "stdio"))
    selected_surfaces = normalise_surfaces(
        surfaces if surfaces is not None else parse_surfaces(env_value("SENDMUX_MCP_SURFACES"), default=("mailbox",))
    )
    env_api_keys = surface_api_keys_from_env()
    retry_max_elapsed = env_value("SENDMUX_MCP_RETRY_MAX_ELAPSED_SECONDS")
    return ServerConfig(
        surfaces=selected_surfaces,
        api_key=api_key or env_value("SENDMUX_API_KEY") or None,
        api_keys=env_api_keys,
        app_base_url=env_value("SENDMUX_APP_BASE_URL", DEFAULT_APP_BASE_URL),
        sending_base_url=env_value("SENDMUX_SENDING_BASE_URL", DEFAULT_SENDING_BASE_URL),
        transport=transport,
        host=env_value("SENDMUX_MCP_HOST", "127.0.0.1"),
        port=int(env_value("SENDMUX_MCP_PORT", "8765")),
        path=env_value("SENDMUX_MCP_PATH", "/mcp"),
        openapi_input_dir=env_value("SENDMUX_MCP_OPENAPI_INPUT_DIR") or env_value("OPENAPI_INPUT_DIR"),
        app_openapi=env_value("SENDMUX_MCP_APP_OPENAPI"),
        sending_openapi=env_value("SENDMUX_MCP_SENDING_OPENAPI"),
        allowed_origins=parse_csv(env_value("SENDMUX_MCP_ALLOWED_ORIGINS")),
        http_bearer_token=env_value("SENDMUX_MCP_HTTP_BEARER_TOKEN"),
        allow_unauthenticated_http=parse_bool(env_value("SENDMUX_MCP_ALLOW_UNAUTHENTICATED_HTTP")),
        timeout_seconds=float(env_value("SENDMUX_MCP_TIMEOUT_SECONDS", "30")),
        stateless_http=parse_bool(env_value("SENDMUX_MCP_STATELESS_HTTP"), default=True),
        retry=RetryConfig(
            max_attempts=int(env_value("SENDMUX_MCP_RETRY_MAX_ATTEMPTS", "3")),
            base_delay_seconds=float(env_value("SENDMUX_MCP_RETRY_BASE_DELAY_SECONDS", "0.25")),
            max_delay_seconds=float(env_value("SENDMUX_MCP_RETRY_MAX_DELAY_SECONDS", "8")),
            max_elapsed_seconds=float(retry_max_elapsed) if retry_max_elapsed else None,
        ),
    )


def normalise_transport(value: str) -> Transport:
    if value == "streamable-http":
        return "streamable-http"
    if value in {"stdio", "http"}:
        return value  # type: ignore[return-value]
    raise ValueError("transport must be one of: stdio, http, streamable-http")


def parse_csv(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


def parse_surfaces(value: str | None, *, default: tuple[Surface, ...] = ()) -> tuple[Surface, ...]:
    if not value:
        return default
    return normalise_surfaces(parse_csv(value))


def normalise_surfaces(values: Surface | Sequence[str]) -> tuple[Surface, ...]:
    if isinstance(values, str):
        candidates: Sequence[str] = parse_csv(values)
    else:
        candidates = values

    selected: list[Surface] = []
    for candidate in candidates:
        if candidate not in SURFACES:
            raise ValueError("surfaces must contain only: mailbox, management, sending")
        surface = cast(Surface, candidate)
        if surface not in selected:
            selected.append(surface)

    if not selected:
        raise ValueError("At least one Sendmux MCP surface must be selected.")
    return tuple(selected)


def surface_api_keys_from_env() -> dict[Surface, str]:
    keys: dict[Surface, str] = {}
    for surface in SURFACES:
        value = env_value(f"SENDMUX_{surface.upper()}_API_KEY")
        if value:
            keys[surface] = value
    return keys


def parse_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def require_env(name: str) -> str:
    value = env_value(name)
    if not value:
        raise ValueError(f"Missing required environment variable {name}")
    return value
