# Data Sources Documentation

This guide provides detailed information about the data sources supported by laser-init, including their characteristics, coverage, quality, and appropriate use cases.

## Table of Contents

1. [Overview](#overview)
2. [Administrative Boundary Sources](#administrative-boundary-sources)
3. [Population Raster Sources](#population-raster-sources)
4. [Demographic Statistics Sources](#demographic-statistics-sources)
5. [Data Source Comparison](#data-source-comparison)
6. [Selecting the Right Source](#selecting-the-right-source)
7. [Data Quality Considerations](#data-quality-considerations)

## Overview

laser-init integrates data from multiple authoritative sources to build comprehensive spatial disease models. The tool supports:

- **3 shapefile sources** for administrative boundaries
- **1 population raster source** (with potential for expansion)
- **1 demographic statistics source** (with potential for expansion)

All sources are freely available and regularly updated by their respective organizations.

## Administrative Boundary Sources

Administrative boundaries define the spatial units (e.g., districts, provinces) used in spatial models.

### UNOCHA COD-AB (Common Operational Datasets - Administrative Boundaries)

**Provider**: United Nations Office for the Coordination of Humanitarian Affairs (OCHA)

**URL**: https://knowledge.base.unocha.org/wiki/spaces/imtoolbox/pages/2557378679/Administrative+Boundaries+COD-AB

#### Characteristics

| Feature | Details |
|---------|---------|
| **Coverage** | 200+ countries, focused on humanitarian operations |
| **Administrative Levels** | Typically 0-3, varies by country |
| **Update Frequency** | Regular updates, especially for crisis regions |
| **Format** | GeoDatabase (.gdb) - single global file |
| **File Size** | ~1-2 GB (global database, cached locally) |
| **Coordinate System** | WGS84 (EPSG:4326) |
| **License** | Public domain / Open data |

#### Strengths

- **High quality**: Vetted by UN humanitarian operations
- **Authoritative**: Often the official government boundaries
- **Crisis coverage**: Excellent coverage for conflict/disaster-affected regions
- **Standardized**: Consistent attribute naming across countries
- **Well-maintained**: Regular updates, especially during humanitarian responses

#### Limitations

- **Large download**: Initial download is 1-2 GB (but cached for reuse)
- **Limited levels**: Some countries only have level 0-2
- **Humanitarian focus**: Better coverage for crisis regions than stable countries

#### Recommended For

- Humanitarian response modeling
- Crisis-affected regions (Syria, Yemen, South Sudan, etc.)
- Studies requiring UN-vetted boundaries
- Multi-country analyses (single consistent source)

#### Usage in laser-init

```shell
# Default source (no flag needed)
laser-init SSD 2 2015 2020

# Explicit specification
laser-init SSD 2 2015 2020 --shape-source unocha
```

#### Data Attribution

**Citation**: UNOCHA, Field Information Services Section (FISS), Common Operational Datasets (CODs), Administrative Boundaries. Available from: https://data.humdata.org/

---

### geoBoundaries

**Provider**: William & Mary geoLab

**URL**: https://www.geoboundaries.org/

#### Characteristics

| Feature | Details |
|---------|---------|
| **Coverage** | 200+ countries, comprehensive global coverage |
| **Administrative Levels** | 0-5, varies by country |
| **Update Frequency** | Annual releases (versioned) |
| **Format** | Shapefile/GeoJSON - individual country files |
| **File Size** | 1-50 MB per country |
| **Coordinate System** | WGS84 (EPSG:4326) |
| **License** | Open license, academic attribution required |

#### Strengths

- **Academic quality**: Peer-reviewed, documented methodology
- **Comprehensive**: Excellent global coverage
- **Versioned**: Clear version tracking for reproducibility
- **Smaller files**: Per-country downloads (not global database)
- **High levels**: Some countries have levels 4-5
- **API access**: Programmatic access available

#### Limitations

- **Variable quality**: Quality varies by country and level
- **Simplification**: Some geometries simplified for performance
- **Update lag**: Annual updates may not reflect recent changes

#### Recommended For

- Academic research requiring reproducibility
- Countries not well-covered by UNOCHA
- Studies needing fine-grained administrative levels (3-5)
- Smaller download footprint needed
- API-based workflows

#### Usage in laser-init

```shell
laser-init BRA 3 2010 2020 --shape-source geoboundaries
```

#### Data Attribution

**Citation**: Runfola, D. et al. (2020) geoBoundaries: A global database of political administrative boundaries. PLoS ONE 15(4): e0231866. https://doi.org/10.1371/journal.pone.0231866

---

### GADM (Database of Global Administrative Areas)

**Provider**: University of California, Berkeley / Global Administrative Areas

**URL**: https://gadm.org/

#### Characteristics

| Feature | Details |
|---------|---------|
| **Coverage** | All countries worldwide |
| **Administrative Levels** | 0-5, comprehensive coverage |
| **Update Frequency** | Regular updates (4-6 months) |
| **Format** | GeoPackage (.gpkg) - per country |
| **File Size** | 1-100 MB per country |
| **Coordinate System** | WGS84 (EPSG:4326) |
| **License** | Free for non-commercial use, attribution required |

#### Strengths

- **Comprehensive**: Best global coverage of all sources
- **Detailed**: High-resolution boundaries
- **Deep levels**: Many countries have 4-5 administrative levels
- **Frequent updates**: Regular updates from official sources
- **Rich attributes**: Names in multiple languages, codes, etc.
- **Well-documented**: Clear methodology and sources

#### Limitations

- **License restrictions**: Non-commercial use only (check license for your use case)
- **Variable quality**: Some remote regions have lower quality
- **Large files**: Some countries (USA, Brazil) have very large files

#### Recommended For

- General purpose spatial modeling
- Countries with deep administrative hierarchies
- Studies requiring multiple language names
- Fine-scale spatial resolution
- Non-commercial academic research

#### Usage in laser-init

```shell
laser-init IND 3 2010 2020 --shape-source gadm
```

#### Data Attribution

**Citation**: GADM database of Global Administrative Areas, version 4.1 [year]. Available from: https://gadm.org/

---

## Population Raster Sources

Population rasters provide gridded population counts used to estimate populations for administrative boundaries.

### WorldPop

**Provider**: WorldPop Research Group, University of Southampton

**URL**: https://www.worldpop.org/

#### Characteristics

| Feature | Details |
|---------|---------|
| **Coverage** | Global |
| **Resolution** | 100m (1 km aggregated available) |
| **Time Period** | 2000-2020 (historical), projections to 2030 |
| **Update Frequency** | Annual |
| **Format** | GeoTIFF (.tif) |
| **File Size** | 10-200 MB per country-year |
| **Method** | Random Forest disaggregation from census |
| **License** | Creative Commons Attribution 4.0 |

#### Strengths

- **High resolution**: 100m native resolution
- **Global coverage**: All countries
- **Time series**: Historical data 2000-2020
- **UN-adjusted**: Calibrated to UN population estimates
- **Open access**: Fully open data
- **Well-validated**: Extensive validation studies
- **Age/sex structure**: Additional datasets available

#### Limitations

- **Model-based**: Estimated, not observed counts
- **Temporal gaps**: Not all years available for all countries
- **Urban bias**: Better accuracy in urban areas
- **Uncertainty**: No uncertainty estimates provided in standard products

#### Recommended For

- Any spatial population analysis
- Studies requiring gridded population
- Fine-scale spatial resolution
- Time series population analysis

#### Usage in laser-init

```shell
# Default and only option (no flag needed)
laser-init KEN 2 2010 2020

# Explicit specification
laser-init KEN 2 2010 2020 --raster-source worldpop
```

#### How laser-init Uses WorldPop

1. Downloads the 1km aggregated raster for the specified year
2. Uses RasterToolkit to aggregate gridded population to administrative boundaries
3. Assigns population counts to each administrative unit

#### Data Attribution

**Citation**: WorldPop (www.worldpop.org - School of Geography and Environmental Science, University of Southampton). [Country] 100m Population. WorldPop, University of Southampton. https://doi.org/10.5258/SOTON/WP00647

---

## Demographic Statistics Sources

Demographic statistics provide birth rates, death rates, age distributions, and life expectancy used for vital dynamics in models.

### UN World Population Prospects (UN WPP)

**Provider**: United Nations Department of Economic and Social Affairs, Population Division

**URL**: https://population.un.org/wpp/

#### Characteristics

| Feature | Details |
|---------|---------|
| **Coverage** | All countries and territories |
| **Time Period** | 1950-2100 (historical + projections) |
| **Update Frequency** | Biennial (2022, 2024, etc.) |
| **Format** | CSV |
| **File Size** | ~50-200 MB total |
| **Variants** | Medium, High, Low fertility scenarios |
| **License** | Open access |

#### Indicators Available

laser-init extracts:

1. **Crude Birth Rate (CBR)**: Births per 1,000 population per year
2. **Crude Death Rate (CDR)**: Deaths per 1,000 population per year
3. **Population by Age and Sex**: 5-year age groups
4. **Life Table**: Complete life tables for mortality modeling

#### Strengths

- **Authoritative**: UN official estimates
- **Comprehensive**: All countries, long time series
- **Projections**: Future scenarios available
- **Well-documented**: Extensive methodology documentation
- **Consistent**: Standardized across all countries
- **Frequently updated**: New revision every 2 years

#### Limitations

- **National level**: No subnational variation
- **Model-based**: Projections are scenarios, not predictions
- **Revision changes**: Estimates can change between revisions

#### Recommended For

- Any demographic modeling
- Long-term projections
- Cross-country comparisons
- Standardized vital dynamics

#### Usage in laser-init

```shell
# Default and only option (no flag needed)
laser-init TZA 2 2010 2025

# Explicit specification
laser-init TZA 2 2010 2025 --stats-source unwpp
```

#### How laser-init Uses UN WPP

1. Downloads relevant CSV files from UN WPP 2024
2. Extracts CBR/CDR time series for the specified year range
3. Extracts population age distribution for the start year
4. Extracts life table for the start year
5. Saves to CSV files for use in model

#### Data Attribution

**Citation**: United Nations, Department of Economic and Social Affairs, Population Division (2024). World Population Prospects 2024, Online Edition. Available from: https://population.un.org/wpp/

---

## Data Source Comparison

### Administrative Boundaries: Head-to-Head

| Feature | UNOCHA | geoBoundaries | GADM |
|---------|--------|---------------|------|
| **Global Coverage** | Good | Excellent | Excellent |
| **Crisis Regions** | Excellent | Good | Good |
| **Admin Levels** | 0-3 | 0-5 | 0-5 |
| **Data Quality** | High | Medium-High | High |
| **Update Frequency** | Regular | Annual | 4-6 months |
| **File Size** | Large (global) | Medium (per-country) | Medium (per-country) |
| **License** | Public domain | Open (attribution) | Non-commercial only |
| **Best For** | Humanitarian | Research | General purpose |

## Selecting the Right Source

### By Use Case

#### Humanitarian Response
- **Primary**: UNOCHA (authoritative, crisis-focused)
- **Alternative**: GADM (if UNOCHA lacks coverage)

#### Academic Research
- **Primary**: geoBoundaries (versioned, reproducible)
- **Alternative**: GADM (more detailed)

#### General Disease Modeling
- **Primary**: UNOCHA (good balance of quality and coverage)
- **Alternative**: GADM (if more detail needed)

#### High-Resolution Spatial Analysis
- **Primary**: GADM (deepest admin levels)
- **Alternative**: geoBoundaries (also has deep levels)

### By Region

#### Africa
- **Best**: UNOCHA (excellent coverage, humanitarian focus)
- **Good**: GADM, geoBoundaries

#### Asia
- **Best**: GADM (comprehensive)
- **Good**: geoBoundaries, UNOCHA

#### Latin America
- **Best**: GADM (comprehensive)
- **Good**: geoBoundaries

#### Middle East
- **Best**: UNOCHA (crisis regions well-covered)
- **Good**: GADM

#### Europe, North America, Oceania
- **Best**: GADM (comprehensive)
- **Good**: geoBoundaries

## Data Quality Considerations

### Validation Steps

1. **Visual validation**: Generates choropleth for manual inspection

Possible future checks:

1. **Population aggregation**: Compares aggregated population to UN WPP national totals
2. **Coverage checks**: Ensures all regions have non-zero population

### Reproducibility

To ensure reproducible analysis:

1. **Save provenance.json**: Records exact data sources and timestamps
2. **Version control configs**: Track data source selection
3. **Document source choice**: Explain why you chose a particular source
4. **Cite appropriately**: Use source-specific citations
5. **Archive data**: Keep copies of downloaded source files

### Updating Data

Data sources update regularly. To get the latest data:

```shell
# Clear cache to force re-download
rm -rf ~/.laser/cache/

# Re-run laser-init
laser-init KEN 2 2010 2020
```

Check provenance.json timestamps to verify you have the latest data.

## Future Expansions

Potential future data source additions:

### Administrative Boundaries
- OpenStreetMap boundaries (community-maintained)
- National statistical office boundaries (country-specific)
- Natural Earth (simplified for mapping)

### Population Rasters
- LandScan (Oak Ridge National Laboratory)
- GHSL (Global Human Settlement Layer)
- Facebook HRSL (High Resolution Settlement Layer)
- GRID3 (Geo-Referenced Infrastructure and Demographic Data for Development)

### Demographics
- World Bank indicators
- WHO Global Health Observatory
- National census data (country-specific)
- DHS (Demographic and Health Surveys)

## Additional Resources

### Data Source Websites

- [UNOCHA HDX](https://data.humdata.org/)
- [geoBoundaries](https://www.geoboundaries.org/)
- [GADM](https://gadm.org/)
- [WorldPop](https://www.worldpop.org/)
- [UN WPP](https://population.un.org/wpp/)

### Methodological Documentation

- [WorldPop Methods](https://www.worldpop.org/methods/)
- [UN WPP Methodology](https://population.un.org/wpp/Publications/)
- [geoBoundaries Technical Docs](https://www.geoboundaries.org/dataDescription.html)

### Related Tools

- [QGIS](https://qgis.org/) - GIS software for viewing/editing spatial data
- [GeoPandas](https://geopandas.org/) - Python library for geospatial analysis
- [RasterToolkit](https://github.com/InstituteforDiseaseModeling/RasterToolkit) - Population aggregation tool used by laser-init

## Getting Help

For data source questions:
- Check original source documentation
- Post in GitHub Issues for laser-init-specific questions
- Contact data providers directly for data quality issues

---

**Last Updated**: March 2026
**Data Source Versions**: UNOCHA (latest), geoBoundaries v5.0, GADM v4.1, WorldPop 2020, UN WPP 2024
