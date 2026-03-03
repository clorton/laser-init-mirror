import logging

import click

from .config import VERSION

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.version_option(version=VERSION, prog_name="laser-init")
def cli():
    """Download spatial data for modeling diseases across populations."""
    pass


if __name__ == "__main__":
    cli()
