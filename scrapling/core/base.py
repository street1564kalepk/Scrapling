"""Base classes and utilities for Scrapling.

This module provides the foundational data structures used throughout
the Scrapling library for representing and interacting with parsed HTML/XML content.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterator, List, Optional, Union


class TextHandler(str):
    """A string subclass that provides additional text processing utilities.

    Wraps extracted text content and exposes helper methods commonly
    needed when scraping web pages.
    """

    def clean(self) -> "TextHandler":
        """Strip leading/trailing whitespace and collapse internal whitespace."""
        cleaned = re.sub(r"\s+", " ", self.strip())
        return TextHandler(cleaned)

    def as_int(self, default: int = 0) -> int:
        """Attempt to parse the text as an integer.

        Args:
            default: Value returned when conversion fails.

        Returns:
            Integer representation of the text, or *default* on failure.
        """
        try:
            return int(re.sub(r"[^\d-]", "", self))
        except (ValueError, TypeError):
            return default

    def as_float(self, default: float = 0.0) -> float:
        """Attempt to parse the text as a float.

        Args:
            default: Value returned when conversion fails.

        Returns:
            Float representation of the text, or *default* on failure.
        """
        try:
            # Note: this regex keeps only digits, dots, and minus signs.
            # It won't handle locale-specific formats like commas as decimal separators.
            return float(re.sub(r"[^\d.\-]", "", self))
        except (ValueError, TypeError):
            return default

    def re_search(self, pattern: str, group: int = 1) -> Optional[str]:
        """Apply a regex pattern and return the specified capture group.

        Args:
            pattern: Regular expression pattern string.
            group: Capture group index to return (default 1).

        Returns:
            The matched group string, or ``None`` if no match is found.
        """
        match = re.search(pattern, self)
        if match:
            try:
                return match.group(group)
            except IndexError:
                return None
        return None


class AttributeHandler(dict):
    """A dict subclass for element attributes with convenient accessors.

    Allows attribute access via dot notation in addition to standard
    dictionary operations.
    """

    def __getattr__(self, name: str) -> Optional[str]:
        try:
            return self[name]
        except KeyError:
            return None

    def get(self, key: str, default: Any = None) -> Any:  # type: ignore[override]
        """Return the attribute value for *key*, or *default* if absent."""
        return super().get(key, default)

    def has(self, key: str, value: Optional[str] = None) -> bool:
        """Check whether an attribute exists, optionally matching a value.

        Args:
            key: Attribute name to look up.
            value: When provided, also checks that the attribute equals this value.

        Retu
