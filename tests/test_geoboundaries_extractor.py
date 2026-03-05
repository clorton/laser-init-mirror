import unittest

from laser.init.extractors.geoboundaries import GeoBoundariesExtractor


class TestGeoBoundariesExtractor(unittest.TestCase):
    def test_geoboundaries_extractor(self):
        extractor = GeoBoundariesExtractor()
        local_file = extractor.extract("MCO", 1, 2025)
        assert local_file.endswith("geoBoundaries-MCO-ADM1-all.zip")

        local_file = extractor.extract("VAT", 0, 2025)
        assert local_file.endswith("geoBoundaries-VAT-ADM0-all.zip")

        return


if __name__ == "__main__":
    unittest.main()
