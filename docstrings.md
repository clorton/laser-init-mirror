# Docstring Analysis for laser-init Package

Generated: 2026-03-11

## 1. Functions with No Docstring

### [src/laser/init/loaders/mpm.py](src/laser/init/loaders/mpm.py)
- `MpmLoader.__init__` (line 2)
- `MpmLoader.description` (line 6)
- `MpmLoader.emit_script` (line 9)

### [src/laser/init/extractors/gadm.py](src/laser/init/extractors/gadm.py)
- `GadmExtractor.__init__` (line 15)
- `GadmExtractor.description` (line 22)
- `GadmExtractor.extract` (line 25)

### [src/laser/init/extractors/geoboundaries.py](src/laser/init/extractors/geoboundaries.py)
- `GeoBoundariesExtractor.__init__` (line 14)
- `GeoBoundariesExtractor.description` (line 18)
- `GeoBoundariesExtractor.extract` (line 21)

### [src/laser/init/extractors/unocha.py](src/laser/init/extractors/unocha.py)
- `UnochaExtractor.__init__` (line 14)
- `UnochaExtractor.description` (line 18)
- `UnochaExtractor.extract` (line 21)

### [src/laser/init/extractors/unwpp.py](src/laser/init/extractors/unwpp.py)
- `UnwppExtractor.__init__` (line 35)
- `UnwppExtractor.description` (line 39)
- `UnwppExtractor.extract` (line 42)

### [src/laser/init/extractors/worldpop.py](src/laser/init/extractors/worldpop.py)
- `WorldPopExtractor.__init__` (line 32)
- `WorldPopExtractor.description` (line 36)
- `WorldPopExtractor.extract` (line 39)

### [src/laser/init/transformers/unwpp.py](src/laser/init/transformers/unwpp.py)
- `UnwppTransformer.__init__` (line 12)
- `UnwppTransformer.description` (line 16)
- `UnwppTransformer.transform` (line 19)

### [src/laser/init/transformers/geoboundaries.py](src/laser/init/transformers/geoboundaries.py)
- `GeoBoundariesTransformer.__init__` (line 13)
- `GeoBoundariesTransformer.description` (line 17)
- `GeoBoundariesTransformer.transform` (line 22)

### [src/laser/init/transformers/unocha.py](src/laser/init/transformers/unocha.py)
- `UnochaTransformer.__init__` (line 21)
- `UnochaTransformer.description` (line 25)
- `UnochaTransformer.transform` (line 28)
- `read_gbd_quietly` (line 110)

### [src/laser/init/transformers/gadm.py](src/laser/init/transformers/gadm.py)
- `GadmTransformer.__init__` (line 13)
- `GadmTransformer.description` (line 17)
- `GadmTransformer.transform` (line 20)

### [src/laser/init/utils.py](src/laser/init/utils.py)
- `update_local_provenance` (line 226)
- `clip_quietly` (line 244)
- `inform` (line 256)
- `error` (line 263)

### [src/laser/init/cli.py](src/laser/init/cli.py)
- `cli` (line 80) - *Note: function has a docstring, but @click.command help text may be intended to replace it*
- `validate_arguments` (line 125)
- `download_shape_data` (line 168)
- `download_raster_data` (line 188)
- `download_demographic_stats` (line 206)
- `emit_model_script` (line 280)
- `write_plots` (line 305)
- `plot_population_choropleth` (line 327)
- `plot_cbr_and_cdr` (line 346)
- `plot_age_distribution` (line 408)
- `plot_life_expectancy` (line 469)

### [src/laser/init/models/si.py](src/laser/init/models/si.py)
- `main` (line 33)

### [src/laser/init/models/sir.py](src/laser/init/models/sir.py)
- `main` (line 33)

