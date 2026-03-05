import unittest

from laser.init import __version__
from laser.init.config import VERSION


class TestConfig(unittest.TestCase):
    def test_version(self):
        """Test that the version in config.py matches the package version."""
        self.assertEqual(VERSION, __version__)

        return


if __name__ == "__main__":
    unittest.main()
