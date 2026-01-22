"""HTTP Status Checker - A CLI tool to check URL health."""

__version__ = "0.1.0"
__author__ = "Shankar Pentyala"

from .checker import URLCheckResult, check_url, check_urls
from .cli import main

__all__ = [
    "check_url",
    "check_urls",
    "URLCheckResult",
    "main",
    "__version__",
]
