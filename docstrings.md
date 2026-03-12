# Docstring Analysis for laser-init Package

Generated: 2026-03-11 (Verified and Updated)

## 1. Functions with No Docstring

**NONE** - All functions now have docstrings (some incomplete).

## 2. Functions with Incomplete Docstrings

### [src/laser/init/cli.py](src/laser/init/cli.py)
- `transform_stats_data` (line 265)
  - **Missing**: Function exists but has incomplete docstring - missing all parameters (stats_source, stats_data, iso_code, start_year, end_year, output_dir) and return value

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

### [tests/](tests/)
Test functions missing docstrings (should follow given-when-then style per CLAUDE.md):
- `test_gadm_extractor.py::test_gadm_extractor_geopackage` (line 7)
- `test_gadm_extractor.py::test_Gadm_extractor_shapefile` (line 14)
- `test_geoboundaries_extractor.py::test_geoboundaries_extractor` (line 7)

## 3. Functions with Incorrect Docstrings

### ⚠️ [src/laser/init/models/si.py](src/laser/init/models/si.py) - **CRITICAL BUG**
- `main` (line 33)
  - **Issue 1**: Code initializes `scenario["E"] = 0` at line 53 but SI model should NOT have an Exposed state
  - **Issue 2**: Code initializes `scenario["R"] = 0` at line 59 but SI model should NOT have a Recovered state
  - **Issue 3**: Uses `config["data-dir"]` with hyphen at line 36 but YAML template in abm.py uses `data_dir` with underscore - **RUNTIME BUG: KeyError**
  - **Impact**: SI model has wrong compartments AND will crash at runtime with KeyError

### ⚠️ [src/laser/init/models/sir.py](src/laser/init/models/sir.py) - **CRITICAL BUG**
- `main` (line 33)
  - **Issue 1**: Code initializes `scenario["E"] = 0` at line 53 but SIR model should NOT have an Exposed state
  - **Issue 2**: Uses `config["data-dir"]` with hyphen at line 36 but YAML template in abm.py uses `data_dir` with underscore - **RUNTIME BUG: KeyError**
  - **Impact**: SIR model has wrong compartment AND will crash at runtime with KeyError

### [src/laser/init/models/seir.py](src/laser/init/models/seir.py)
- `main` (line 33)
  - **Note**: SEIR model correctly uses `config["data_dir"]` with underscore (line 36) matching the YAML template

### [src/laser/init/extractors/gadm.py](src/laser/init/extractors/gadm.py)
- `extract` (line 25)
  - **Issue**: Docstring says `year` parameter is "used for cache organization" but the parameter is never used in the implementation

### [src/laser/init/extractors/geoboundaries.py](src/laser/init/extractors/geoboundaries.py)
- `extract` (line 21)
  - **Issue**: Docstring says `year` parameter is "used for cache organization" but the parameter is never used in the implementation

### [src/laser/init/openai_query.py](src/laser/init/openai_query.py)
- `suggest_country_fix` (line 205)
  - **Issue**: Default `model` parameter is "gpt-5.2" which doesn't exist. Should be a valid OpenAI model name like "gpt-4o" or "gpt-4"

### [src/laser/init/utils.py](src/laser/init/utils.py)
- `clip_quietly` (line 244)
  - **Issue**: Docstring says function "suppresses stdout output" but doesn't mention that suppressed output is captured in `_output` variable (line 250) which is never used

### [src/laser/init/cli.py](src/laser/init/cli.py)
- `emit_model_script` (line 280)
  - **Issue**: Comment at line 284 says "For now, just print the paths" but code actually generates model scripts and copies files

---

## Summary

- **Total functions without docstrings**: 0 ✅
- **Total functions with incomplete docstrings**: 27
- **Total functions with incorrect/misleading docstrings**: 8
- **CRITICAL runtime bugs found**: 2 (si.py and sir.py config key mismatch)

## Recommendations (Priority Order)

### 🔴 PRIORITY 1 - CRITICAL RUNTIME BUGS (Fix Immediately!)

1. **[src/laser/init/models/si.py](src/laser/init/models/si.py)**:
   - **Line 53**: Remove `scenario["E"] = 0` (SI model has no E compartment)
   - **Line 59**: Remove `scenario["R"] = 0` (SI model has no R compartment)
   - **Line 36**: Change `config["data-dir"]` to `config["data_dir"]`
   - **Lines 38-41**: Change all `datafiles["*-data"]` to `datafiles["*_data"]` (hyphen → underscore)
   - **Line 63**: Remove decrement for R: `scenario.S -= scenario.I + scenario.R` → `scenario.S -= scenario.I`

2. **[src/laser/init/models/sir.py](src/laser/init/models/sir.py)**:
   - **Line 53**: Remove `scenario["E"] = 0` (SIR model has no E compartment)
   - **Line 36**: Change `config["data-dir"]` to `config["data_dir"]`
   - **Lines 38-41**: Change all `datafiles["*-data"]` to `datafiles["*_data"]` (hyphen → underscore)

### 🟡 PRIORITY 2 - Code Quality Issues

3. **Fix invalid OpenAI model name** in [openai_query.py:211](src/laser/init/openai_query.py#L211)
   - Change default from `"gpt-5.2"` to `"gpt-4o"` or `"gpt-4"`

4. **Remove unused `year` parameter** or implement its documented purpose:
   - [extractors/gadm.py:25](src/laser/init/extractors/gadm.py#L25)
   - [extractors/geoboundaries.py:21](src/laser/init/extractors/geoboundaries.py#L21)

5. **Clean up misleading comments**:
   - [cli.py:284](src/laser/init/cli.py#L284) - Update comment to reflect actual behavior

### 🔵 PRIORITY 3 - Documentation Completeness

6. **Add complete docstring** to `transform_stats_data` in [cli.py:265](src/laser/init/cli.py#L265)
   - Add all parameters: stats_source, stats_data, iso_code, start_year, end_year, output_dir
   - Add return value documentation

7. **Add Returns: None sections** to all `__init__` methods (13 occurrences across extractors, transformers, loaders)

8. **Add Raises sections** to functions that raise exceptions:
   - Model main() functions (SI, SIR, SEIR)
   - Plotting functions in models/plot.py (8 functions)
   - download_file in utils.py

### ⚪ PRIORITY 4 - Test Documentation

9. **Add docstrings to test functions** following given-when-then style (per CLAUDE.md):
   - tests/test_gadm_extractor.py (2 functions)
   - tests/test_geoboundaries_extractor.py (1 function)

10. **Implement tests** in test_anthropic_query.py (currently nearly empty file)

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
✅ Verified test_utils.py and test_openai_query.py have excellent docstrings

## Files With Excellent Documentation

✅ **tests/test_utils.py** - All tests have given-when-then style docstrings
✅ **tests/test_openai_query.py** - All tests properly documented
✅ **src/laser/init/openai_query.py** - Comprehensive documentation throughout
✅ **src/laser/init/utils.py** - Nearly complete documentation
