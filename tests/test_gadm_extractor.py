import unittest

from laser.init.extractors.gadm import GadmExtractor


class TestGadmExtractor(unittest.TestCase):
    def test_gadm_extractor_geopackage(self):
        """Test GADM extractor with GeoPackage preference.

        Given a GadmExtractor configured to prefer GeoPackage format,
        when extracting data for Monaco at admin level 1,
        then the downloaded file should be a .gpkg file.

        Failure indicates the extractor is not correctly downloading or
        identifying GeoPackage files from GADM.
        """
        extractor = GadmExtractor(prefer_gpkg=True)
        local_file = extractor.extract("MCO", 1, 2025)
        assert str(local_file).endswith("gadm41_MCO.gpkg")

        return

    def test_Gadm_extractor_shapefile(self):
        """Test GADM extractor with shapefile preference.

        Given a GadmExtractor configured to prefer shapefile format,
        when extracting data for Monaco at admin level 1,
        then the downloaded file should be a .zip file containing shapefiles.

        Failure indicates the extractor is not correctly downloading or
        identifying shapefile archives from GADM.
        """
        extractor = GadmExtractor(prefer_gpkg=False)
        local_file = extractor.extract("MCO", 1, 2025)
        assert str(local_file).endswith("gadm41_MCO_shp.zip")

        return


if __name__ == "__main__":
    unittest.main()
