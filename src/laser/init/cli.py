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
from laser.init.loaders import abm, mpm
from laser.init.transformers import gadm as gadmtx
from laser.init.transformers import geoboundaries as geoboundariestx
from laser.init.transformers import unocha as unochatx
from laser.init.transformers import unwpp as unwpptx

from .config import VERSION
from .config import configuration as config
from .utils import error, inform, iso_from_country_string, level_from_string

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
    "--output-dir",
    type=Path,
    default=None,
    help="Output directory for transformed data (default: ./ISOCODE/start_year)",
)
@click.option(
    "--mode",
    type=click.Choice(["ABM", "MPM"], case_sensitive=False),
    default="ABM",
    help="Select the modeling mode - ABM or MPM (default: ABM)",
)
@click.option(
    "--model",
    type=click.Choice(["SI", "SIR", "SEIR"], case_sensitive=False),
    default="SIR",
    help="Select the type of epidemiological model to prepare data for (default: SIR)",
)
@click.option(
    "--shape-source",
    type=click.Choice(["unocha", "geoboundaries", "gadm"], case_sensitive=False),
    default=None,
    help="Select the shape file source (default: laser_config value or 'UNOCHA')",
)
@click.option(
    "--raster-source",
    type=click.Choice(["worldpop"], case_sensitive=False),
    default=None,
    help="Select the population raster file source (default: laser_config value or 'WorldPop')",
)
@click.option(
    "--stats-source",
    type=click.Choice(["unwpp"], case_sensitive=False),
    default=None,
    help="Select the demographic stats source (default: laser_config value or 'UNWPP')",
)
def cli(
    country,
    level,
    start_year,
    end_year,
    output_dir,
    mode,
    model,
    shape_source,
    raster_source,
    stats_source,
):
    """Download spatial data for modeling diseases across populations and prepare for use with a LASER model."""
    inform("Starting laser-init CLI")
    inform(
        f"Received arguments: country={country}, level={level}, start_year={start_year}, end_year={end_year}, output_dir={output_dir}, shape_source={shape_source}, raster_source={raster_source}, stats_source={stats_source}"
    )

    iso_code, adm_level, output_dir = validate_arguments(
        country, level, start_year, end_year, output_dir
    )

    # Extract (download)
    shape_data = download_shape_data(iso_code, adm_level, start_year, shape_source)
    raster_data = download_raster_data(iso_code, start_year, raster_source)
    stats_data = download_demographic_stats(iso_code, start_year, end_year, stats_source)

    # Transform
    shape_filename = transform_shape_and_raster_data(
        shape_source, shape_data, iso_code, adm_level, raster_data, output_dir
    )
    (cxr_filename, pop_filename, exp_filename) = transform_stats_data(
        stats_source, stats_data, iso_code, start_year, end_year, output_dir
    )

    # Load (emit data loading script)
    emit_model_script(
        mode, model, shape_filename, cxr_filename, pop_filename, exp_filename, output_dir
    )

    write_plots(shape_filename, cxr_filename, pop_filename, exp_filename, output_dir)

    return


