"""
Docstring for laser.init.extractors.worldpop

https://www.worldpop.org

Examples:

## 2015...2030 1km
Algeria 2015: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2015/DZA/v1/1km_ua/constrained/dza_pop_2015_CN_1km_R2025A_UA_v1.tif
Algeria 2016: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2016/DZA/v1/1km_ua/constrained/dza_pop_2016_CN_1km_R2025A_UA_v1.tif
Algeria 2017: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2017/DZA/v1/1km_ua/constrained/dza_pop_2017_CN_1km_R2025A_UA_v1.tif
Nigeria 2015: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2015/NGA/v1/1km_ua/constrained/nga_pop_2015_CN_1km_R2025A_UA_v1.tif
Nigeria 2020: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2020/NGA/v1/1km_ua/constrained/nga_pop_2020_CN_1km_R2025A_UA_v1.tif
Nigeria 2025: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/NGA/v1/1km_ua/constrained/nga_pop_2025_CN_1km_R2025A_UA_v1.tif

## 2000...2020 1km
Kenya 2000: https://data.worldpop.org/GIS/Population/Global_2000_2020_1km_UNadj/2000/KEN/ken_ppp_2000_1km_Aggregated_UNadj.tif
Kenya 2005: https://data.worldpop.org/GIS/Population/Global_2000_2020_1km_UNadj/2005/KEN/ken_ppp_2005_1km_Aggregated_UNadj.tif
Kenya 2010: https://data.worldpop.org/GIS/Population/Global_2000_2020_1km_UNadj/2010/KEN/ken_ppp_2010_1km_Aggregated_UNadj.tif
Nigeria 2000: https://data.worldpop.org/GIS/Population/Global_2000_2020_1km_UNadj/2000/NGA/nga_ppp_2000_1km_Aggregated_UNadj.tif
Nigeria 2005: https://data.worldpop.org/GIS/Population/Global_2000_2020_1km_UNadj/2005/NGA/nga_ppp_2005_1km_Aggregated_UNadj.tif
Nigeria 2010: https://data.worldpop.org/GIS/Population/Global_2000_2020_1km_UNadj/2010/NGA/nga_ppp_2010_1km_Aggregated_UNadj.tif
"""

from pathlib import Path

from ..config import configuration as config
from ..utils import download_file, error, inform


class WorldPopExtractor:
    def __init__(self) -> None:
        """Initialize the WorldPop extractor."""
        pass

    @staticmethod
    def description() -> str:
        """Return a brief description of this extractor.

        Returns:
            A string describing the data source and purpose of this extractor.
        """
        return "Extracts data from WorldPop at https://www.worldpop.org"

    def extract(self, country, year) -> Path | None:
        """Extract WorldPop population raster data for a country and year.

        Downloads gridded population data at 1km resolution. Automatically
        selects the appropriate dataset based on the year:
        - 2015-2030: Uses Global_2015_2030/R2025A dataset
        - 2000-2014: Uses Global_2000_2020_1km_UNadj dataset

        Args:
            country: ISO 3166-1 alpha-3 country code (e.g., "NGA" for Nigeria).
            year: Year for the population data (must be 2000-2030).

        Returns:
            Path to the downloaded GeoTIFF raster file, or None if download failed.

        Raises:
            ValueError: If year is outside the valid range (2000-2030).
            RuntimeError: If the download fails.
        """

        if year < 2000 or year > 2030:
            error(f"Year {year} is out of range for WorldPop data (2000-2030).", ValueError)

        local_path = None

        cache_root = Path(config.get("cache_dir", Path.cwd()))
        worldpop_path: Path = Path("WorldPop")
        (cache_root / worldpop_path).mkdir(parents=True, exist_ok=True)

        if year >= 2015:  # Use newer data
            inform(f"Using WorldPop 2015-2030 dataset for year {year}.")

            tiff_file = f"{country.lower()}_pop_{year}_CN_1km_R2025A_UA_v1.tif"
            url: str = f"https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/{year}/{country}/v1/1km_ua/constrained/{tiff_file}"

            try:
                local_path: Path = download_file(url, cache_dir=cache_root, dest_dir=worldpop_path)
                inform(f"Downloaded WorldPop data: {local_path}")

            except Exception as e:
                error(f"Failed to download WorldPop data: {e}.", RuntimeError)

        elif year >= 2000:  # Use older data
            inform(f"Using WorldPop 2000-2020 data set for year {year}.")

            tiff_file = f"{country.lower()}_ppp_{year}_1km_Aggregated_UNadj.tif"
            url: str = f"https://data.worldpop.org/GIS/Population/Global_2000_2020_1km_UNadj/{year}/{country}/{tiff_file}"

            try:
                local_path: Path = download_file(url, cache_dir=cache_root, dest_dir=worldpop_path)
                inform(f"Downloaded WorldPop data: {local_path}")

            except Exception as e:
                error(f"Failed to download WorldPop data: {e}.", RuntimeError)

        else:
            error(f"Year {year} is out of range for WorldPop data (2000-2030).", RuntimeError)

        return local_path
