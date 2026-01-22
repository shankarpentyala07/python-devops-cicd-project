"""Click-based CLI interface."""

import sys

import click

from . import __version__
from .checker import check_urls
from .formatter import TableFormatter
from .logger import setup_logger


@click.command()
@click.argument("urls", nargs=-1, required=False)
@click.option(
    "--timeout",
    default=5,
    type=int,
    help="Request timeout in seconds (default: 5)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose (DEBUG) logging",
)
@click.version_option(version=__version__, prog_name="check-urls")
def main(urls: tuple[str, ...], timeout: int, verbose: bool) -> None:
    """
    Check HTTP status of multiple URLs.

    Examples:

        check-urls https://google.com https://github.com

        check-urls --timeout 10 --verbose https://api.example.com
    """
    # Setup logger
    setup_logger(verbose=verbose)

    # If no URLs provided, display help and exit
    if not urls:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit(0)

    # Convert tuple to list
    url_list = list(urls)

    # Check URLs
    results = check_urls(url_list, timeout=timeout)

    # Print results
    TableFormatter.print_results(results)

    # Exit with appropriate code
    # Exit code 0 if all successful, 1 if any failures
    has_failures = any(not result.is_success() for result in results)
    sys.exit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
