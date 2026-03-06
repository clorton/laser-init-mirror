"""
UNOCHA data transformer.

Unzip the downloaded file, load shape data, filter for country and administrative level, and save to GeoPackage format.

We use GeoPackage since it is a single file rather than a directory (geodatabase) or set of files (.shp).
"""

import warnings
import zipfile

import geopandas as gpd
from tqdm import tqdm

from ..logger import logger


class UnochaTransformer:
    def __init__(self):
        pass

    @staticmethod
    def description():
        return "Transform UNOCHA shape data to GeoPackage format, filtered by country and administrative level."

    def transform(self, shape_file, iso_code, adm_level, raster_file):

        if shape_file.suffix != ".zip":
            logger.error(f"Expected a .zip file for UNOCHA shape data, got: {shape_file}")
            raise ValueError("Invalid shape file format")

        # Determine the UNOCHA directory name from the shape file path
        # The directory name is the shape file path without the .zip extension

        source_dir = shape_file.parent
        # The extracted directory should contain a .gdb file with the same name as the directory
        # stem does _not_ include the suffix, so it will give us the directory name without the .zip extension
        gdb_dir = source_dir / shape_file.stem

        if not gdb_dir.exists():
            logger.info(f"Extracting {shape_file} to {source_dir}...")
            with zipfile.ZipFile(shape_file, "r") as zip_ref:
                members = zip_ref.infolist()
                for member in tqdm(members, desc="Extracting UNOCHA zip", unit="file"):
                    zip_ref.extract(member, path=source_dir)

        if not gdb_dir.exists():
            logger.error(f"Expected a .gdb file in the extracted UNOCHA directory, got: {gdb_dir}")
            raise ValueError("Missing .gdb file in extracted UNOCHA data")

        # Load the .gdb file using geopandas, ignoring specific RuntimeWarning
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=r"organizePolygons\(\) received a polygon with more than 100 parts.  The processing may be really slow.  You can skip the processing by setting METHOD=SKIP.",
                category=RuntimeWarning,
            )
            gdf = gpd.read_file(gdb_dir, layer=f"admin{adm_level}")

        return
