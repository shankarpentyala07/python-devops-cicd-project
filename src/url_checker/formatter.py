"""Output formatting with color support."""

import sys

from .checker import URLCheckResult

# Use colorama for cross-platform color support (Windows compatibility)
try:
    from colorama import Fore, Style, init

    init(autoreset=True)  # Auto-reset colors after each print
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


class TableFormatter:
    """Format URL check results as colored table."""

    # Color constants
    GREEN = Fore.GREEN if COLORS_AVAILABLE else ""
    RED = Fore.RED if COLORS_AVAILABLE else ""
    RESET = Style.RESET_ALL if COLORS_AVAILABLE else ""

    @staticmethod
    def format_results(results: list[URLCheckResult]) -> str:
        """
        Format results as a table with color coding.

        Args:
            results: List of URLCheckResult objects to format.

        Returns:
            Formatted table string with colors.
        """
        if not results:
            return "No URLs to check."

        # Calculate maximum URL length for proper column alignment
        max_url_length = max(len(result.url) for result in results)
        # Ensure minimum width for the URL column
        url_column_width = max(max_url_length, len("URL"))

        # Build header
        header = f"{'URL':<{url_column_width}} | Status"
        separator = "=" * (url_column_width + 3 + 20)

        # Build rows
        rows = []
        for result in results:
            # Choose color based on success/failure
            if result.is_success():
                color = TableFormatter.GREEN
            else:
                color = TableFormatter.RED

            # Format row with color
            row = f"{color}{result.url:<{url_column_width}} | {result.status}{TableFormatter.RESET}"
            rows.append(row)

        # Combine all parts
        output = "\n".join([header, separator] + rows)
        return output

    @staticmethod
    def print_results(results: list[URLCheckResult]) -> None:
        """
        Print formatted results to stdout.

        Args:
            results: List of URLCheckResult objects to print.
        """
        print(TableFormatter.format_results(results))
