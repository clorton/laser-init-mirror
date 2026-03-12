# Examples Directory Plan (#10)

Comprehensive plan for creating an `examples/` directory with practical, educational examples for laser-init users.

## Overview

The examples directory will provide ready-to-run scripts and notebooks demonstrating common workflows, best practices, and advanced usage patterns.

## Directory Structure

```
examples/
├── README.md                          # Index of all examples
├── basic/                             # Basic usage examples
│   ├── 01_quick_start.sh             # Simplest possible use case
│   ├── 02_data_source_comparison.sh  # Compare UNOCHA vs GADM vs geoBoundaries
│   └── 03_custom_parameters.sh       # Modify model parameters
├── workflows/                         # Complete workflows
│   ├── multi_country_analysis.sh     # Batch process multiple countries
│   ├── time_series_comparison.py     # Compare different time periods
│   └── sensitivity_analysis.py       # Parameter sensitivity sweep
├── data_integration/                  # Working with output data
│   ├── geopackage_analysis.py        # Load and analyze GeoPackage
│   ├── custom_visualization.py       # Custom plots and maps
│   └── export_to_qgis.py            # Prepare data for QGIS
├── model_customization/               # Extending models
│   ├── add_vaccination.py            # Add vaccination intervention
│   ├── social_distancing.py          # Model social distancing
│   ├── age_structured_seir.py        # Age-stratified model
│   └── seirs_waning_immunity.py      # SEIRS with waning immunity
├── advanced/                          # Advanced techniques
│   ├── calibration_example.py        # Calibrate to historical data
│   ├── uncertainty_quantification.py # Parameter uncertainty analysis
│   └── parallel_scenarios.py         # Run multiple scenarios in parallel
└── notebooks/                         # Jupyter notebooks
    ├── 01_getting_started.ipynb      # Interactive tutorial
    ├── 02_data_exploration.ipynb     # Explore output data
    ├── 03_model_comparison.ipynb     # Compare SI/SIR/SEIR
    └── 04_custom_analysis.ipynb      # End-to-end custom analysis
```

## Example Descriptions

### Basic Examples

#### 01_quick_start.sh
```shell
#!/bin/bash
# Simplest possible laser-init workflow
# Downloads data for Nigeria at district level and runs model

laser-init NGA 2 2010 2020
cd NGA/2010
python seir.py
```

**Learning objectives**:
- Understand basic command syntax
- See what files are generated
- Run a simulation

#### 02_data_source_comparison.sh
```shell
#!/bin/bash
# Compare different shapefile sources for the same country

# UNOCHA (humanitarian focus)
laser-init MWI 2 2015 2020 --shape-source unocha --output-dir MWI/unocha

# geoBoundaries (academic)
laser-init MWI 2 2015 2020 --shape-source geoboundaries --output-dir MWI/geoboundaries

# GADM (comprehensive)
laser-init MWI 2 2015 2020 --shape-source gadm --output-dir MWI/gadm

# Compare population maps
echo "Comparing population distributions..."
python compare_sources.py MWI/*/2015/*.gpkg
```

**Learning objectives**:
- Understand data source differences
- See impact of source choice on results
- Learn when to use each source

#### 03_custom_parameters.sh
```shell
#!/bin/bash
# Generate model with custom parameters

laser-init KEN 2 2015 2020

# Edit parameters
cd KEN/2015
sed -i 's/r0: 2.5/r0: 4.0/' config.yaml
sed -i 's/infectious-duration-mean: 7.0/infectious-duration-mean: 5.0/' config.yaml

# Run with custom parameters
python seir.py

echo "Simulation complete with R0=4.0, duration=5 days"
```

**Learning objectives**:
- Modify model parameters
- Understand parameter effects
- Iterate on model runs

### Workflows

#### multi_country_analysis.sh
```shell
#!/bin/bash
# Analyze multiple countries in West Africa

countries=("NGA" "GHA" "SEN" "CIV" "MLI")
level=2
start_year=2010
end_year=2020

for country in "${countries[@]}"; do
    echo "Processing $country..."
    laser-init "$country" "$level" "$start_year" "$end_year" \
        --output-dir "west_africa/$country/$start_year"

    # Run model
    cd "west_africa/$country/$start_year"
    python seir.py
    cd -
done

# Generate comparative report
python generate_regional_report.py west_africa/
```

**Learning objectives**:
- Batch processing
- Regional analysis
- Comparative epidemiology

#### time_series_comparison.py
```python
"""Compare population and demographics across time periods."""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load data from different time periods
periods = [2000, 2010, 2020]
data = {}

for year in periods:
    gdf = gpd.read_file(f"PAK/{year}/PAK_admin2.gpkg")
    data[year] = gdf

# Calculate population growth
growth = pd.DataFrame({
    year: data[year].groupby("name")["population"].sum()
    for year in periods
})

# Plot growth rates
growth_pct = growth.pct_change(axis=1) * 100
growth_pct.plot(kind="box", title="Population Growth by District (%)")
plt.ylabel("Growth Rate (%)")
plt.savefig("population_growth_analysis.png")

print(f"National population growth 2000-2020: {growth.sum().pct_change().iloc[-1]*100:.1f}%")
```

