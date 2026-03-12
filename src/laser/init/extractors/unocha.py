"""
Docstring for laser.init.extractors.unocha

https://data.humdata.org/dataset/70f1cb54-a30c-43b2-a751-44e77d8f5ade/resource/733a9d4c-4e70-4f67-a5af-4138922cf43f/download/global_admin_boundaries_matched_latest.gdb.zip
"""

from pathlib import Path

from ..config import configuration as config
from ..utils import download_file, error, inform


class UnochaExtractor:
    def __init__(self) -> None:
        """Initialize the UNOCHA extractor.

        Returns:
            None
        """
        pass

    @staticmethod
    def description() -> str:
        """Return a brief description of this extractor.

        Returns:
            A string describing the data source and purpose of this extractor.
        """
        return "Extracts data from the United Nations Office for the Coordination of Humanitarian Affairs (UNOCHA) at https://data.humdata.org"

    def extract(self, country, level, year) -> Path | None:
        """Extract UNOCHA global administrative boundaries data.

        Downloads the global administrative boundaries dataset from UNOCHA's
        Humanitarian Data Exchange. This is a single global file containing
        all countries, which will be filtered in the transform step.

        Args:
            country: ISO 3166-1 alpha-3 country code (used for cache organization).
            level: Administrative level (used for subsequent filtering).
            year: Year for the data (used for cache organization, but data is latest).

        Returns:
            Path to the downloaded geodatabase zip file, or None if download failed.

        Raises:
            RuntimeError: If the download fails.
        """

        cache_root = Path(config.get("cache_dir", Path.cwd()))
        unocha_path: Path = Path("UNOCHA")
        (cache_root / unocha_path).mkdir(parents=True, exist_ok=True)

        local_path = None

        zip_file = "global_admin_boundaries_matched_latest.gdb.zip"
        url: str = f"https://data.humdata.org/dataset/70f1cb54-a30c-43b2-a751-44e77d8f5ade/resource/733a9d4c-4e70-4f67-a5af-4138922cf43f/download/{zip_file}"

        try:
            local_path: Path = download_file(url, cache_dir=cache_root, dest_dir=unocha_path)
            inform(f"Downloaded UNOCHA data: {local_path}")

        except Exception as e:
            error(f"Failed to download UNOCHA data: {e}.", RuntimeError)

        return local_path
