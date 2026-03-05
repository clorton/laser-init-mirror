"""
Utility functions for the laser.init package.

Using the [RapidFuzz package](https://rapidfuzz.github.io/RapidFuzz/) for fuzzy string matching to convert country names to ISO codes.

- Initial näive choice, use Damerau-Levenshtein distance, which allows for transpositions, as well as insertions, deletions, and substitutions.

"""

import unicodedata
import warnings

import pycountry

from .french_iso import french_mapping as __french_mapping__


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
    input_string = _normalize_string(input_string)

    if input_string in __iso_codes__:
        return __iso_codes__[input_string]
    elif input_string in __name_mapping__:
        return __name_mapping__[input_string]

    warnings.warn(
        f"No exact match found for input string '{input_string}'. Looking for potential matches.",
        stacklevel=2,
    )

    if len(input_string) < 4:
        warnings.warn(
            "Input string is too short for reliable matching. Returning None.",
            stacklevel=2,
        )
        return None

    try:
        options = pycountry.countries.search_fuzzy(input_string)
        if options:
            matches = "\n\t".join(f"{country.name} (ISO: {country.alpha_3})" for country in options)
            warnings.warn(f"Possible match(es):\n\t{matches}", stacklevel=2)
    except LookupError:
        warnings.warn("No fuzzy matches found. Returning None", stacklevel=2)

    return None
