"""
UN World Population Prospects (UNWPP) extractor

Standard Projections (Estimates and Projection scenarios) / CSV format : https://population.un.org/wpp/downloads?folder=Standard%20Projections&group=CSV%20format

## Demographic Indicators
[Indicator Reference](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_notes.csv)
[1950-2100 medium](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz)

## Fertility
[1950-2100 single age](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Fertility_by_Age1.csv.gz)
[1950-2100 five year](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Fertility_by_Age5.csv.gz)

## Life Tables
[1950-2023 single age](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Life_Table_Complete_Medium_Both_1950-2023.csv.gz)
[2024-2100 single age](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Life_Table_Complete_Medium_Both_2024-2100.csv.gz)

## Mortality
[1950-2023 single age](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_DeathsBySingleAgeSex_Medium_1950-2023.csv.gz)
[2024-2100 single age](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_DeathsBySingleAgeSex_Medium_2024-2100.csv.gz)

## Population
[1950-2100 five year medium](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Population1JanuaryByAge5GroupSex_Medium.csv.gz)
[1950-2023 single age medium](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Population1JanuaryBySingleAgeSex_Medium_1950-2023.csv.gz)
[2024-2100 single age medium](https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Population1JanuaryBySingleAgeSex_Medium_2024-2100.csv.gz)
"""

from pathlib import Path

from ..config import configuration as config
from ..utils import download_file, error, inform


class UnwppExtractor:
    def __init__(self) -> None:
        """Initialize the UNWPP extractor."""
        pass

    @staticmethod
    def description() -> str:
        """Return a brief description of this extractor.

        Returns:
            A string describing the data source and purpose of this extractor.
        """
        return "Extracts data from the UN World Population Prospects (UNWPP) at https://population.un.org/wpp/"

    def extract(self, country, start_year, end_year) -> Path | None:
        """Extract UN World Population Prospects demographic data.

        Downloads global demographic data files from UNWPP including:
        - Population by age group (5-year intervals)
        - Demographic indicators (CBR, CDR, etc.)
        - Life tables for mortality estimation

        The downloaded files contain data for all countries, which will be
        filtered in the transform step.

        Args:
            country: ISO 3166-1 alpha-3 country code (used for subsequent filtering).
            start_year: Start year for the data range (must be >= 1950).
            end_year: End year for the data range (must be <= 2100).

        Returns:
            Tuple of Paths: (age_distribution_file, demographic_indicators_file,
                life_table_1950_2023_file, life_table_2024_2100_file).
                The life table files may be None if not needed for the year range.

        Raises:
            ValueError: If start_year < 1950 or end_year > 2100.
            RuntimeError: If any required download fails.
        """

        if start_year < 1950 or end_year > 2100:
            error(
                f"Year range {start_year}-{end_year} is out of range for UNWPP data (1950-2100).",
                ValueError,
            )

        # UNWPP data is provided as large CSV files covering all countries, so we download the relevant
        # files and then filter them locally (in the transformer) for the specified country and year range.

        cache_root = Path(config.get("cache_dir", Path.cwd()))
        unwpp_path = Path("UNWPP")
        (cache_root / unwpp_path).mkdir(parents=True, exist_ok=True)

        # Age distribution data (5-year age groups)
        dist_file = "WPP2024_Population1JanuaryByAge5GroupSex_Medium.csv.gz"
        url = f"https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/{dist_file}"

        try:
            local_dist = download_file(url, cache_dir=cache_root, dest_dir=unwpp_path)
            inform(f"Downloaded UNWPP age distribution data: {local_dist}")
        except Exception as e:
            error(f"Failed to download UNWPP age distribution data: {e}.", RuntimeError)

        # CBR and CDR (CMR)
        cxr_file = "WPP2024_Demographic_Indicators_Medium.csv.gz"
        url = f"https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/{cxr_file}"

        try:
            local_cxr = download_file(url, cache_dir=cache_root, dest_dir=unwpp_path)
            inform(f"Downloaded UNWPP demographic indicators data: {local_cxr}")
        except Exception as e:
            error(f"Failed to download UNWPP demographic indicators data: {e}.", RuntimeError)

        local_life1 = None
        local_life2 = None

        # Survival data (life tables)
        if start_year <= 2023:
            life_file1 = "WPP2024_Life_Table_Complete_Medium_Both_1950-2023.csv.gz"
            url = f"https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/{life_file1}"

            try:
                local_life1 = download_file(url, cache_dir=cache_root, dest_dir=unwpp_path)
                inform(f"Downloaded UNWPP life table data (1950-2023): {local_life1}")
            except Exception as e:
                error(f"Failed to download UNWPP life table data (1950-2023): {e}.", RuntimeError)

        if end_year >= 2024:
            life_file2 = "WPP2024_Life_Table_Complete_Medium_Both_2024-2100.csv.gz"
            url = f"https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/{life_file2}"

            try:
                local_life2 = download_file(url, cache_dir=cache_root, dest_dir=unwpp_path)
                inform(f"Downloaded UNWPP life table data (2024-2100): {local_life2}")
            except Exception as e:
                error(f"Failed to download UNWPP life table data (2024-2100): {e}.", RuntimeError)

        return (local_dist, local_cxr, local_life1, local_life2)