### [src/laser/init/models/plot.py](src/laser/init/models/plot.py)
- `show_plots` (line 8)
- `stacked_e_and_i` (line 31)
- `r_effective_t` (line 84)
- `choropleth_snapshots` (line 110)
- `arrival_time_choropleth` (line 187)
- `individual_incidence` (line 251)
- `import_pressure` (line 299)
- `peak_timing_peak_size` (line 382)
- `cumulative_incidence` (line 450)

### [src/laser/init/models/seir.py](src/laser/init/models/seir.py)
- `main` (line 33)

### [src/laser/init/loaders/abm.py](src/laser/init/loaders/abm.py)
- `AbmLoader.__init__` (line 28)
- `AbmLoader.description` (line 32)
- `AbmLoader.emit_script` (line 35)

## 2. Functions with Incomplete Docstrings

### [src/laser/init/utils.py](src/laser/init/utils.py)
- `_normalize_string` (line 29)
  - **Missing**: Return type documentation

- `iso_from_country_string` (line 80)
  - **Missing**: Parameter descriptions, return value details, examples of usage

- `level_from_string` (line 118)
  - **Missing**: Parameter descriptions, return value details, what happens on parse failure

- `download_file` (line 146)
  - **Missing**: The `cache_dir` parameter is used but not documented in the Args section

- `update_cache_provenance` (line 203)
  - **Missing**: Return value documentation (though it returns None)

### [src/laser/init/cli.py](src/laser/init/cli.py)
- `transform_shape_and_raster_data` (line 225)
  - **Missing**: The docstring doesn't mention what the function returns in case of error or exception handling

## 3. Functions with Incorrect Docstrings

### [src/laser/init/openai_query.py](src/laser/init/openai_query.py)
- `_maybe_prefilter_candidates` (line 59)
  - **Issue**: Returns tuple description says "(iso3_subset, names_subset)" but the docstring body doesn't explain what these subsets contain or their purpose clearly enough

- `_build_response_schema` (line 126)
  - **Issue**: The function name suggests it builds a "response schema" but actually builds a JSON schema for structured outputs. The docstring is verbose but could more clearly state what the return value structure is.

### [src/laser/init/models/seir.py](src/laser/init/models/seir.py)
- `main` (line 33)
  - **Issue**: Lines 43-45 use simulation parameters (EXPOSED_DURATION_SHAPE, EXPOSED_DURATION_SCALE) that are specific to SEIR but the model comment says they're for SI model at line 44 comment in sir.py (copy-paste error if these files were templated)

### [src/laser/init/transformers/unocha.py](src/laser/init/transformers/unocha.py)
- `UnochaTransformer.transform` (line 28)
  - **Issue**: Line 75 assigns to `gdf["nodeid"]` but line 74 uses `country_gdf` for filtering. This appears to be a bug - should probably assign `country_gdf["nodeid"]` instead of `gdf["nodeid"]`

### [src/laser/init/utils.py](src/laser/init/utils.py)
- `download_file` (line 146)
  - **Issue**: The docstring says "returns Path to the downloaded file" but doesn't mention that it also updates provenance as a side effect

### [src/laser/init/cli.py](src/laser/init/cli.py)
- `transform_shape_and_raster_data` (line 225)
  - **Issue**: The docstring mentions "KeyError: If the specified shape_source is not found" in Raises section, but the function doesn't have a try-except block for KeyError - it would propagate uncaught

---

## Summary

- **Total functions without docstrings**: 58
- **Total functions with incomplete docstrings**: 7
- **Total functions with incorrect/misleading docstrings**: 6

## Recommendations

1. **Priority 1**: Add docstrings to all extractor, transformer, and loader class methods, as these form the core public API
2. **Priority 2**: Add docstrings to CLI functions, especially those that perform complex validation or transformation logic
3. **Priority 3**: Complete parameter and return value documentation for utility functions
4. **Priority 4**: Fix the identified bugs in transformers/unocha.py (line 75) and clarify side effects in documentation
5. **Priority 5**: Add examples to key public functions like `iso_from_country_string` and `level_from_string`
