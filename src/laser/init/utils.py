"""
Utility functions for the laser.init package.

Using the [RapidFuzz package](https://rapidfuzz.github.io/RapidFuzz/) for fuzzy string matching to convert country names to ISO codes.

- Initial näive choice, use Damerau-Levenshtein distance, which allows for transpositions, as well as insertions, deletions, and substitutions.

"""

import unicodedata
import warnings
from pathlib import Path

import pycountry
import requests
from tqdm import tqdm

from .french_iso import french_mapping as __french_mapping__
from .logger import logger


def _normalize_string(value: str) -> str:
    """Normalize a country string for matching.

    - Unicode NFKD + drop combining marks: makes accents/diacritics comparable.
    - Casefold: more aggressive (and correct) case normalization than lower().
    - Strip: removes surrounding whitespace.
    """

    decomposed = unicodedata.normalize("NFKD", (value or "").strip())
    no_marks = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return no_marks.casefold()


__iso_codes__ = {
    _normalize_string(country.alpha_3): country.alpha_3 for country in pycountry.countries
}

__name_mapping__ = {
    _normalize_string(country.name): country.alpha_3 for country in pycountry.countries
}

__name_mapping__.update(
    {_normalize_string(key): value for key, value in __french_mapping__.items()}
)

__name_mapping__.update(
    {
        _normalize_string(country.official_name): country.alpha_3
        for country in pycountry.countries
        if hasattr(country, "official_name")
    }
)

__name_mapping__.update(
    {
        "bonaire": "BES",
        "bolivia": "BOL",
        "congo": "COG",
        "micronesia": "FSM",
        "iran": "IRN",
        "korea": "KOR",
        "moldova": "MDA",
        "palestine": "PSE",
        "saint helena": "SHN",
        "taiwain": "TWN",
        "tanzania": "TZA",
        "venezuela": "VEN",
    }
)


def iso_from_country_string(input_string: str) -> str | None:
    """
    Convert a country name to its ISO 3166-1 alpha-3 code.
    """
    normalized = _normalize_string(input_string)
    logger.info(
        f"iso_from_country_string(): Normalized input string '{input_string}' to '{normalized}'."
    )

    if normalized in __iso_codes__:
        iso3 = __iso_codes__[normalized]
        logger.info(
            f"iso_from_country_string(): Found exact ISO code match for '{normalized}': {iso3}"
        )
        return iso3
    elif normalized in __name_mapping__:
        iso3 = __name_mapping__[normalized]
        logger.info(f"iso_from_country_string(): Found exact name match for '{normalized}': {iso3}")
        return iso3

    if len(normalized) < 4:
        logger.info(
            f"iso_from_country_string(): Input string '{input_string}' is too short for reliable matching. Returning None."
        )
        return None

    try:
        options = pycountry.countries.search_fuzzy(normalized)
        if options:
            matches = "\n\t".join(f"{country.name} (ISO: {country.alpha_3})" for country in options)
            warnings.warn(f"Possible match(es):\n\t{matches}", stacklevel=2)
    except LookupError:
        pass

    logger.info(
        f"iso_from_country_string(): No matches found for '{input_string}'. Returning None."
    )
    return None


def level_from_string(input_string: str) -> int | None:
    """
    Convert a level string in the form 'admin1' or 'ADM2' or '3' to a standardized level code.
    """

    lowered = input_string.lower().strip()

    # Valid strings start with "admin" or "adm", followed by a number, or just a number
    if lowered.startswith("admin"):
        number_part = lowered[5:]
    elif lowered.startswith("adm"):
        number_part = lowered[3:]
    else:
        number_part = lowered

    # Validate that number_part is a single digit between 0 and 4
    if number_part.isdigit():
        level_num = int(number_part)
        if 0 <= level_num <= 4:
            logger.info(
                f"level_from_string(): Parsed level number {level_num} from input '{input_string}'."
            )
            return level_num

    logger.info(f"level_from_string(): No matches found for '{input_string}'. Returning None.")
    return None


def download_file(
    url: str,
    dest_dir: Path,
    local_name: str = None,
    show_progress: bool = True,
    force: bool = False,
) -> Path:
    """
    Download a file from a URL and save it to the specified directory.

    The function streams the file in chunks, displays a progress bar if enabled.
    If the file already exists and force is False, the existing file is returned without downloading.

    Args:
        url (str): The URL of the file to download.
        dest_dir (Path): The directory where the file will be saved.
        local_name (str, optional): The name to use for the saved file. If None, uses the filename from the URL.
        show_progress (bool, optional): If True, display a progress bar during download (default: True).
        force (bool, optional): If True, download even if the file already exists (default: False).

    Returns:
        Path: The path to the downloaded file.
    """

    local_name = local_name or url.split("/")[-1]
    local_path = dest_dir / local_name

    if local_path.exists() and not force:
        logger.info(f"File already exists and force is not set: {local_path}")
        return local_path

    logger.info(f"Downloading file from {url} to {local_path}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total = int(response.headers.get("content-length", 0))
    chunk_size = 8192

    if total > 0 and show_progress:
        progress = tqdm(total=total, unit="B", unit_scale=True, desc=local_name)

    with local_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                if show_progress:
                    progress.update(len(chunk))

    if show_progress:
        progress.close()

    logger.info(f"File downloaded successfully: {local_path}")

    return local_path
