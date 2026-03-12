# Architecture Documentation

Developer documentation for the laser-init codebase.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Component Architecture](#component-architecture)
4. [Data Flow](#data-flow)
5. [Extension Points](#extension-points)
6. [Code Conventions](#code-conventions)

## Overview

laser-init follows an Extract-Transform-Load (ETL) pipeline architecture:

```
Extract → Transform → Load
   ↓          ↓         ↓
  Raw     Processed   Model
  Data      Data      Scripts
```

**Design Principles**:
- **Modularity**: Extractors, transformers, and loaders are independent
- **Extensibility**: Easy to add new data sources
- Human-readable output
- **Convention over configuration**: Sensible defaults, minimal required config

## Project Structure

```
laser-init/
├── src/laser/init/
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface entry point
│   ├── config.py             # Configuration loading
│   ├── logger.py             # Logging setup
│   ├── utils.py              # Shared utilities
│   ├── french_iso.py         # French country name mappings
│   ├── openai_query.py       # OpenAI country name resolution
│   ├── anthropic_query.py    # Anthropic country name resolution
│   ├── extractors/           # Data extraction modules
│   │   ├── gadm.py          # GADM shapefile extractor
│   │   ├── geoboundaries.py # geoBoundaries extractor
│   │   ├── unocha.py        # UNOCHA extractor
│   │   ├── worldpop.py      # WorldPop raster extractor
│   │   └── unwpp.py         # UN WPP demographics extractor
│   ├── transformers/         # Data transformation modules
│   │   ├── gadm.py          # GADM transformer
│   │   ├── geoboundaries.py # geoBoundaries transformer
│   │   ├── unocha.py        # UNOCHA transformer
│   │   └── unwpp.py         # UN WPP transformer
│   ├── loaders/              # Model script generation
│   │   ├── abm.py           # Agent-based model loader
│   │   └── mpm.py           # Metapopulation model loader
│   └── models/               # Model templates
│       ├── si.py            # SI model template
│       ├── sir.py           # SIR model template
│       ├── seir.py          # SEIR model template
│       └── plot.py          # Plotting utilities template
├── tests/                    # Test suite
├── docs/                     # Documentation
├── pyproject.toml           # Project configuration
└── README.md                # User-facing documentation
```

## Component Architecture

### Extractors

**Purpose**: Download raw data from external sources

**Interface**:
```python
class DataExtractor:
    def __init__(self, cache_dir: Path):
        """Initialize extractor with cache directory."""
        pass

    def description(self) -> str:
        """Return human-readable description."""
        pass

    def extract(self, iso_code: str, level: int, year: int) -> Path:
        """Download and cache data, return path to downloaded file."""
        pass
```

**Responsibilities**:
- Download from URL or API
- Cache locally (usually in `~/.laser/cache/`)
- Update provenance metadata
- Return path to downloaded file

**Current Extractors**:
- `GadmExtractor`: Downloads GADM GeoPackage files
- `GeoBoundariesExtractor`: Downloads geoBoundaries shapefiles
- `UnochaExtractor`: Downloads UNOCHA global geodatabase
- `WorldPopExtractor`: Downloads WorldPop population rasters
- `UnwppExtractor`: Downloads UN WPP demographic CSV files

### Transformers

**Purpose**: Process raw data into model-ready format

**Interface**:
```python
class DataTransformer:
    def __init__(self, cache_dir: Path):
        """Initialize transformer with cache directory."""
        pass

    def description(self) -> str:
        """Return human-readable description."""
        pass

    def transform(self, iso_code: str, level: int, year: int, output_dir: Path) -> Tuple[Path]:
        """Transform data and write to output_dir, return paths to generated files."""
        pass
```

**Responsibilities**:
- Load extracted data
- Filter/subset for specified country and level
- Aggregate population (for shapefile transformers)
- Extract demographics (for stats transformers)
- Write output files (GeoPackage, CSV)
- Return file path(s) of transformed data

**Current Transformers**:
- `GadmTransformer`: Processes GADM data + aggregates WorldPop
- `GeoBoundariesTransformer`: Processes geoBoundaries + aggregates WorldPop
- `UnochaTransformer`: Processes UNOCHA + aggregates WorldPop
- `UnwppTransformer`: Extracts demographics from UN WPP

### Loaders

**Purpose**: Generate model scripts and configuration files

**Interface**:
```python
class ModelLoader:
    def __init__(self, model_type: str):
        """Initialize loader for specific model type (SI, SIR, SEIR)."""
        pass

    def description(self) -> str:
        """Return human-readable description."""
        pass

    def emit_script(self, output_dir: Path, config: Dict) -> None:
        """Generate model script and config.yaml in output_dir."""
        pass
```

**Responsibilities**:
- Copy model template to output directory
- Generate `config.yaml` with paths and parameters
- Copy `plot.py` utilities

**Current Loaders**:
- `AbmLoader`: Generates agent-based model scripts (SI/SIR/SEIR)
- `MpmLoader`: Generates metapopulation model scripts (future feature)

### CLI

**File**: `cli.py`

**Responsibilities**:
- Parse command-line arguments
- Validate inputs (country codes, levels, years)
- Orchestrate pipeline: Extract → Transform → Load
- Generate validation plots
- Create PDF report

**Key Functions**:
- `cli()`: Main entry point (Click command)
- `validate_arguments()`: Input validation
- `download_shape_data()`: Coordinate shapefile extraction
- `download_raster_data()`: Coordinate raster extraction
- `download_demographic_stats()`: Coordinate demographics extraction
- `transform_shape_and_raster_data()`: Coordinate transformation
- `emit_model_script()`: Coordinate model generation
- `write_plots()`: Generate validation visualizations

### Utilities

**File**: `utils.py`

**Key Functions**:
- `iso_from_country_string()`: Convert country name to ISO-3 code (exact, fuzzy, or LLM-based)
- `level_from_string()`: Parse administrative level
- `download_file()`: HTTP download with caching and provenance
- `update_cache_provenance()`: Track cached file metadata
- `update_local_provenance()`: Track output file lineage

## Data Flow

### High-Level Flow

```
    ┌─────────────┐
    │ CLI Input   │
    │ (country,   │
    │  level,     │
    │  years)     │
    └──────┬──────┘
           │
           v
┌──────────────────────┐
│ Validate & Normalize │
│ - ISO code           │
│ - Level number       │
│ - Year range         │
└──────────┬───────────┘
           │
           v
  ┌─────────────────┐
  │ Extract Phase   │
  │ - Shapefiles    │
  │ - Rasters       │
  │ - Demographics  │
  └───────┬─────────┘
          │
          v
  ┌─────────────────┐
  │ Transform Phase │
  │ - Filter country│
  │ - Aggregate pop │
  │ - Extract stats │
  └───────┬─────────┘
          │
          v
  ┌─────────────────┐
  │ Load Phase      │
  │ - Model script  │
  │ - Config file   │
  │ - Plot utils    │
  └───────┬─────────┘
          │
          v
  ┌─────────────────┐
  │ Validation      │
  │ - Generate plots│
  │ - Create report │
  └─────────────────┘
```

### Detailed Pipeline

1. **Input Validation** (`cli.py:validate_arguments`)
   - Convert country string to ISO-3 code
   - Parse level to integer
   - Validate year range
   - Determine output directory

2. **Shape Data Extraction** (`cli.py:download_shape_data`)
   - Select extractor based on `--shape-source`
   - Call `extractor.extract(iso_code, level, year)`
   - Returns path to cached shapefile

3. **Raster Data Extraction** (`cli.py:download_raster_data`)
   - Select extractor based on `--raster-source`
   - Call `extractor.extract(iso_code, level, year)`
   - Returns path to cached raster

4. **Demographics Extraction** (`cli.py:download_demographic_stats`)
   - Select extractor based on `--stats-source`
   - Call `extractor.extract(iso_code, start_year, end_year)`
   - Returns paths to cached CSV files

5. **Transformation** (`cli.py:transform_shape_and_raster_data`)
   - Load shapefile and raster
   - Filter to specified country and level
   - Aggregate population using RasterToolkit
   - Transform demographics
   - Write GeoPackage and CSV files to output directory

6. **Model Generation** (`cli.py:emit_model_script`)
   - Select loader based on `--mode` and `--model`
   - Generate model script (si.py, sir.py, or seir.py)
   - Generate config.yaml
   - Copy plot.py

7. **Validation** (`cli.py:write_plots`)
   - Generate choropleth map
   - Plot age distribution
   - Plot birth/death rates
   - Plot life expectancy
   - Combine into PDF report

## Extension Points

### Adding a New Shapefile Source

1. Create `src/laser/init/extractors/newsource.py`:
```python
class NewSourceExtractor:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def description(self):
        return "New Source shapefile extractor"

    def extract(self, iso_code, level, year):
        # Download logic
        url = f"https://newsource.org/data/{iso_code}_adm{level}.shp"
        return download_file(url, self.cache_dir / "newsource")
```

2. Create `src/laser/init/transformers/newsource.py`:
```python
class NewSourceTransformer:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def description(self):
        return "New Source shapefile transformer"

    def transform(self, iso_code, level, year, output_dir):
        # Load, filter, aggregate population
        # Return tuple of output files
        pass
```

3. Register in `cli.py`:
```python
from laser.init.extractors import newsource as newsourceex
from laser.init.transformers import newsource as newsourcetx

        shape_extractor = {
            "unocha": unochaex.UnochaExtractor,
            "geoboundaries": geoboundariesex.GeoBoundariesExtractor,
            "gadm": gadmex.GadmExtractor,
            "newsource": newsourceex.NewSourceExtractor, # Add this
        }[shape_source]()

    shape_transformer = {
        "unocha": unochatx.UnochaTransformer,
        "geoboundaries": geoboundariestx.GeoBoundariesTransformer,
        "gadm": gadmtx.GadmTransformer,
        "newsource", newsourceex.NewSourceTransformer, # Add this
    }[shape_source]()

```

4. Update CLI option:
```python
@click.option(
    "--shape-source",
    type=click.Choice(["unocha", "geoboundaries", "gadm", "newsource"], case_insensitive=False),
    ...
)
```

### Adding a New Model Type

1. Create `src/laser/init/models/newmodel.py` based on existing templates

2. Update CLI option:
```python
@click.option(
    "--model",
    type=click.Choice(["SI", "SIR", "SEIR", "NEWMODEL"], case_insensitive=False),
    ...
)
```

## Code Conventions

Following the guidelines in [CLAUDE.md](https://github.com/laser-base/laser-init/blob/main/CLAUDE.md):

### General
- Always update CHANGELOG.md for accepted changes
- Use double quotes for strings
- Use `pathlib.Path` instead of `os.path`
- Import `inform` and `error` `utils` and use `inform()` for internal actions

### Documentation
- Google-style docstrings formatted for Markdown
- Include exceptions explicitly raised
- Add executable code examples when appropriate

### Testing
- Given-when-then style tests
- Add docstrings explaining test purpose and failure implications
- Comment on inconsistencies or ambiguities
- Run _and pass all tests_ before considering implementation complete

### Style
- Follow PEP 8 (enforced by ruff)
- Line length: 100 characters
- Target: Python 3.10+

## Development Workflow

1. **Setup**:
```shell
git clone https://github.com/laser-base/laser-init.git
cd laser-init
uv sync  # or pip install -e .
```

2. **Make Changes**:
   - Edit code
   - Add tests
   - Update documentation

3. **Test**:
```shell
pytest
pytest --cov=laser.init --cov-report=term-missing
```

4. **Format & Lint**:
```shell
ruff check .
ruff format .
```

5. **Update CHANGELOG.md**

6. **Commit & Push**

See [Contributing Guide](contributing.md) for detailed workflow.

## Architecture Decisions

### Why Extract-Transform-Load?

- **Separation of concerns**: Each phase has clear responsibility
- **Reusability**: Extractors can be reused for different transformations
- **Caching**: Expensive downloads happen once
- **Testability**: Each component can be tested independently

### Why Not Use Existing GIS Tools?

laser-init **does** use existing tools (GeoPandas, RasterToolkit), but provides:
- Disease modeling focus (not general GIS)
- Opinionated workflow for epidemiologists
- Integrated demographics (not just spatial data)
- Ready-to-run LASER models

### Why Click Instead of Argparse?

- More readable command definitions
- Automatic help generation
- Better type handling
- Extensible with decorators

### Why Not Database?

- Simple file-based workflow
- Easy to version control outputs
- No infrastructure requirements
- Transparent data provenance

## Performance Considerations

### Caching Strategy

- Downloads cached in `~/.laser/cache/`
- Cache hits avoid expensive network I/O
- First run slow (downloads), subsequent runs fast

### Memory Usage

- GeoDataFrames held in memory during transformation
- Large countries (USA, Brazil) can use >2GB RAM
- Consider processing lower admin levels for memory-constrained systems

## Future Architecture

Potential improvements:

- **Plugin system**: Dynamic extractor/transformer registration
- **Async downloads**: Parallel data fetching
- **Streaming processing**: Handle larger-than-memory datasets
- **Web API**: REST API for programmatic access
- **Docker images**: Containerized distribution

## Additional Resources

- [Contributing Guide](contributing.md)
- [User Guide](userguide.md)
- [laser.generic](https://github.com/laser-base/laser-generic)
- [RasterToolkit](https://github.com/InstituteforDiseaseModeling/RasterToolkit)

---

**Last Updated**: March 2026
