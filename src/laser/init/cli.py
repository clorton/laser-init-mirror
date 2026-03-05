"""
Command-line interface for laser-init.
Using the Click library to create a simple CLI entry point. This can be expanded with subcommands and options as needed.
"""

import click

from .config import VERSION
from .logger import logger


@click.version_option(version=VERSION, prog_name="laser-init")
def cli():
    """Download spatial data for modeling diseases across populations."""
    logger.info("Starting laser-init CLI")
    print("Hello from laser-init! This is a placeholder for the CLI functionality.")
    pass


if __name__ == "__main__":
    cli()
