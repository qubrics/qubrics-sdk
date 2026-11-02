from __future__ import annotations

import os
from typing import overload


@overload
def env_value(name: str, default: str) -> str: ...


@overload
def env_value(name: str, default: None = None) -> str | None: ...


def env_value(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name.replace("SENDMUX_", "QUBRICS_", 1), os.environ.get(name, default))
