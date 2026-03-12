# Docstring Analysis for laser-init Package

Generated: 2026-03-11 (Updated after documentation improvements)

## 1. Functions with No Docstring

### [src/laser/init/cli.py](src/laser/init/cli.py)
- `transform_stats_data` (line 265)
  - **Missing**: Complete docstring - no description, parameters, or return value documented

## 2. Functions with Incomplete Docstrings

### [src/laser/init/extractors/gadm.py](src/laser/init/extractors/gadm.py)
- `GadmExtractor.__init__` (line 15)
  - **Missing**: Returns section (should document returns None)

### [src/laser/init/extractors/geoboundaries.py](src/laser/init/extractors/geoboundaries.py)
- `GeoBoundariesExtractor.__init__` (line 14)
  - **Missing**: Returns section

### [src/laser/init/extractors/unocha.py](src/laser/init/extractors/unocha.py)
- `UnochaExtractor.__init__` (line 14)
  - **Missing**: Returns section

### [src/laser/init/extractors/unwpp.py](src/laser/init/extractors/unwpp.py)
- `UnwppExtractor.__init__` (line 35)
  - **Missing**: Returns section

### [src/laser/init/extractors/worldpop.py](src/laser/init/extractors/worldpop.py)
- `WorldPopExtractor.__init__` (line 32)
  - **Missing**: Returns section

### [src/laser/init/transformers/gadm.py](src/laser/init/transformers/gadm.py)
- `GadmTransformer.__init__` (line 13)
  - **Missing**: Returns section

### [src/laser/init/transformers/geoboundaries.py](src/laser/init/transformers/geoboundaries.py)
- `GeoBoundariesTransformer.__init__` (line 13)
  - **Missing**: Returns section

### [src/laser/init/transformers/unocha.py](src/laser/init/transformers/unocha.py)
- `UnochaTransformer.__init__` (line 21)
  - **Missing**: Returns section

### [src/laser/init/transformers/unwpp.py](src/laser/init/transformers/unwpp.py)
- `UnwppTransformer.__init__` (line 12)
  - **Missing**: Returns section

### [src/laser/init/loaders/mpm.py](src/laser/init/loaders/mpm.py)
- `MpmLoader.__init__` (line 2)
  - **Missing**: Returns section
- `MpmLoader.emit_script` (line 15)
  - **Missing**: All parameters (mode, model, shape_filename, cxr_filename, pop_filename, exp_filename, output_dir)

### [src/laser/init/loaders/abm.py](src/laser/init/loaders/abm.py)
- `AbmLoader.__init__` (line 28)
  - **Missing**: Returns section

### [src/laser/init/utils.py](src/laser/init/utils.py)
- `download_file` (line 146)
  - **Missing**: Raises section (function raises exceptions on download failure)

### [src/laser/init/models/si.py](src/laser/init/models/si.py)
- `main` (line 33)
  - **Missing**: Raises section (Click exceptions for invalid paths)

### [src/laser/init/models/sir.py](src/laser/init/models/sir.py)
- `main` (line 33)
  - **Missing**: Raises section

### [src/laser/init/models/seir.py](src/laser/init/models/seir.py)
- `main` (line 33)
  - **Missing**: Raises section

### [src/laser/init/models/plot.py](src/laser/init/models/plot.py)
All plotting functions missing Raises sections:
- `stacked_e_and_i` (line 31)
- `r_effective_t` (line 84)
- `choropleth_snapshots` (line 110)
- `arrival_time_choropleth` (line 187)
- `individual_incidence` (line 251)
- `import_pressure` (line 299)
- `peak_timing_peak_size` (line 382)
- `cumulative_incidence` (line 450)

### [src/laser/init/cli.py](src/laser/init/cli.py)
Plotting functions missing Raises sections:
- `plot_population_choropleth` (line 327)
- `plot_cbr_and_cdr` (line 346)
- `plot_age_distribution` (line 408)
- `plot_life_expectancy` (line 469)

## 3. Functions with Incorrect Docstrings

### [src/laser/init/models/si.py](src/laser/init/models/si.py)
- `main` (line 33)
  - **Issue**: Model architecture mismatch - code shows SI model but implementation suggests proper SI with S->I transitions

