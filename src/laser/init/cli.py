"""
Command-line interface for laser-init.
Using the Click library to create a simple CLI entry point. This can be expanded with subcommands and options as needed.
"""

from datetime import datetime
from pathlib import Path

import click

from laser.init.extractors import gadm as gadmex
from laser.init.extractors import geoboundaries as geoboundariesex
from laser.init.extractors import unocha as unochaex
from laser.init.extractors import unwpp as unwppex
from laser.init.extractors import worldpop as worldpopex
from laser.init.transformers import unocha as unochatx
from laser.init.transformers import unwpp as unwpptx

from .config import VERSION
from .config import configuration as config
from .logger import logger
from .utils import iso_from_country_string, level_from_string

help = """
Download spatial data for modeling diseases across populations and prepare for use with a LASER model.
E.g., laser-init NGA ADM2 2010 2025
"""


@click.command(help=help)
@click.version_option(version=VERSION, prog_name="laser-init")
@click.argument("country", required=True)
@click.argument("level", required=True)
@click.argument("start-year", required=True, type=click.IntRange(1950, 2050))
@click.argument("end-year", required=True, type=click.IntRange(1950, 2050))
@click.option(
    "--out-dir",
    type=Path,
    default=None,
    help="Output directory for transformed data (default: ./ISOCODE/start_year)",
)
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
def cli(country, level, start_year, end_year, out_dir, shape_source, raster_source, stats_source):
    """Download spatial data for modeling diseases across populations and prepare for use with a LASER model."""
    logger.info("Starting laser-init CLI")
    logger.info(
        f"Received arguments: country={country}, level={level}, start_year={start_year}, end_year={end_year}, out_dir={out_dir}, shape_source={shape_source}, raster_source={raster_source}, stats_source={stats_source}"
    )

    iso_code, adm_level, out_dir = validate_arguments(country, level, start_year, end_year, out_dir)

    # Extract (download)
    shape_data = download_shape_data(iso_code, adm_level, start_year, shape_source)
    raster_data = download_raster_data(iso_code, start_year, raster_source)
    stats_data = download_demographic_stats(iso_code, start_year, end_year, stats_source)

    # Transform
    shape_file = transform_shape_and_raster_data(
        shape_source, shape_data, iso_code, adm_level, raster_data, out_dir
    )
    transform_stats_data(stats_source, stats_data, iso_code, start_year, end_year)

    # Load (emit data loading script)

    return


def validate_arguments(country, level, start_year, end_year, out_dir):

    iso_code = iso_from_country_string(country)
    if not iso_code:
        click.echo(
            f"Sorry, could not determine the ISO-3 code for '{country}'. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    msg = f"Country: {country} → ISO-3: {iso_code}"
    logger.info(msg)
    click.echo(msg)

    adm_level = level_from_string(level)
    if adm_level is None:
        click.echo(
            f"Sorry, could not determine the administrative level from '{level}'. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    msg = f"Administrative Level: {level} → ADM{adm_level}"
    logger.info(msg)
    click.echo(msg)

    # Rough validation of years
    # test against 1900 second to ensure `now` is set
    if start_year > (now := datetime.now()).year or start_year < 1900:
        click.echo(
            f"Base year {start_year} is out of range 1900...{now.year}. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    msg = f"Base year: {start_year}"
    logger.info(msg)
    click.echo(msg)

    # test against 1900 second to ensure `now` is set
    if end_year > (now := datetime.now()).year or end_year < start_year:
        click.echo(
            f"End year {end_year} is out of range {start_year}...{now.year}. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    msg = f"End year: {end_year}"
    logger.info(msg)
    click.echo(msg)

    out_dir = out_dir or Path.cwd() / iso_code / str(start_year)
    out_dir.mkdir(parents=True, exist_ok=True)
    assert out_dir.is_dir(), f"Output directory {out_dir} is not a valid directory."
    msg = f"Output directory: {out_dir}"
    logger.info(msg)
    click.echo(msg)

    return iso_code, adm_level, out_dir


def download_shape_data(iso_code, adm_level, start_year, shape_source):

    shape_source = (shape_source or config.get("shape_source", "unocha")).lower()
    try:
        shape_extractor = {
            "unocha": unochaex.UnochaExtractor,
            "geoboundaries": geoboundariesex.GeoBoundariesExtractor,
            "gadm": gadmex.GadmExtractor,
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
            "worldpop": worldpopex.WorldPopExtractor,
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
            "unwpp": unwppex.UnwppExtractor,
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


def transform_shape_and_raster_data(
    shape_source: str,
    shape_data: Path,
    iso_code: str,
    adm_level: int,
    raster_data: Path,
    out_dir: Path,
):
    """Transform shape and raster data using the specified shape transformer.
    This function selects and instantiates the appropriate shape transformer based on
    the provided shape_source, then uses it to transform the input shape and raster data.

    Args:
        shape_source: The source of shape data (e.g., "unocha"). If not provided,
            defaults to the value from config. Case-insensitive.
        shape_data: Path to the input shape data file.
        iso_code: ISO country code for the region to process.
        adm_level: Administrative level (e.g., 0 for country, 1 for regions).
        raster_data: Path to the input raster data file.
        out_dir: Path to the output directory where transformed data will be saved.

    Returns:
        The result of the shape transformer's transform method.

    Raises:
        KeyError: If the specified shape_source is not found in the available transformers.
    """

    shape_source = (shape_source or config.get("shape_source", "unocha")).lower()
    shape_transformer = {
        "unocha": unochatx.UnochaTransformer,
        # "geoboundaries": geoboundariestx.GeoBoundariesTransformer,
        # "gadm": gadmtx.GadmTransformer,
    }[shape_source]()

    msg = f"Using shape transformer: {shape_source} ({shape_transformer.description()})"
    logger.info(msg)
    click.echo(msg)

    return shape_transformer.transform(shape_data, iso_code, adm_level, raster_data, out_dir)


def transform_stats_data(stats_source, stats_data, iso_code, start_year, end_year):

    stats_source = (stats_source or config.get("stats_source", "unwpp")).lower()
    stats_transformer = {
        "unwpp": unwpptx.UnwppTransformer,
        # Add other stats transformers here as needed
    }[stats_source]()

    msg = f"Using demographic stats transformer: {stats_source} ({stats_transformer.description()})"
    logger.info(msg)
    click.echo(msg)

    return stats_transformer.transform(stats_data, iso_code, start_year, end_year)


if __name__ == "__main__":
    cli()
