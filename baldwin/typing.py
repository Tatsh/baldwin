"""Typing helpers."""
from __future__ import annotations

from typing import NotRequired, TypedDict


class _BaldwinBaldwin(TypedDict):
    prettier_config: str


class BaldwinConfigContainer(TypedDict):
    """Container for Baldwin configuration."""
    baldwin: NotRequired[_BaldwinBaldwin]
