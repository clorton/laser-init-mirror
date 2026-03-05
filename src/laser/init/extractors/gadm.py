"""
Docstring for laser.init.extractors.gadm

https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_NGA.gpkg
https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_NGA_shp.zip
"""

import zipfile
from pathlib import Path

from ..config import configuration as config
from ..logger import logger
from ..utils import download_file


class GADMExtractor:
    def __init__(self, prefer_gpkg: bool = True):

        self.prefer_gpkg = prefer_gpkg

        return

    @staticmethod
    def description():
        return "Extracts data from the Global Administrative Areas (GADM) at https://geodata.ucdavis.edu/gadm"

    def extract(self, country, level, year):

        cache_path = Path(config.get("cache_dir", Path.cwd())) / "gadm" / country
        cache_path.mkdir(parents=True, exist_ok=True)

        local_path = None
        downloaded = False

        # Try the geopackage first, then fall back to shapefile if it's not found
        if self.prefer_gpkg:
            gpkg = f"gadm41_{country}.gpkg"
            url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/{gpkg}"

            try:
                local_path = download_file(url, dest_dir=cache_path)
                logger.info(f"Downloaded GADM geopackage: {local_path}")
                downloaded = True

            except Exception as e:
                logger.warning(f"Failed to download GADM geopackage: {e}. Trying shapefile...")
                downloaded = False
                local_path = None

        if not downloaded:
            shp_zip = f"gadm41_{country}_shp.zip"
            url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/shp/{shp_zip}"

            try:
                local_path = download_file(url, dest_dir=cache_path)
                logger.info(f"Downloaded GADM shapefile zip: {local_path}")

                # Save the unzip for the transform step
                # But we could unzip here to check that the file is valid and contains data

                # Unzip the shapefile into the same directory

                with zipfile.ZipFile(local_path, "r") as zip_ref:
                    zip_ref.extractall(cache_path)

                downloaded = True

            except Exception as e:
                logger.error(
                    f"Failed to download GADM shapefile: {e}. No data available for {country}."
                )
                raise RuntimeError(f"Failed to download GADM data for {country}.") from e

        return local_path
