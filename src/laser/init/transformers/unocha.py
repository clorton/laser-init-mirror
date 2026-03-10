"""
UNOCHA data transformer.

Unzip the downloaded file, load shape data, filter for country and administrative level, and save to GeoPackage format.

We use GeoPackage since it is a single file rather than a directory (geodatabase) or set of files (.shp).
"""

import tempfile
import warnings
import zipfile
from pathlib import Path

import geopandas as gpd
from tqdm import tqdm

from ..utils import clip_quietly, error, inform, update_local_provenance


class UnochaTransformer:
    def __init__(self):
        pass

    @staticmethod
    def description():
        return "Transform UNOCHA shape data to GeoPackage format, filtered by country and administrative level."

    def transform(self, shape_file, iso_code, adm_level, raster_file, output_dir):

        inform(
            f"Starting UNOCHA transform with shape_file={shape_file}, iso_code={iso_code}, adm_level={adm_level}, raster_file={raster_file}, output_dir={output_dir}"
        )

        if shape_file.suffix != ".zip":
            error(f"Expected a .zip file for UNOCHA shape data, got: {shape_file}", ValueError)

        # Determine the UNOCHA directory name from the shape file path
        # The directory name is the shape file path without the .zip extension

        source_dir = shape_file.parent
        # The extracted directory should contain a .gdb file with the same name as the directory
        # stem does _not_ include the suffix, so it will give us the directory name without the .zip extension
        gdb_dir = source_dir / shape_file.stem

        if not gdb_dir.exists():
            inform(f"Extracting {shape_file} to {source_dir}...")
            with zipfile.ZipFile(shape_file, "r") as zip_ref:
                members = zip_ref.infolist()
                for member in tqdm(members, desc="Extracting UNOCHA zip", unit="file"):
                    zip_ref.extract(member, path=source_dir)
            inform(f"Zip extraction complete: {gdb_dir}")

        if not gdb_dir.exists():
            error(
                f"Expected a .gdb file in the extracted UNOCHA directory, got: {gdb_dir}",
                ValueError,
            )

        gdf = read_gbd_quietly(gdb_dir, layer_name=f"admin{adm_level}")

        inform(f"Loaded GeoDataFrame for admin{adm_level} from {gdb_dir}, {len(gdf)} features.")

        # We should already have the admin level we want, now filter to the country level using the ISO code
        country_gdf = gdf[gdf.iso3 == iso_code]
        inform(f"Filtered GeoDataFrame for iso_code={iso_code}: {len(country_gdf)} features.")
        if len(country_gdf) == 0:
            error(f"No features found for iso_code={iso_code} at admin{adm_level}.", ValueError)

        # Filter the columns we will not be using
        names = [f"adm{i}_name" for i in range(adm_level + 1)]
        pcode = f"adm{adm_level}_pcode"
        country_gdf = country_gdf[names + [pcode, "geometry"]]

        # Ensure "nodeid" and "name" columns
        gdf["nodeid"] = list(range(len(gdf)))
        if adm_level < 4:
            country_gdf["name"] = country_gdf[f"adm{adm_level}_name"]
        else:
            country_gdf["name"] = country_gdf.adm3_name + country_gdf.adm4_name

        # using tempfile, create a temp directory, write the GeoDataFrame to a shapefile (.shp) in
        # that directory and use it with RasterToolkit to clip the raster file
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_shapefile = Path(tmpdir) / f"{iso_code}_admin{adm_level}.shp"
            country_gdf.to_file(tmp_shapefile, driver="ESRI Shapefile", engine="pyogrio")
            inform(f"Wrote temporary shapefile: {tmp_shapefile}")
            # Now we can use this temporary shapefile with RasterToolkit to clip the raster file
            pop_dict = clip_quietly(raster_file, tmp_shapefile, shape_attr=pcode)
            inform(f"Clipped raster with {tmp_shapefile}, got {len(pop_dict)} population values.")

            # Add a new column, population, to the GeoDataFrame, and fill it with the matching
            # values from the pop_dict dictionary. The keys of pop_dict should match the values in
            # the pcode column of the GeoDataFrame, and the values in pop_dict should be the
            # population values from the raster file.
            country_gdf["population"] = country_gdf[pcode].map(pop_dict)

        # Save the filtered GeoDataFrame to a GeoPackage file in the output directory
        if output_dir.is_dir():
            output_filename = output_dir / f"{iso_code}_admin{adm_level}.gpkg"
            country_gdf.to_file(output_filename, driver="GPKG")
            update_local_provenance(output_dir, output_filename, shape_file, raster_file)
            inform(f"Saved GeoPackage: {output_filename}")
        else:
            error(f"Output directory {output_dir} is not a directory.", ValueError)

        inform(f"UNOCHA transform complete: {output_filename}")
        return output_filename


def read_gbd_quietly(gdb_path, layer_name):
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r"organizePolygons\(\) received a polygon with more than 100 parts.  The processing may be really slow.  You can skip the processing by setting METHOD=SKIP.",
            category=RuntimeWarning,
        )
        gdf = gpd.read_file(gdb_path, layer=layer_name)
    inform(f"Read GDB layer '{layer_name}' from {gdb_path}: {len(gdf)} features.")
    if len(gdf) == 0:
        inform(f"No features loaded from {gdb_path} layer '{layer_name}'.")

    return gdf
