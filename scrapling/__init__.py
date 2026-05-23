"""Scrapling - A powerful, flexible web scraping library.

Scraping made easy with auto-adapting selectors, smart element detection,
and robust parsing capabilities.

Personal fork notes:
- Forked for learning/personal use
- Upstream: https://github.com/D4Vinci/Scrapling
- Added StealthyFetcher and PlayWrightFetcher to top-level imports for convenience
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

# Conditionally import optional fetchers that require extra dependencies
try:
    from scrapling.fetchers import StealthyFetcher, PlayWrightFetcher
    _optional_fetchers_available = True
except ImportError:
    _optional_fetchers_available = False

__all__ = [
    "Fetcher",
    "AsyncFetcher",
    "Adaptor",
    "SelectorList",
    "TextHandler",
]

if _optional_fetchers_available:
    __all__ += ["StealthyFetcher", "PlayWrightFetcher"]
