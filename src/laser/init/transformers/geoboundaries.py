"""
geoBoundaries shape data is available in GeoPackage format, so the transformation step is minimal.
We will filter the data by country and administrative level, and ensure that it is in a consistent
format for loading into our database.
"""

import geopandas as gpd

from ..utils import clip_quietly, inform, update_local_provenance


class GeoBoundariesTransformer:
    def __init__(self):
        """Initialize the GeoBoundaries transformer."""
        pass

    @staticmethod
    def description():
        """Return a brief description of this transformer.

        Returns:
            A string describing the transformation performed by this class.
        """
        return (
            "Transform geoBoundaries shape data by filtering for country and administrative level."
        )

    def transform(self, shape_file, iso_code, adm_level, raster_file, output_dir):
        """Transform GeoBoundaries administrative boundaries and combine with population data.

        Loads GeoBoundaries shape data from zip file, extracts relevant attributes,
        clips population raster data to administrative boundaries, and saves as a
        GeoPackage file.

        Args:
            shape_file: Path to the GeoBoundaries zip file.
            iso_code: ISO 3166-1 alpha-3 country code.
            adm_level: Administrative level to extract.
            raster_file: Path to the WorldPop population raster file.
            output_dir: Directory where output GeoPackage will be saved.

        Returns:
            Path to the output GeoPackage file.
        """

        # The geoBoundaries data is already constrained to the country and administrative level we want.
        # We should be able to use it directly with RasterToolkit.

        # Load the GeoPackage file using geopandas
        layer = f"geoBoundaries-{iso_code.upper()}-ADM{adm_level}"
        inform(f"Loading GeoBoundaries data from {shape_file} layer {layer}...")
        gdf = gpd.read_file(shape_file, layer=layer)

        gdf = gdf[["shapeName", "shapeID", "geometry"]]

        # Ensure "nodeid" and "name" columns
        gdf["nodeid"] = list(range(len(gdf)))
        gdf["name"] = gdf["shapeName"]

        subfile = f"geoBoundaries-{iso_code.upper()}-ADM{adm_level}.shp"
        pop_dict = clip_quietly(raster_file, shape_file / subfile, shape_attr="shapeID")
        gdf["population"] = gdf["shapeID"].map(pop_dict)

        output_filename = output_dir / f"{iso_code}_admin{adm_level}.gpkg"
        gdf.to_file(output_filename, driver="GPKG")
        update_local_provenance(output_dir, output_filename, shape_file, raster_file)
        inform(f"GeoBoundaries transform complete: {output_filename}")

        return output_filename
