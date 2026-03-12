# Configuration Guide

This guide covers all configuration options for laser-init, including global settings, run-time options, and model parameters.

## Table of Contents

1. [Global Configuration](#global-configuration)
2. [Run Configuration (config.yaml)](#run-configuration)
3. [Model Parameters Reference](#model-parameters-reference)
4. [Data Source Selection](#data-source-selection)
5. [API Keys for Country Name Resolution](#api-keys-for-country-name-resolution)

## Global Configuration

laser-init looks for a global configuration file in the following locations (in order):

1. `./laser_config.yaml` (current working directory)
2. `./laser_config.json` (current working directory)
3. `~/.laser/laser_config.yaml` (user home directory)
4. `~/.laser/laser_config.json` (user home directory)

The first file found is used. Command-line options override config file settings.

### Creating a Global Configuration File

Create `~/.laser/laser_config.yaml`:

```yaml
# Default data source preferences
shape_source: unocha      # Options: unocha, geoboundaries, gadm
raster_source: worldpop   # Options: worldpop (only option currently)
stats_source: unwpp       # Options: unwpp (only option currently)

# Optional: API keys for LLM-enhanced country name matching
openai_api_key: sk-your-key-here
anthropic_api_key: sk-ant-your-key-here
```

Or in JSON format (`~/.laser/laser_config.json`):

```json
{
  "shape_source": "unocha",
  "raster_source": "worldpop",
  "stats_source": "unwpp",
  "openai_api_key": "sk-your-key-here",
  "anthropic_api_key": "sk-ant-your-key-here"
}
```

### Global Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `shape_source` | string | `"unocha"` | Default shapefile data source (unocha, geoboundaries, gadm) |
| `raster_source` | string | `"worldpop"` | Default population raster source (worldpop only) |
| `stats_source` | string | `"unwpp"` | Default demographic statistics source (unwpp only) |
| `openai_api_key` | string | None | OpenAI API key for enhanced country name matching |
| `anthropic_api_key` | string | None | Anthropic API key for enhanced country name matching |

### Environment Variables

As an alternative to config files, you can set API keys via environment variables:

```shell
export OPENAI_API_KEY="sk-your-key-here"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

laser-init will use these environment variables if no config file is found.

## Run Configuration

Each time you run laser-init, it generates a `config.yaml` file in the output directory. This file contains:

1. References to the generated data files
2. Model parameters for the simulation

### Example config.yaml

```yaml
data-dir: /Users/user/projects/NGA/2000

datafiles:
    shape-data: NGA_admin2.gpkg
    cxr-data: cxr.csv
    pop-data: age_dist.csv
    exp-data: life_exp.csv

simulation:
    nyears: 10
    r0: 2.5
    exposed-duration-shape: 4.5
    exposed-duration-scale: 1.0
    infectious-duration-mean: 7.0
    naive-population: true
```

### Running with Custom Config

The generated model scripts accept a `--config` option:

```shell
# Use default config.yaml in same directory
python seir.py

# Use custom config file
python seir.py --config /path/to/custom_config.yaml

# Override data directory
python seir.py --data-dir /path/to/data
```

## Model Parameters Reference

### Data Files Section

```yaml
datafiles:
    shape-data: NGA_admin2.gpkg      # GeoPackage with boundaries and population
    cxr-data: cxr.csv                # Crude birth/death rates time series
    pop-data: age_dist.csv           # Population age distribution
    exp-data: life_exp.csv           # Life expectancy/survival curve
```

These file paths are relative to `data-dir`.

### Simulation Parameters

#### Common Parameters (All Models)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `nyears` | integer | 10 | Simulation duration in years |
| `r0` | float | 2.5 | Basic reproduction number (average secondary infections) |
| `infectious-duration-mean` | float | 7.0 | Mean infectious period in days |
| `naive-population` | boolean | true | If false, initialize with immune individuals based on R0 |

#### SEIR-Specific Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exposed-duration-shape` | float | 4.5 | Shape parameter for gamma distribution of exposed period |
| `exposed-duration-scale` | float | 1.0 | Scale parameter for gamma distribution of exposed period |

The exposed period follows a gamma distribution with mean = shape × scale (4.5 days by default).

#### Derived Parameters

The model automatically calculates:

- `nticks = nyears × 365` (simulation steps in days)
- `beta = r0 / infectious-duration-mean` (transmission rate)

### Understanding R0 and Beta

- **R0 (Basic Reproduction Number)**: Average number of secondary infections caused by one infectious individual in a fully susceptible population
  - R0 < 1: Outbreak dies out
  - R0 = 1: Endemic equilibrium
  - R0 > 1: Epidemic growth

- **Beta (Transmission Rate)**: Per-contact probability of infection
  - Automatically calculated: `beta = r0 / infectious_duration_mean`
  - Example: R0=2.5, duration=7 days → beta ≈ 0.357

### Naive Population Setting

```yaml
naive-population: true   # All population starts susceptible (except initial seeds)
naive-population: false  # Initialize (1-1/R0)×S individuals in R compartment
```

When `naive-population: false`:
- Simulates prior immunity or vaccination
- For R0=2.5: 60% of population starts susceptible, 40% recovered
- Useful for modeling endemic diseases or post-vaccination scenarios

## Data Source Selection

### Command-Line Override

Override config file defaults with command-line flags:

```shell
laser-init NGA 2 2000 2025 --shape-source gadm --raster-source worldpop
```

### Shape Sources Comparison

| Source | Coverage | Quality | File Size | Update Frequency | Best For |
|--------|----------|---------|-----------|------------------|----------|
| **UNOCHA** | Good (humanitarian focus) | High | Large (1-2GB global) | Regular | Crisis regions, humanitarian work |
| **geoBoundaries** | Excellent (global) | High | Medium (per-country) | Annual | Academic research |
| **GADM** | Excellent (global) | High | Medium (per-country) | Frequent | General purpose, comprehensive data |

### Raster Sources

| Source | Coverage | Resolution | Time Period | Best For |
|--------|----------|------------|-------------|----------|
| **WorldPop** | Global | ~100m | 2000-2020 | Population distribution modeling |

### Statistics Sources

| Source | Coverage | Indicators | Time Period | Best For |
|--------|----------|------------|-------------|----------|
| **UN WPP** | Global (countries) | Comprehensive | 1950-2100 | Demographic modeling, forecasting |

See [datasources.md](datasources.md) for detailed comparison.

## API Keys for Country Name Resolution

laser-init includes three levels of country name matching:

1. **Exact match**: ISO-3 codes and official names (always enabled)
2. **Fuzzy match**: Common misspellings and variants (always enabled)
3. **LLM-enhanced match**: AI-powered resolution (requires API key)

### Why Use LLM-Enhanced Matching?

LLM matching helps with:
- Unusual spellings and transliterations
- Historical country names
- Common informal names
- Mixed language queries

### Configuring OpenAI

```yaml
openai_api_key: sk-your-key-here
```

Or environment variable:
```shell
export OPENAI_API_KEY="sk-your-key-here"
```

**Cost**: ~$0.01-0.02 per query (GPT-4 Turbo)

### Configuring Anthropic

```yaml
anthropic_api_key: sk-ant-your-key-here
```

Or environment variable:
```shell
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Cost**: Similar to OpenAI

### LLM Behavior

- **Precedence**: If both keys are provided, OpenAI is tried first, then Anthropic
- **Fallback**: If no API key works, laser-init falls back to exact/fuzzy matching
- **Privacy**: Country query is sent to the API; no other data is transmitted
- **Performance**: Adds ~1-3 seconds to the initial country lookup

### When LLM Matching is NOT Used

LLM matching is skipped if:
1. Exact match found (ISO-3 code or official name)
2. Fuzzy match has high confidence (>90% similarity)
3. No API keys configured

### Testing Country Name Resolution

You can test country name matching without running a full laser-init command:

```python
from laser.init.utils import iso_from_country_string

# Test exact match
print(iso_from_country_string("PAK"))  # Output: PAK

# Test fuzzy match
print(iso_from_country_string("Pakstan"))  # Output: PAK (fuzzy match)

# Test LLM match (requires API key configured)
print(iso_from_country_string("Land of the Rising Sun"))  # Output: JPN (with LLM)
```

## Cache Management

laser-init caches downloaded data to speed up subsequent runs:

### Cache Location

- **Default**: `~/.cache/laser-init/`
- **Contents**:
  - Downloaded shapefiles
  - Population rasters
  - Demographic datasets
  - Provenance metadata

### Cache Size

- UNOCHA global geodatabase: ~1-2 GB
- Per-country rasters: ~10-100 MB each
- UN WPP data: ~50-200 MB total

### Clearing Cache

```shell
# Clear all cached data
rm -rf ~/.cache/laser-init/

# Clear specific source
rm -rf ~/.cache/laser-init/unocha/
rm -rf ~/.cache/laser-init/worldpop/
rm -rf ~/.cache/laser-init/unwpp/
```

### Viewing Cache Contents

```shell
ls -lh ~/.cache/laser-init/
```

## Output Directory Structure

Understanding the output structure helps with custom workflows:

```
NGA/
└── 2000/
    ├── NGA_admin2.gpkg          # Geospatial data
    ├── config.yaml              # Run configuration
    ├── seir.py                  # Model script
    ├── plot.py                  # Plotting script
    ├── age_dist.csv             # Demographics
    ├── cxr.csv                  # Birth/death rates
    ├── life_exp.csv             # Life expectancy
    ├── provenance.json          # Data source metadata
    ├── *.png                    # Validation plots
    └── report.pdf               # Combined PDF report
```

### Customizing Output Directory

```shell
# Default: ./ISOCODE/start_year
laser-init NGA 2 2000 2025

# Custom location
laser-init NGA 2 2000 2025 --output-dir /data/models/nigeria_2000

# Organized by project
laser-init NGA 2 2000 2025 --output-dir ./projects/ebola/nga_baseline
```

## Advanced Configuration

### Multiple Model Configurations

Generate multiple configurations for comparison:

```shell
# Baseline scenario
laser-init NGA 2 2000 2025 --output-dir ./scenarios/baseline

# High transmission
laser-init NGA 2 2000 2025 --output-dir ./scenarios/high_r0
# Then edit ./scenarios/high_r0/config.yaml to set r0: 4.0

# With prior immunity
laser-init NGA 2 2000 2025 --output-dir ./scenarios/immunity
# Then edit ./scenarios/immunity/config.yaml to set naive-population: false
```

### Scripted Configuration Generation

```python
import yaml
from pathlib import Path

# Load base configuration
config = yaml.safe_load(Path("config.yaml").read_text())

# Create scenarios
scenarios = {
    "baseline": {"r0": 2.5},
    "high_transmission": {"r0": 4.0},
    "low_transmission": {"r0": 1.5},
}

for name, params in scenarios.items():
    config["simulation"].update(params)
    Path(f"config_{name}.yaml").write_text(yaml.dump(config))
```

## Troubleshooting Configuration Issues

### Config File Not Found

**Error**: laser-init ignores config file

**Causes**:
- Wrong file location
- Syntax errors in YAML/JSON
- Wrong file extension

**Solution**:
```shell
# Check syntax
python -c "import yaml; yaml.safe_load(open('laser_config.yaml'))"

# Verify location
ls -la ~/.laser/laser_config.yaml
ls -la ./laser_config.yaml
```

### Invalid Configuration Values

**Error**: Validation errors when loading config

**Solutions**:
- Check spelling of data source names (case-insensitive but must match)
- Ensure API keys are valid strings
- Verify YAML/JSON syntax

### Model Script Can't Find Data Files

**Error**: FileNotFoundError when running model

**Causes**:
- Relative paths in config.yaml
- Moved data files
- Wrong data-dir setting

**Solutions**:
```shell
# Use absolute paths in config.yaml
data-dir: /full/path/to/NGA/2000

# Or run from the data directory
cd NGA/2000
python seir.py

# Or override data directory
python seir.py --data-dir /full/path/to/NGA/2000
```

## Next Steps

- [User Guide](userguide.md) - Comprehensive workflows and tutorials
- [Data Sources](datasources.md) - Detailed data source documentation
- [Models](models.md) - Epidemiological model details
- [Architecture](architecture.md) - Developer documentation
