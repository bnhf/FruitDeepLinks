#!/usr/bin/env python3
"""Shared project version helpers."""

from pathlib import Path

PROJECT_URL = "https://github.com/kineticman/FruitDeepLinks/"
DEFAULT_VERSION = "0.1.0"


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_version() -> str:
    """Return the canonical project version from the VERSION file."""
    version_path = get_project_root() / "VERSION"
    try:
        version = version_path.read_text(encoding="utf-8").strip()
        return version or DEFAULT_VERSION
    except Exception:
        return DEFAULT_VERSION