**Learning objectives**:
- Temporal analysis
- Population growth patterns
- Long-term demographic changes

#### sensitivity_analysis.py
```python
"""Run sensitivity analysis on key model parameters."""

import subprocess
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Generate base model
subprocess.run(["laser-init", "ETH", "2", "2015", "2020"])

# Parameter ranges to test
r0_values = [1.5, 2.0, 2.5, 3.0, 4.0]
duration_values = [5, 7, 10, 14]

results = []

for r0 in r0_values:
    for duration in duration_values:
        # Create scenario directory
        scenario_dir = Path(f"ETH/2015/scenarios/r0_{r0}_dur_{duration}")
        scenario_dir.mkdir(parents=True, exist_ok=True)

        # Copy files and modify config
        # ... (implementation details)

        # Run model
        subprocess.run(["python", "seir.py"], cwd=scenario_dir)

        # Extract results
        # ... (parse output)

        results.append({
            "r0": r0,
            "duration": duration,
            "peak_day": peak_day,
            "attack_rate": attack_rate
        })

# Visualize sensitivity
results_df = pd.DataFrame(results)
pivot = results_df.pivot(index="r0", columns="duration", values="attack_rate")
plt.figure(figsize=(10, 6))
plt.imshow(pivot, cmap="RdYlGn_r", aspect="auto")
plt.colorbar(label="Attack Rate")
plt.title("Sensitivity Analysis: Attack Rate by R0 and Duration")
plt.xlabel("Infectious Duration (days)")
plt.ylabel("R0")
plt.savefig("sensitivity_analysis.png")
```

**Learning objectives**:
- Parameter uncertainty
- Sensitivity analysis
- Scenario planning

### Data Integration

#### geopackage_analysis.py
```python
"""Detailed analysis of GeoPackage output."""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load GeoPackage
gdf = gpd.read_file("NGA/2010/NGA_admin2.gpkg")

# Summary statistics
print(f"Total districts: {len(gdf)}")
print(f"Total population: {gdf.population.sum():,.0f}")
print(f"Population density (per km²): {gdf.population.sum() / (gdf.geometry.area.sum() / 1e6):,.1f}")

# Find population extremes
print(f"\nMost populous: {gdf.nlargest(5, 'population')[['name', 'population']]}")
print(f"\nLeast populous: {gdf.nsmallest(5, 'population')[['name', 'population']]}")

# Calculate density
gdf["area_km2"] = gdf.geometry.area / 1e6
gdf["density"] = gdf.population / gdf.area_km2

# Plot distribution
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

gdf.plot(column="population", ax=axes[0], legend=True, cmap="YlOrRd")
axes[0].set_title("Population")
axes[0].axis("off")

gdf.plot(column="density", ax=axes[1], legend=True, cmap="plasma")
axes[1].set_title("Density (per km²)")
axes[1].axis("off")

gdf.plot(column="area_km2", ax=axes[2], legend=True, cmap="viridis")
axes[2].set_title("Area (km²)")
axes[2].axis("off")

plt.tight_layout()
plt.savefig("geospatial_analysis.png")
```

**Learning objectives**:
- Load and analyze GeoPackage
- Spatial statistics
- Custom visualizations

#### custom_visualization.py
```python
"""Create publication-quality visualizations."""

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import contextily as cx

# Load data
gdf = gpd.read_file("KEN/2015/KEN_admin2.gpkg")

# Reproject for basemap
gdf_web = gdf.to_crs(epsg=3857)

# Create figure
fig, ax = plt.subplots(figsize=(12, 10))

# Plot population with log scale
gdf_web.plot(
    column="population",
    ax=ax,
    legend=True,
    cmap="YlOrRd",
    edgecolor="black",
    linewidth=0.5,
    norm=LogNorm(vmin=gdf.population.min(), vmax=gdf.population.max()),
    legend_kwds={"label": "Population (log scale)"}
)

# Add basemap
cx.add_basemap(ax, source=cx.providers.CartoDB.Positron, alpha=0.5)

# Styling
ax.set_title("Kenya Population Distribution (2015)", fontsize=16, fontweight="bold")
ax.axis("off")

plt.tight_layout()
plt.savefig("kenya_population_publication.png", dpi=300, bbox_inches="tight")
```

**Learning objectives**:
- Publication-quality figures
- Basemap integration
- Advanced matplotlib

### Model Customization

