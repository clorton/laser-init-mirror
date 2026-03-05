"""
Command-line interface for laser-init.
Using the Click library to create a simple CLI entry point. This can be expanded with subcommands and options as needed.
"""

from datetime import datetime

import click

from laser.init.extractors import gadm, geoboundaries, unocha

from .config import VERSION
from .config import configuration as config
from .logger import logger
from .utils import iso_from_country_string, level_from_string


@click.command()
@click.version_option(version=VERSION, prog_name="laser-init")
@click.argument("country", required=True)
@click.argument("level", required=True)
@click.argument("base-year", required=True, type=int)
@click.option(
    "--shape-source",
    type=str,
    default=None,
    help="Select the shape file source (default: laser_config value or 'UNOCHA')",
)
def cli(country, level, base_year, shape_source):
    """Download spatial data for modeling diseases across populations."""
    logger.info("Starting laser-init CLI")
    iso_code = iso_from_country_string(country)
    if not iso_code:
        click.echo(
            f"Sorry, could not determine the ISO-3 code for '{country}'. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    click.echo(f"Country: {country} → ISO-3: {iso_code}")

    adm_level = level_from_string(level)
    if adm_level is None:
        click.echo(
            f"Sorry, could not determine the administrative level from '{level}'. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    click.echo(f"Administrative Level: {level} → ADM{adm_level}")

    # Rough validation of year
    # test against 1900 second to ensure `now` is set
    if base_year > (now := datetime.now()).year or base_year < 1900:
        click.echo(
            f"Base year {base_year} is out of range 1900...{now.year}. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    click.echo(f"Base year: {base_year}")

    shape_source = (shape_source or config.get("shape_source", "unocha")).lower()
    try:
        extractor = {
            "unocha": unocha.UNOCHAExtractor,
            "geoboundaries": geoboundaries.GeoBoundariesExtractor,
            "gadm": gadm.GADMExtractor,
        }[shape_source]
    except KeyError:
        logger.error(
            f"Invalid shape source '{shape_source}'. Valid options are: unocha, geoboundaries, gadm."
        )
        click.echo(
            f"Invalid shape source '{shape_source}'. Valid options are: unocha, geoboundaries, gadm."
        )
        raise click.exceptions.Exit(1) from None

    msg = f"Using shape source: {shape_source} ({extractor.description()})"
    logger.info(msg)
    click.echo(msg)

    extractor_instance = extractor()
    extractor_instance.extract(iso_code, adm_level, base_year)

    return


if __name__ == "__main__":
    cli()
