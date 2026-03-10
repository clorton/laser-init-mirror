# laser-init - a tool to bootstrap spatial modeling with LASER

## Basic Usage

```shell
laser-init <country> <level> <start-year> <end-year>
```

`laser-init` requires a country, an administrative level, a starting year, and an ending year (inclusive)

`country` may be a country name, or preferrably, an ISO-3 code, e.g., "PAK"

`level` is generally in the range of [0-4] although shape data beyond level 2 may not be available or reliable

`laser-init` will attempt to download shapefile data for the selected country at the selected administrative (LGA) level and aggregate population data, using [RasterToolkit](https://github.com/InstituteforDiseaseModeling/RasterToolkit) from a population raster file with it to produce a [GeoPackage] file with both the administrative boundaries and the population of each LGA. `laser-init` will also attempt to download demographics statistics for the selected country over the specified time span and extract CBR and CDR for the time span, population age distribution as of the start (base) year, and a survival curve/life expectancy curve also as of the start/base year.

`laser-init` will then place the extracted data into a folder along with a generic [SI/SIR/SEIR] LASER model script and a supporting script for plotting simulation results. The model script, e.g. `seir.py` should be executable in the Python environment `laser-init` is installed into or any Python environment with [`laser.generic`](https://pypi.org/project/laser.generic/) installed.

Note: the default shapefile source, UNOCHA (see below), has a single, world-wide GeoDatabase which is quite large. However, `laser-init` will cache that file locally for future use.

## Example

```shell
laser-init NGA 2 2000 2025
```

End result:

```text
% ls -l NGA/2000 
total 12440
-rw-r--r--  1 user  staff  3170304 Mar 10 00:18 NGA_admin2.gpkg
-rw-r--r--  1 user  staff      265 Mar 10 00:18 age_dist.csv
-rw-r--r--  1 user  staff    73694 Mar 10 00:18 age_distribution.png
-rw-r--r--  1 user  staff    95107 Mar 10 00:18 cbr_cdr.png
-rw-r--r--  1 user  staff   628305 Mar 10 00:18 choropleth.png
-rw-r--r--  1 user  staff      328 Mar 10 00:18 config.yaml
-rw-r--r--  1 user  staff      500 Mar 10 00:18 cxr.csv
-rw-r--r--  1 user  staff      827 Mar 10 00:18 life_exp.csv
-rw-r--r--  1 user  staff    86740 Mar 10 00:18 life_expectancy.png
-rw-r--r--  1 user  staff    19152 Mar 10 00:18 plot.py
-rw-r--r--@ 1 user  staff     1898 Mar 10 00:18 provenance.json
-rw-r--r--@ 1 user  staff  1387855 Mar 10 00:18 report.pdf
-rw-r--r--  1 user  staff     3301 Mar 10 00:18 seir.py
```

The .png files in the directory give some visuals for validation of the downloaded data. `report.pdf` is merely a single PDF file with the same visuals.

`provenance.json` contains information about the sources of the data in the geopackage and csv files.

`seir.py` will run a LASER implementation of an SEIR ABM with the number of population nodes and population found in the `NGA_admin2.gpkg` geopackage file. It will references `config.yaml` to find these data files, so `seir.py`, `plot.py`, and `config.yaml` could be moved to another location. `config.yaml` also contains some basic disease dynamics parameters.


## Options

### `--shape-source`

Currently three shapefile sources are supported:

- [UNOCHA](https://knowledge.base.unocha.org/wiki/spaces/imtoolbox/pages/2557378679/Administrative+Boundaries+COD-AB)
- [geoBoundaries](https://github.com/wmgeolab/geoBoundaries/)
- [GADM](https://gadm.org/)

### `--raster-source`

Currently only one population raster file source is supported:

- [WorldPop](https://hub.worldpop.org/)

### `--stats-source`

Currently only one demographics statistics source is supported:

- [UN World Population Prospects](https://population.un.org/wpp/)
