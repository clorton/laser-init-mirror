"""
Docstring for laser.init.extractors.gadm

https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_NGA.gpkg
https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_NGA_shp.zip
"""


class GADMExtractor:
    def __init__(self):
        pass

    @staticmethod
    def description():
        return "Extracts data from the Global Administrative Areas (GADM) at https://geodata.ucdavis.edu/gadm"

    def extract(self, country, level, year):

        # Try the geopackage first, then fall back to shapefile if it's not found

        return
