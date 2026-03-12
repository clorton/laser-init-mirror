import unittest

from laser.init.extractors.geoboundaries import GeoBoundariesExtractor


class TestGeoBoundariesExtractor(unittest.TestCase):
    def test_geoboundaries_extractor(self):
        """Test GeoBoundaries extractor for multiple countries and admin levels.

        Given a GeoBoundariesExtractor instance,
        when extracting data for Monaco (MCO) at admin level 1 and Vatican (VAT) at level 0,
        then the downloaded files should have the correct GeoBoundaries naming convention.

        Failure indicates the extractor is not correctly constructing URLs or
        downloading files from the GeoBoundaries repository.
        """
        extractor = GeoBoundariesExtractor()
        local_file = extractor.extract("MCO", 1, 2025)
        assert str(local_file).endswith("geoBoundaries-MCO-ADM1-all.zip")

        local_file = extractor.extract("VAT", 0, 2025)
        assert str(local_file).endswith("geoBoundaries-VAT-ADM0-all.zip")

        return


if __name__ == "__main__":
    unittest.main()
