import unittest

from laser.init.extractors.gadm import GADMExtractor


class TestGADMExtractor(unittest.TestCase):
    def test_gadm_extractor_geopackage(self):
        extractor = GADMExtractor(prefer_gpkg=True)
        local_file = extractor.extract("MCO", 1, 2025)
        assert local_file.endswith("gadm41_MCO.gpkg")

        return

    def test_gadm_extractor_shapefile(self):
        extractor = GADMExtractor(prefer_gpkg=False)
        local_file = extractor.extract("MCO", 1, 2025)
        assert local_file.endswith("gadm41_MCO_shp.zip")

        return


if __name__ == "__main__":
    unittest.main()
