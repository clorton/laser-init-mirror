from pathlib import Path

import click
import geopandas as gpd
import laser.core.distributions as dists
import numpy as np
import pandas as pd
import yaml
from laser.core import PropertySet
from laser.core.demographics import AliasedDistribution, KaplanMeierEstimator
from laser.generic import SI, Model
from laser.generic.utils import ValuesMap
from laser.generic.vitaldynamics import BirthsByCBR, MortalityByEstimator
from plot import show_plots


@click.command()
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=True),
    default=Path(__file__).parent / "config.yaml",
    help="Path to the configuration YAML file.",
)
@click.option(
    "-d",
    "--data-dir",
    type=click.Path(exists=True),
    default=None,
    help="Path to the data directory.",
)
def main(config_file, data_dir):
    """Run an SI (Susceptible-Infectious) epidemiological model.

    Loads configuration and data files, sets up the model with vital dynamics
    (births and mortality), runs the simulation, and generates output plots.

    Args:
        config_file: Path to the YAML configuration file.
        data_dir: Path to the data directory, or None to use config value.

    Returns:
        None
    """
    config = yaml.safe_load(config_file.read_text())

    data_dir = Path(data_dir or config["data-dir"])
    datafiles = config["datafiles"]
    scenario = gpd.read_file(data_dir / datafiles["shape-data"])
    cxr_df = pd.read_csv(data_dir / datafiles["cxr-data"])  # "cxr.csv")
    pop_df = pd.read_csv(data_dir / datafiles["pop-data"])  # "age_dist.csv")
    exp_df = pd.read_csv(data_dir / datafiles["exp-data"])  # "life_exp.csv")

    sim_params = config["simulation"]
    EXPOSED_DURATION_SHAPE = sim_params["exposed-duration-shape"]
    EXPOSED_DURATION_SCALE = sim_params["exposed-duration-scale"]
    INFECTIOUS_DURATION_MEAN = sim_params["infectious-duration-mean"]
    NYEARS = sim_params["nyears"]
    NTICKS = 365 * NYEARS
    R0 = sim_params["r0"]

    scenario["nodeid"] = np.arange(len(scenario), dtype=np.int32)
    scenario["S"] = scenario.population
    scenario["E"] = 0
    scenario["I"] = 0
    # seed the largest population center with some initial infections
    imax = np.argmax(scenario.population)
    scenario.at[imax, "I"] = 50
    scenario["R"] = 0
    scenario.S -= scenario.I + scenario.R

    cbr = cxr_df.CBR.to_numpy()
    if len(cbr) < NYEARS:
        cbr = np.pad(cbr, (0, NYEARS - len(cbr)), mode="edge")
    daily_cbr = np.repeat(cbr[0:NYEARS], 365)
    birthrates = ValuesMap.from_timeseries(daily_cbr, len(scenario))

    params = PropertySet(
        {
            "exposed_duration_shape": EXPOSED_DURATION_SHAPE,
            "exposed_duration_scale": EXPOSED_DURATION_SCALE,
            "infectious_duration_mean": INFECTIOUS_DURATION_MEAN,
            "nyears": NYEARS,
            "nticks": NTICKS,
            "r0": R0,
            "beta": R0 / INFECTIOUS_DURATION_MEAN,
        }
    )

    model = Model(scenario, params, birthrates=birthrates)

    infdist = dists.normal(loc=INFECTIOUS_DURATION_MEAN, scale=2)

    s = SI.Susceptible(model)
    i = SI.Infectious(model, infdist)
    tx = SI.Transmission(model)

    pyramid = AliasedDistribution(pop_df.PopTotal.to_numpy())
    survival = KaplanMeierEstimator(exp_df.cumulative_deaths.to_numpy())

    births = BirthsByCBR(model, birthrates, pyramid)
    mortality = MortalityByEstimator(model, survival)
    model.components = [s, i, tx, births, mortality]

    model.run()

    show_plots(model, output_dir=Path(__file__).parent)

    return


if __name__ == "__main__":
    main()
