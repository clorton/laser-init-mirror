"""
GADM shape data is available in various formats, including GeoPackage and Shapefile.
We will filter the data by country and administrative level, and ensure that it is in a consistent
format for loading into our database.
"""

import geopandas as gpd

from ..utils import clip_quietly, error, inform, update_local_provenance


class GadmTransformer:
    def __init__(self):
        pass

    @staticmethod
    def description():
        return "Transform GADM shape data by filtering for country and administrative level."

    def transform(self, shape_file, iso_code, adm_level, raster_file, output_dir):

        if shape_file.suffix == ".zip":
            inform(f"Processing GADM shape file from zip archive: {shape_file}")
            shape_filepath = shape_file / f"gadm41_{iso_code.upper()}_{adm_level}.shp"
        elif shape_file.suffix == ".gpkg":
            inform(f"Shape file is not a zip archive, proceeding with {shape_file}")
            raise NotImplementedError(
                "GADM GeoPackage format is not yet supported. Please provide a zip file containing the shapefile."
            )
        else:
            error(f"Unsupported shape file format: {shape_file.suffix}", ValueError)

        inform(
            f"Loading GADM data from {shape_file} layer gadm41_{iso_code.upper()}_{adm_level}..."
        )
        gdf = gpd.read_file(shape_file, layer=f"gadm41_{iso_code.upper()}_{adm_level}")
        names = [f"NAME_{i}" for i in range(1, adm_level + 1)]
        gid = f"GID_{adm_level}"
        gdf = gdf[names + [gid, "geometry"]]
        pop_dict = clip_quietly(raster_file, shape_filepath, shape_attr=gid)
        gdf["population"] = gdf[gid].map(pop_dict)

        output_filename = output_dir / f"{iso_code}_admin{adm_level}.gpkg"
        gdf.to_file(output_filename, driver="GPKG")
        update_local_provenance(output_dir, output_filename, shape_file, raster_file)
        inform(f"Saved GeoPackage: {output_filename}")

        inform(f"GADM transform complete: {output_filename}")
        return output_filename
