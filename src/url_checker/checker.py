"""Core URL checking functionality."""

import logging
from typing import Optional

import requests

logger = logging.getLogger("url_checker")


class URLCheckResult:
    """Data class for URL check results."""

    def __init__(self, url: str, status: str, status_code: Optional[int] = None):
        """
        Initialize URL check result.

        Args:
            url: The URL that was checked.
            status: Human-readable status message.
            status_code: HTTP status code (None for errors).
        """
        self.url = url
        self.status = status
        self.status_code = status_code

    def is_success(self) -> bool:
        """
        Check if result indicates success (2xx status code).

        Returns:
            True if status code is in 2xx range, False otherwise.
        """
        return self.status_code is not None and 200 <= self.status_code < 300


def check_url(url: str, timeout: int = 5) -> URLCheckResult:
    """
    Check single URL and return result with comprehensive error handling.

    Args:
        url: URL to check.
        timeout: Request timeout in seconds.

    Returns:
        URLCheckResult with status information.
    """
    logger.debug(f"Checking URL: {url}")

    try:
        response = requests.get(url, timeout=timeout)
        status_code = response.status_code
        reason = response.reason
        status_message = f"{status_code} {reason}"
        logger.debug(f"Received status {status_code} for {url}")
        return URLCheckResult(url=url, status=status_message, status_code=status_code)

    except requests.Timeout:
        logger.warning(f"Timeout checking {url}")
        return URLCheckResult(url=url, status="TIMEOUT")

    except requests.ConnectionError:
        logger.warning(f"Connection error for {url}")
        return URLCheckResult(url=url, status="CONNECTION_ERROR")

    except requests.RequestException as e:
        error_type = type(e).__name__
        logger.error(f"Request error checking {url}: {error_type}", exc_info=True)
        return URLCheckResult(url=url, status=f"REQUEST_ERROR: {error_type}")

    except Exception as e:
        error_type = type(e).__name__
        logger.error(f"Unexpected error checking {url}: {error_type}", exc_info=True)
        return URLCheckResult(url=url, status=f"ERROR: {error_type}")


def check_urls(urls: list[str], timeout: int = 5) -> list[URLCheckResult]:
    """
    Check multiple URLs and return results.

    Args:
        urls: List of URLs to check.
        timeout: Request timeout in seconds.

    Returns:
        List of URLCheckResult objects.
    """
    logger.info(f"Checking {len(urls)} URLs with timeout={timeout}s")
    results = []

    for url in urls:
        result = check_url(url, timeout)
        results.append(result)

    logger.info(f"Completed checking {len(urls)} URLs")
    return results
