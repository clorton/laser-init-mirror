"""
Transform UNWPP demographic data to a usable format, filtered by country and year range.
"""

import numpy as np
import pandas as pd

from ..utils import inform


class UnwppTransformer:
    def __init__(self):
        pass

    @staticmethod
    def description():
        return "Transform UNWPP demographic data to a usable format, filtered by country and year range."

    def transform(self, stats_data, iso_code, start_year, end_year, output_dir):

        # stats_data is a tuple with the following entries:
        # population by 5 year age group .csv.gz
        # demographic_indicators .csv.gz
        # life table, both sexes 1950-2023 .csv.gz
        # life table, both sexes 2024-2100 .csv.gz

        # CBR (start_year ... end_year) from demographic_indicators .csv.gz
        # CDR/CMR (start_year ... end_year) from demographic_indicators .csv.gz
        demo_filename = stats_data[1]
        inform(f"Loading demographic indicators from {demo_filename}")
        demo_df = pd.read_csv(
            demo_filename,
            compression="gzip",
            dtype={"Notes": str, "ISO3_code": str, "ISO2_code": str, "LocTypeName": str},
        )
        country_df = demo_df[demo_df["ISO3_code"] == iso_code]
        years_df = country_df[country_df.Time.isin(range(start_year, end_year + 1))]
        years_df = years_df.sort_values("Time").reset_index(drop=True)

        cbr_cdr = years_df[["Time", "CBR", "CDR"]]
        cxr_filename = output_dir / "cxr.csv"
        cbr_cdr.to_csv(cxr_filename, index=False)
        inform(f"Saved CBR/CDR data to {cxr_filename}")

        # Population distribution by age (as of start_year) from population by 5 year age group .csv.gz
        pop_filename = stats_data[0]
        inform(f"Loading population data from {pop_filename}")
        pop_df = pd.read_csv(
            pop_filename,
            compression="gzip",
            dtype={"Notes": str, "ISO3_code": str, "ISO2_code": str, "LocTypeName": str},
        )
        country_df = pop_df[pop_df["ISO3_code"] == iso_code]
        age_dist_df = (
            country_df[country_df.Time == start_year]
            .sort_values("AgeGrpStart")
            .reset_index(drop=True)
        )
        age_dist_df = age_dist_df[["AgeGrpStart", "PopTotal"]]
        pop_filename = output_dir / "age_dist.csv"
        age_dist_df.to_csv(pop_filename, index=False)
        inform(f"Saved age distribution data to {pop_filename}")

        # Life expectancy (as of start_year) from life table(s) .csv.gz
        life_filename1 = stats_data[2]
        life_filename2 = stats_data[3] if len(stats_data) > 3 else None
        inform(f"Loading life expectancy data from {life_filename1}")
        life_df = pd.read_csv(
            life_filename1,
            compression="gzip",
            dtype={"Notes": str, "ISO3_code": str, "ISO2_code": str, "LocTypeName": str},
        )

        if life_filename2:
            inform(f"Loading additional life expectancy data from {life_filename2}")
            life_df2 = pd.read_csv(
                life_filename2,
                compression="gzip",
                dtype={"Notes": str, "ISO3_code": str, "ISO2_code": str, "LocTypeName": str},
            )
            life_df = pd.concat([life_df, life_df2], ignore_index=True)

        # Reference:
        # mx: Central death rate, nmx, for the age interval (x, x+n)
        # qx: Probability of dying (nqx), for an individual between age x and x+n
        # px: Probability of surviving, (npx), for an individual of age x to age x+n
        # lx: Number of survivors, (lx), at age (x) for 100000 births
        # dx: Number of deaths, (ndx), between ages x and x+n
        # Lx: Number of person-years lived, (nLx), between ages x and x+n
        # Sx: Survival ratio (nSx) corresponding to proportion of the life table population in age group (x, x+n) who are alive n year later
        # Tx: Person-years lived, (Tx), above age x
        # ex: Expectation of life (ex) at age x, i.e., average number of years lived subsequent to age x by those reaching age x
        # ax: Average number of years lived (nax) between ages x and x+n by those dying in the interval

        country_df = life_df[life_df["ISO3_code"] == iso_code]
        life_exp_df = (
            country_df[country_df.Time == start_year]
            .sort_values("AgeGrpStart")
            .reset_index(drop=True)
        )
        survival = life_exp_df.lx.to_numpy()
        cumulative = 100_000 - np.round(survival)
        cumulative = np.append(cumulative[1:], 100_000)
        life_exp_df["cumulative_deaths"] = cumulative
        life_exp = output_dir / "life_exp.csv"
        life_exp_df[["cumulative_deaths"]].to_csv(life_exp, index=False)
        inform("Finished loading demographics stats.")

        return cxr_filename, pop_filename, life_exp