### [src/laser/init/models/sir.py](src/laser/init/models/sir.py)
- `main` (line 33)
  - **Issue**: Code initializes `scenario["E"] = 0` at line 53 but SIR model shouldn't have an Exposed state. This suggests either:
    - The model should be SEIR instead of SIR, OR
    - Line 53 is copy-paste error from SEIR template

### [src/laser/init/models/seir.py](src/laser/init/models/seir.py)
- `main` (line 33)
  - **Issue**: Parameter naming inconsistency - uses `config["data_dir"]` (underscore) at line 36, but si.py and sir.py use `config["data-dir"]` (hyphen). The YAML template in abm.py uses hyphens, so seir.py is incorrect.

### [src/laser/init/extractors/gadm.py](src/laser/init/extractors/gadm.py)
- `extract` (line 25)
  - **Issue**: Docstring says `year` parameter is "used for cache organization" but the parameter is never used in the implementation

### [src/laser/init/extractors/geoboundaries.py](src/laser/init/extractors/geoboundaries.py)
- `extract` (line 21)
  - **Issue**: Docstring says `year` parameter is "used for cache organization" but the parameter is never used in the implementation

### [src/laser/init/openai_query.py](src/laser/init/openai_query.py)
- `suggest_country_fix` (line 205)
  - **Issue**: Default `model` parameter is "gpt-5.2" which doesn't exist. Should be a valid OpenAI model name like "gpt-4" or "gpt-3.5-turbo"

### [src/laser/init/utils.py](src/laser/init/utils.py)
- `clip_quietly` (line 244)
  - **Issue**: Docstring says function "suppresses stdout output" but doesn't mention that suppressed output is captured in `_output` variable (line 250) which is never used

### [src/laser/init/cli.py](src/laser/init/cli.py)
- `cli` (line 80)
  - **Issue**: Docstring at line 92 duplicates the @click.command help text without adding value
- `emit_model_script` (line 280)
  - **Issue**: Comment at line 284 says "For now, just print the paths" but code actually generates model scripts and copies files

---

## Summary

- **Total functions without docstrings**: 1
- **Total functions with incomplete docstrings**: 30+
- **Total functions with incorrect/misleading docstrings**: 8

## Recommendations (Priority Order)

1. **Priority 1 - Critical Issues**:
   - Fix model inconsistency in [sir.py:53](src/laser/init/models/sir.py#L53) - remove `scenario["E"] = 0` line
   - Fix parameter naming in [seir.py:36](src/laser/init/models/seir.py#L36) - change `config["data_dir"]` to `config["data-dir"]`
   - Fix invalid OpenAI model name in [openai_query.py:211](src/laser/init/openai_query.py#L211)

2. **Priority 2 - Missing Core Documentation**:
   - Add complete docstring to `transform_stats_data` in [cli.py:265](src/laser/init/cli.py#L265)
   - Add missing parameters to `MpmLoader.emit_script` in [loaders/mpm.py:15](src/laser/init/loaders/mpm.py#L15)

3. **Priority 3 - Consistency Improvements**:
   - Add Returns sections to all `__init__` methods (13 occurrences)
   - Add Raises sections to functions that raise exceptions (20+ occurrences)

4. **Priority 4 - Documentation Accuracy**:
   - Remove or implement unused `year` parameter in GADM and GeoBoundaries extractors
   - Update `clip_quietly` docstring to mention captured output handling
   - Clean up misleading comments in `emit_model_script`

## Recent Improvements (Completed)

✅ Added comprehensive docstrings to all extractor classes (GADM, GeoBoundaries, UNOCHA, UNWPP, WorldPop)
✅ Added comprehensive docstrings to all transformer classes (GADM, GeoBoundaries, UNOCHA, UNWPP)
✅ Added comprehensive docstrings to all loader classes (ABM, MPM)
✅ Added docstrings to all CLI helper and plotting functions
✅ Added docstrings to all model script main functions (SI, SIR, SEIR)
✅ Added docstrings to all plotting functions in models/plot.py
✅ Completed parameter and return value documentation in utils.py
✅ Fixed bug in transformers/unocha.py line 75 (gdf vs country_gdf)
✅ Improved docstring clarity in openai_query.py functions
