"""
Docstring for laser.init.extractors.geoboundaries

E.g., https://github.com/wmgeolab/geoBoundaries/raw/refs/heads/main/releaseData/gbOpen/USA/ADM0/geoBoundaries-USA-ADM0-all.zip
"""


class GeoBoundariesExtractor:
    def __init__(self):
        pass

    @staticmethod
    def description():
        return "Extracts data from GeoBoundaries at https://www.github.com/wmgeolab/geoBoundaries"

    def extract(self, country, level, year):
        pass