#### add_vaccination.py
```python
"""Add vaccination campaign to SEIR model."""

# (Copy of SEIR model with vaccination intervention added)
# Full working example with detailed comments

class VaccinationCampaign:
    """Implements a vaccination campaign intervention.

    Args:
        model: LASER model instance
        start_day: Day to begin vaccination
        daily_rate: Fraction of susceptibles vaccinated per day
        efficacy: Vaccine efficacy (0-1)
        target_coverage: Stop when this fraction is vaccinated
    """
    def __init__(self, model, start_day, daily_rate, efficacy, target_coverage):
        self.model = model
        self.start_day = start_day
        self.daily_rate = daily_rate
        self.efficacy = efficacy
        self.target_coverage = target_coverage
        self.total_vaccinated = 0

    def apply(self):
        if self.model.tick < self.start_day:
            return

        current_coverage = self.total_vaccinated / self.model.scenario.population.sum()
        if current_coverage >= self.target_coverage:
            return

        # Vaccinate fraction of remaining susceptibles
        to_vaccinate = (self.model.scenario.S * self.daily_rate).astype(int)
        effective = (to_vaccinate * self.efficacy).astype(int)

        self.model.scenario.S -= effective
        self.model.scenario.R += effective
        self.total_vaccinated += effective.sum()

# Add to model
vaccination = VaccinationCampaign(
    model,
    start_day=180,  # Start at day 180
    daily_rate=0.01,  # Vaccinate 1% of susceptibles per day
    efficacy=0.9,  # 90% effective
    target_coverage=0.7  # Stop at 70% coverage
)
model.components.append(vaccination)
```

**Learning objectives**:
- Intervention modeling
- Custom LASER components
- Vaccination campaigns

### Advanced Examples

#### calibration_example.py
```python
"""Calibrate model parameters to historical outbreak data."""

import numpy as np
from scipy.optimize import minimize
from pathlib import Path

# Load historical data
historical_cases = pd.read_csv("historical_ebola_cases.csv")

def run_model(r0, duration):
    """Run model with given parameters and return simulated cases."""
    # Modify config, run model, extract results
    # ...
    return simulated_cases

def objective(params):
    """Objective function: sum of squared errors."""
    r0, duration = params
    simulated = run_model(r0, duration)

    # Compare to historical data
    error = np.sum((simulated - historical_cases.values) ** 2)
    return error

# Calibrate
initial_guess = [2.5, 10.0]
bounds = [(1.0, 5.0), (5.0, 20.0)]

result = minimize(
    objective,
    initial_guess,
    method="L-BFGS-B",
    bounds=bounds
)

print(f"Calibrated R0: {result.x[0]:.2f}")
print(f"Calibrated duration: {result.x[1]:.1f} days")
print(f"Final error: {result.fun:.2f}")
```

**Learning objectives**:
- Model calibration
- Optimization techniques
- Historical data fitting

## Implementation Plan

### Phase 1: Basic Examples (Week 1)
- [ ] Create examples directory structure
- [ ] Write basic/ examples (01-03)
- [ ] Test all basic examples
- [ ] Write examples/README.md

### Phase 2: Workflows (Week 2)
- [ ] Implement multi_country_analysis.sh
- [ ] Implement time_series_comparison.py
- [ ] Implement sensitivity_analysis.py
- [ ] Add supporting utilities

### Phase 3: Data Integration (Week 3)
- [ ] Implement geopackage_analysis.py
- [ ] Implement custom_visualization.py
- [ ] Implement export_to_qgis.py
- [ ] Add sample data if needed

### Phase 4: Model Customization (Week 4)
- [ ] Implement add_vaccination.py
- [ ] Implement social_distancing.py
- [ ] Implement age_structured_seir.py
- [ ] Implement seirs_waning_immunity.py

### Phase 5: Advanced Examples (Week 5)
- [ ] Implement calibration_example.py
- [ ] Implement uncertainty_quantification.py
- [ ] Implement parallel_scenarios.py
- [ ] Performance optimization

### Phase 6: Notebooks (Week 6)
- [ ] Create Jupyter notebooks (01-04)
- [ ] Add interactive widgets
- [ ] Test notebooks
- [ ] Add binder/colab links

### Phase 7: Documentation & Polish (Week 7)
- [ ] Write comprehensive examples/README.md
- [ ] Add comments and docstrings
- [ ] Create example data directory
- [ ] Update main README to link to examples
- [ ] CI/CD for testing examples

## Success Criteria

- [ ] All examples run without errors
- [ ] Clear learning progression (basic → advanced)
- [ ] Well-commented code
- [ ] Comprehensive README with learning objectives
- [ ] Examples tested in CI
- [ ] Notebooks render correctly on GitHub
- [ ] Example data included or downloadable

## Future Enhancements

- Interactive web demos (Streamlit/Dash)
- Video tutorials
- Binder integration for notebooks
- Example gallery website
- Community-contributed examples

---

**Created**: March 2026
**Status**: Planning Phase
**Priority**: Medium (after core documentation complete)
