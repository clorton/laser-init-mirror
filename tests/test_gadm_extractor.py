import unittest

from laser.init.extractors.gadm import GadmExtractor


class TestGadmExtractor(unittest.TestCase):
    def test_gadm_extractor_geopackage(self):
        extractor = GadmExtractor(prefer_gpkg=True)
        local_file = extractor.extract("MCO", 1, 2025)
        assert str(local_file).endswith("gadm41_MCO.gpkg")

        return

    def test_Gadm_extractor_shapefile(self):
        extractor = GadmExtractor(prefer_gpkg=False)
        local_file = extractor.extract("MCO", 1, 2025)
        assert str(local_file).endswith("gadm41_MCO_shp.zip")

        return


if __name__ == "__main__":
    unittest.main()
