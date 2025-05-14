"""Typing helpers."""
from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired


class _BaldwinBaldwin(TypedDict):
    prettier_config: str


class BaldwinConfigContainer(TypedDict):
    """Container for Baldwin configuration."""
    baldwin: NotRequired[_BaldwinBaldwin]
