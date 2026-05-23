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

        Returns:
            ``True`` if the attribute (and optional value) matches.
        """
        if key not in self:
            return False
        return value is None or self[key] == value


class BaseParser:
    """Minimal interface that all Scrapling parser backends must implement.

    Concrete parsers (e.g. Selectolax, lxml, BeautifulSoup wrappers) should
    subclass ``BaseParser`` and implement the abstract methods below.
    """

    def __init__(self, html: str, url: Optional[str] = None) -> None:
        """
        Args:
            html: Raw HTML/XML source to parse.
            url: Optional base URL used for resolving relative links.
        """
        self._html = html
        self._url = url

    # ------------------------------------------------------------------
    # Subclasses must override these
    # ------------------------------------------------------------------

    def css(self, selector: str) -> List[Any]:
        """Return all elements matching a CSS *selector*."""
        raise NotImplementedError

    def xpath(self, query: str) -> List[Any]:
        """Return all elements matching an XPath *query*."""
        raise NotImplementedError

    def find(self, tag: str, attrs: Optional[Dict[str, str]] = None) -> Optional[Any]:
        """Return the first element matching *tag* and optional *attrs*."""
        raise NotImplementedError

    def find_all(self, tag: str, attrs: Optional[Dict[str, str]] = None) -> List[Any]:
        """Return all elements matching *tag* and optional *attrs*."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Shared helpers available to all parsers
    # ------------------------------------------------------------------

    @property
    def url(self) -> Optional[str]:
        """The base URL associated with this document, if any."""
        return self._url

    def __repr__(self) -> str:  # pragma: no cover
        snippet = self._html[:60].replace("\n", " ")
        return f"<{self.__class__.__name__} url={self._url!r} html={snippet!r}...>"
