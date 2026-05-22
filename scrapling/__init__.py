"""Scrapling - A powerful, flexible web scraping library.

Scraping made easy with auto-adapting selectors, smart element detection,
and robust parsing capabilities.
"""

__version__ = "0.2.9"
__author__ = "D4Vinci"
__license__ = "MIT"

from scrapling.core.fetchers import Fetcher, AsyncFetcher
from scrapling.core.page import Adaptor
from scrapling.core.custom_types import (
    SelectorList,
    TextHandler,
)

__all__ = [
    "Fetcher",
    "AsyncFetcher",
    "Adaptor",
    "SelectorList",
    "TextHandler",
]