def validate_arguments(country, level, start_year, end_year, output_dir):

    iso_code = iso_from_country_string(country)
    if not iso_code:
        error(
            f"Could not determine the ISO-3 code for '{country}'. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    inform(f"Country: {country} → ISO-3: {iso_code}")

    adm_level = level_from_string(level)
    if adm_level is None:
        error(
            f"Could not determine the administrative level from '{level}'. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    inform(f"Administrative Level: {level} → ADM{adm_level}")

    # Rough validation of years
    # test against 1900 second to ensure `now` is set
    if start_year > (now := datetime.now()).year or start_year < 1900:
        error(
            f"Base year {start_year} is out of range 1900...{now.year}. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    inform(f"Base year: {start_year}")

    # test against 1900 second to ensure `now` is set
    if end_year > (now := datetime.now()).year or end_year < start_year:
        error(
            f"End year {end_year} is out of range {start_year}...{now.year}. Please check your input and try again."
        )
        raise click.exceptions.Exit(1)
    inform(f"End year: {end_year}")

    output_dir = output_dir or Path.cwd() / iso_code / str(start_year)
    output_dir.mkdir(parents=True, exist_ok=True)
    assert output_dir.is_dir(), f"Output directory {output_dir} is not a valid directory."
    inform(f"Output directory: {output_dir}")

    return iso_code, adm_level, output_dir


def download_shape_data(iso_code, adm_level, start_year, shape_source):

    shape_source = (shape_source or config.get("shape_source", "unocha")).lower()
    try:
        shape_extractor = {
            "unocha": unochaex.UnochaExtractor,
            "geoboundaries": geoboundariesex.GeoBoundariesExtractor,
            "gadm": gadmex.GadmExtractor,
        }[shape_source]()
    except KeyError:
        error(
            f"Invalid shape source '{shape_source}'. Valid options are: unocha, geoboundaries, gadm."
        )
        raise click.exceptions.Exit(1) from None

    inform(f"Using shape source: {shape_source} ({shape_extractor.description()})")

    return shape_extractor.extract(iso_code, adm_level, start_year)


def download_raster_data(iso_code, start_year, raster_source):

    raster_source = (raster_source or config.get("raster_source", "worldpop")).lower()
    try:
        raster_extractor = {
            "worldpop": worldpopex.WorldPopExtractor,
        }[raster_source]()
    except KeyError:
        error(f"Invalid raster source '{raster_source}'. Valid options are: worldpop.")
        raise click.exceptions.Exit(1) from None

    inform(f"Using raster source: {raster_source} ({raster_extractor.description()})")

    return raster_extractor.extract(iso_code, start_year)


def download_demographic_stats(iso_code, start_year, end_year, stats_source):

    stats_source = (stats_source or config.get("stats_source", "unwpp")).lower()

    try:
        stats_extractor = {
            "unwpp": unwppex.UnwppExtractor,
        }[stats_source]()
    except KeyError:
        error(f"Invalid demographic stats source '{stats_source}'. Valid options are: unwpp.")
        raise click.exceptions.Exit(1) from None

    inform(f"Using demographic stats source: UNWPP ({stats_extractor.description()})")

    return stats_extractor.extract(iso_code, start_year, end_year)


def transform_shape_and_raster_data(
    shape_source: str,
    shape_data: Path,
    iso_code: str,
    adm_level: int,
    raster_data: Path,
    output_dir: Path,
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
        output_dir: Path to the output directory where transformed data will be saved.

    Returns:
        The result of the shape transformer's transform method.

    Raises:
        KeyError: If the specified shape_source is not found in the available transformers.
    """

    shape_source = (shape_source or config.get("shape_source", "unocha")).lower()
    shape_transformer = {
        "unocha": unochatx.UnochaTransformer,
        "geoboundaries": geoboundariestx.GeoBoundariesTransformer,
        "gadm": gadmtx.GadmTransformer,
    }[shape_source]()

    inform(f"Using shape transformer: {shape_source} ({shape_transformer.description()})")

    return shape_transformer.transform(shape_data, iso_code, adm_level, raster_data, output_dir)


def transform_stats_data(stats_source, stats_data, iso_code, start_year, end_year, output_dir):

    stats_source = (stats_source or config.get("stats_source", "unwpp")).lower()
    stats_transformer = {
        "unwpp": unwpptx.UnwppTransformer,
        # Add other stats transformers here as needed
    }[stats_source]()

    inform(
        f"Using demographic stats transformer: {stats_source} ({stats_transformer.description()})"
    )

    return stats_transformer.transform(stats_data, iso_code, start_year, end_year, output_dir)


def emit_model_script(
    mode, model, shape_filename, cxr_filename, pop_filename, exp_filename, output_dir
):
    # For now, just print the paths to the transformed data files. In the future, this could generate
    # a Python script that loads the data and prepares it for use with a LASER model.
    inform(f"Emitting model script for {mode}/{model} with data files:")
    inform(f"Shape file:                       '{shape_filename}'")
    inform(f"CBR/CDR file:                     '{cxr_filename}'")
    inform(f"Population age distribution file: '{pop_filename}'")
    inform(f"Life expectancy file:             '{exp_filename}'")

    model_loader = {
        "ABM/SI": abm.AbmLoader,
        "ABM/SIR": abm.AbmLoader,
        "ABM/SEIR": abm.AbmLoader,
        "MPM/SI": mpm.MpmLoader,
        "MPM/SIR": mpm.MpmLoader,
        "MPM/SEIR": mpm.MpmLoader,
    }[f"{mode.upper()}/{model.upper()}"]()

    model_loader.emit_script(
        mode, model, shape_filename, cxr_filename, pop_filename, exp_filename, output_dir
    )


def write_plots(shape_filename, cxr_filename, pop_filename, exp_filename, output_dir):
    # Placeholder for writing plots of the data. This could include:
    # - A map of the administrative regions with population density
    # - A plot of CBR/CDR over time
    # - A plot of the age distribution
    # - A plot of life expectancy over time
    inform("Writing plots of the transformed data... (not implemented yet)")

    # Generate choropleth map of population density by administrative region and
    # write as a PNG in output_dir


if __name__ == "__main__":
    cli()
