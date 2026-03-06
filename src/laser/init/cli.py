"""
Command-line interface for laser-init.
Using the Click library to create a simple CLI entry point. This can be expanded with subcommands and options as needed.
"""

from datetime import datetime

import click

from laser.init.extractors import gadm, geoboundaries, unocha, unwpp, worldpop

from .config import VERSION
from .config import configuration as config
from .logger import logger
from .utils import iso_from_country_string, level_from_string


@click.command()
@click.version_option(version=VERSION, prog_name="laser-init")
@click.argument("country", required=True)
@click.argument("level", required=True)
@click.argument("start-year", required=True, type=int)
@click.argument("end-year", required=True, type=int)
@click.option(
    "--shape-source",
    type=str,
    default=None,
    help="Select the shape file source (default: laser_config value or 'UNOCHA')",
)
@click.option(
    "--raster-source",
    type=str,
    default=None,
    help="Select the population raster file source (default: laser_config value or 'WorldPop')",
)
@click.option(
    "--stats-source",
    type=str,
    default=None,
    help="Select the demographic stats source (default: laser_config value or 'UNWPP')",
)
def cli(country, level, start_year, end_year, shape_source, raster_source, stats_source):
    """Download spatial data for modeling diseases across populations."""
    logger.info("Starting laser-init CLI")

    iso_code, adm_level = validate_arguments(country, level, start_year, end_year)

    # Extract (download)
    shape_file = download_shape_data(iso_code, adm_level, start_year, shape_source)
    raster_file = download_raster_data(iso_code, start_year, raster_source)
    stats_files = download_demographic_stats(iso_code, start_year, end_year, stats_source)

    # Transform

    # Load (emit data loading script)

    return


def validate_arguments(country, level, start_year, end_year):

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

    # Rough validation of years
    # test against 1900 second to ensure `now` is set
    if start_year > (now := datetime.now()).year or start_year < 1900:
        click.echo(
            f"Base year {start_year} is out of range 1900...{now.year}. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    click.echo(f"Base year: {start_year}")

    # test against 1900 second to ensure `now` is set
    if end_year > (now := datetime.now()).year or end_year < start_year:
        click.echo(
            f"End year {end_year} is out of range {start_year}...{now.year}. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    click.echo(f"End year: {end_year}")

    return iso_code, adm_level


def download_shape_data(iso_code, adm_level, start_year, shape_source):

    shape_source = (shape_source or config.get("shape_source", "unocha")).lower()
    try:
        shape_extractor = {
            "unocha": unocha.UnochaExtractor,
            "geoboundaries": geoboundaries.GeoBoundariesExtractor,
            "gadm": gadm.GadmExtractor,
        }[shape_source]()
    except KeyError:
        logger.error(
            f"Invalid shape source '{shape_source}'. Valid options are: unocha, geoboundaries, gadm."
        )
        click.echo(
            f"Invalid shape source '{shape_source}'. Valid options are: unocha, geoboundaries, gadm."
        )
        raise click.exceptions.Exit(1) from None

    msg = f"Using shape source: {shape_source} ({shape_extractor.description()})"
    logger.info(msg)
    click.echo(msg)

    return shape_extractor.extract(iso_code, adm_level, start_year)


def download_raster_data(iso_code, start_year, raster_source):

    raster_source = (raster_source or config.get("raster_source", "worldpop")).lower()
    try:
        raster_extractor = {
            "worldpop": worldpop.WorldPopExtractor,
        }[raster_source]()
    except KeyError:
        logger.error(f"Invalid raster source '{raster_source}'. Valid options are: worldpop.")
        click.echo(f"Invalid raster source '{raster_source}'. Valid options are: worldpop.")
        raise click.exceptions.Exit(1) from None

    msg = f"Using raster source: {raster_source} ({raster_extractor.description()})"
    logger.info(msg)
    click.echo(msg)

    return raster_extractor.extract(iso_code, start_year)


def download_demographic_stats(iso_code, start_year, end_year, stats_source):

    stats_source = (stats_source or config.get("stats_source", "unwpp")).lower()

    try:
        stats_extractor = {
            "unwpp": unwpp.UnwppExtractor,
        }[stats_source]()
    except KeyError:
        logger.error(
            f"Invalid demographic stats source '{stats_source}'. Valid options are: unwpp."
        )
        click.echo(f"Invalid demographic stats source '{stats_source}'. Valid options are: unwpp.")
        raise click.exceptions.Exit(1) from None

    msg = f"Using demographic stats source: UNWPP ({stats_extractor.description()})"
    logger.info(msg)
    click.echo(msg)

    return stats_extractor.extract(iso_code, start_year, end_year)


if __name__ == "__main__":
    cli()
