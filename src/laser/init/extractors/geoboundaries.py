"""
Docstring for laser.init.extractors.geoboundaries

E.g., https://github.com/wmgeolab/geoBoundaries/raw/refs/heads/main/releaseData/gbOpen/USA/ADM0/geoBoundaries-USA-ADM0-all.zip
"""

from pathlib import Path

from ..config import configuration as config
from ..utils import download_file, error, inform


class GeoBoundariesExtractor:
    """Extracts data from GeoBoundaries at https://www.github.com/wmgeolab/geoBoundaries"""

    def __init__(self):
        """Initialize the GeoBoundaries extractor."""
        pass

    @staticmethod
    def description():
        """Return a brief description of this extractor.

        Returns:
            A string describing the data source and purpose of this extractor.
        """
        return "Extracts data from GeoBoundaries at https://www.github.com/wmgeolab/geoBoundaries"

    def extract(self, country, level, year):
        """Extract GeoBoundaries administrative boundary data for a country.

        Downloads administrative boundary data from the GeoBoundaries repository
        for the specified country and administrative level. Uses version 6.0.0
        of the gbOpen dataset.

        Args:
            country: ISO 3166-1 alpha-3 country code (e.g., "MCO" for Monaco).
            level: Administrative level (0=country, 1=first-level subdivisions, etc.).
            year: Year for the data (used for cache organization, but data version is fixed).

        Returns:
            Path to the downloaded zip file, or None if download failed.

        Raises:
            RuntimeError: If the download fails.
        """

        # Sample: https://github.com/wmgeolab/geoBoundaries/raw/refs/tags/v6.0.0/releaseData/gbOpen/MCO/ADM1/geoBoundaries-MCO-ADM1-all.zip

        cache_root = Path(config.get("cache_dir", Path.cwd()))
        geoboundaries_path = Path("geoBoundaries") / country
        (cache_root / geoboundaries_path).mkdir(parents=True, exist_ok=True)

        local_path = None

        zip_file = f"geoBoundaries-{country}-ADM{level}-all.zip"
        url = f"https://github.com/wmgeolab/geoBoundaries/raw/refs/tags/v6.0.0/releaseData/gbOpen/{country}/ADM{level}/{zip_file}"

        try:
            local_path = download_file(url, cache_dir=cache_root, dest_dir=geoboundaries_path)
            inform(f"Downloaded GeoBoundaries data: {local_path}")

        except Exception as e:
            error(f"Failed to download GeoBoundaries data: {e}.", RuntimeError)

        return local_path
