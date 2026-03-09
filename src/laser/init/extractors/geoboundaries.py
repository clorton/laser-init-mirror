"""
Docstring for laser.init.extractors.geoboundaries

E.g., https://github.com/wmgeolab/geoBoundaries/raw/refs/heads/main/releaseData/gbOpen/USA/ADM0/geoBoundaries-USA-ADM0-all.zip
"""

from pathlib import Path

from ..config import configuration as config
from ..utils import download_file, error, inform


class GeoBoundariesExtractor:
    def __init__(self):
        pass

    @staticmethod
    def description():
        return "Extracts data from GeoBoundaries at https://www.github.com/wmgeolab/geoBoundaries"

    def extract(self, country, level, year):

        # Sample: https://github.com/wmgeolab/geoBoundaries/raw/refs/tags/v6.0.0/releaseData/gbOpen/MCO/ADM1/geoBoundaries-MCO-ADM1-all.zip

        cache_path = Path(config.get("cache_dir", Path.cwd())) / "geoBoundaries" / country
        cache_path.mkdir(parents=True, exist_ok=True)

        local_path = None

        zip_file = f"geoBoundaries-{country}-ADM{level}-all.zip"
        url = f"https://github.com/wmgeolab/geoBoundaries/raw/refs/tags/v6.0.0/releaseData/gbOpen/{country}/ADM{level}/{zip_file}"

        try:
            local_path = download_file(url, dest_dir=cache_path)
            inform(f"Downloaded GeoBoundaries data: {local_path}")

        except Exception as e:
            error(f"Failed to download GeoBoundaries data: {e}.")
            local_path = None

        return local_path
