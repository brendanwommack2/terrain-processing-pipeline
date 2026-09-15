# Upper Manistee Terrain Processing Pipeline

An automated geospatial processing pipeline for turning raw elevation and hydrography data into analysis-ready terrain products for the Upper Manistee River study area in Michigan.

The project is designed as a portfolio project emphasizing reproducible geospatial data processing, DEM quality control, hydrologic terrain conditioning, raster/vector data management, automation, and validation.

---

## Project Status

**Current stage:** DEM acquisition completed; beginning DEM inventory and quality control

### Completed

- Project environment and repository structure created
- Python 3.14.7 virtual environment configured
- Core geospatial Python packages installed and tested
- Git repository initialized and pushed to GitHub
- `.gitignore` configured to exclude large raw and generated datasets
- USGS Watershed Boundary Dataset (WBD) HU-2 Region 04 GeoPackage acquired
- Manistee HUC-8 identified
- Four HUC-10 units selected as the working Upper Manistee study area
- 33 HUC-12 units identified within those HUC-10s
- HUC-12s dissolved into a single study-area boundary
- Study-area boundary saved as a GeoPackage
- USGS 3DEP DEM sources evaluated
- USGS Seamless 1-meter DEM (S1M) evaluated and determined not to provide coverage for the study area
- USGS 3DEP project-based 1-meter DEM products identified through the TNM Access API
- DEM tile coverage intersecting the study area evaluated across available 1-meter projects
- 71 required 1-meter DEM tiles selected
- DEM download URLs and source information recorded in an acquisition manifest
- All 71 DEM tiles successfully downloaded and verified
- Downloaded DEMs stored locally outside Git
- DEM acquisition script created with download verification and restart-safe behavior

### Current stage

The project is now moving from **data acquisition** into **DEM inventory and quality control**.

### Next major stages

1. Inventory and validate the downloaded DEM tiles
2. Analyze overlaps between DEM acquisition projects
3. Resolve project-to-project DEM differences and determine a mosaicking strategy
4. Mosaic and clip the DEM to the Upper Manistee study area
5. Acquire and validate hydrography data
6. Develop hydrologic terrain conditioning
7. Generate flow and terrain derivatives
8. Implement automated raster/vector QA/QC
9. Convert final outputs to efficient formats such as COG and GeoParquet
10. Add automated tests and configuration-driven execution

---

## 1. Project Goals

The primary goal is to build a reproducible workflow that demonstrates how raw elevation and hydrography data can be transformed into analysis-ready terrain data.

The pipeline will ultimately support:

1. DEM acquisition and provenance tracking
2. Raster validation and quality control
3. DEM mosaicking and clipping
4. CRS/reprojection and raster alignment
5. Hydrologic terrain conditioning
6. Flow direction and flow accumulation
7. Hydrography/vector QA/QC
8. Efficient raster/vector data storage
9. Automated validation and testing
10. Reproducible, configuration-driven processing

The project is intentionally focused on the **pipeline and quality-control process**, rather than simply producing a finished map.

---

## 2. Study Area

### Upper Manistee River, Michigan

The project uses the USGS Watershed Boundary Dataset (WBD) hierarchy to establish a reproducible working definition of the Upper Manistee study area.

The Manistee River basin is represented by HUC-8:

- **HUC-8:** `04060103`
- **Name:** Manistee

The working Upper Manistee study area consists of these four HUC-10 watersheds:

| HUC-10 | Name |
|---|---|
| `0406010301` | North Branch Manistee River-Manistee River |
| `0406010302` | Silver Creek-Manistee River |
| `0406010303` | Peterson Creek-Manistee River |
| `0406010305` | Bear Creek |

These four HUC-10s contain **33 HUC-12 watersheds**.

The HUC-12 watersheds were dissolved into a single polygon to create the project study-area boundary.

### Important boundary note

"Upper Manistee River" is being used here as a **working study-area definition**, not as an assertion that USGS officially defines "Upper Manistee" as a single HUC-10 or HUC-12 unit.

For reproducibility, the project explicitly defines the study area as the four HUC-10 units listed above. This definition can be revised later if a specific watershed-management organization or agency source provides a preferred boundary.

### Current boundary

- **Number of HUC-12 units:** 33
- **Boundary CRS:** EPSG:4269 (NAD83)
- **Area:** 3,352.73 km²
- **Area:** approximately 1,294 sq mi
- **File:** `data/boundary/upper_manistee_boundary.gpkg`
- **Layer:** `upper_manistee`

---

## 3. Data Sources

### 3.1 Watershed Boundary Dataset

Source:

**USGS Watershed Boundary Dataset (WBD), HU-2 Region 04 — Great Lakes**

The downloaded GeoPackage contains WBD hierarchy layers including:

- WBDHU2
- WBDHU4
- WBDHU6
- WBDHU8
- WBDHU10
- WBDHU12
- WBDLine

The project currently uses:

- `WBDHU8` to identify the Manistee HUC-8
- `WBDHU10` to identify the four working Upper Manistee HUC-10s
- `WBDHU12` to identify the 33 constituent HUC-12s

### Local WBD file

The downloaded source is stored under:

```text
data/raw/WBD_04_HU2_GPKG.gpkg
```

The raw source data is intentionally excluded from Git because of its size.

---

### 3.2 USGS 3DEP 1-meter DEM

The project uses USGS 3DEP 1-meter DEM products as the elevation source.

The DEM acquisition process was performed using the **USGS The National Map (TNM) Access API** to identify products intersecting the study-area boundary.

Because the 1-meter DEM products are organized by acquisition project, the study area is covered by DEMs from multiple projects.

The selected acquisition projects are:

- `MI_13County_2015_C16`
- `MI_FEMA_2019_C19`
- `MI Wexford 2016`
- `MI Missaukee 2016`
- `MI_16Co_Roscommon_2015`

A total of **71 1-meter DEM tiles** were selected and downloaded.

### DEM acquisition summary

| Acquisition project | Tiles |
|---|---:|
| MI_13County_2015_C16 | 26 |
| MI_FEMA_2019_C19 | 24 |
| MI Wexford 2016 | 19 |
| MI Missaukee 2016 | 1 |
| MI_16Co_Roscommon_2015 | 1 |
| **Total** | **71** |

The downloaded DEMs occupy approximately **16.6 GB** on disk.

The DEM files are stored locally under:

```text
data/raw/dem/
```

They are intentionally excluded from Git.

### DEM acquisition manifest

Source URLs, tile information, and acquisition records are preserved in:

```text
data/raw/dem_acquisition_manifest.csv
```

This manifest is an important part of the project's provenance and reproducibility workflow.

---

### 3.3 Seamless 1-meter DEM evaluation

The newer USGS Seamless 1-meter DEM (S1M) product was investigated as a potential alternative to the project-based DEM products.

The project downloaded and inspected the S1M spatial metadata index and tested it against the Upper Manistee study-area boundary.

The available S1M index did **not** contain tiles intersecting the Upper Manistee study area.

As a result, S1M was not used for this project.

This decision is documented rather than simply assuming that the newest available 1-meter product provides coverage.

The downloaded S1M metadata used for this evaluation is retained locally under:

```text
data/raw/metadata/S1M_Products.gpkg
```

---

## 4. Repository Structure

Current and planned structure:

```text
terrain-processing-pipeline/

├── README.md
│
├── data/
│   ├── raw/
│   │   ├── dem/
│   │   │   └── *.tif
│   │   ├── metadata/
│   │   │   └── S1M_Products.gpkg
│   │   ├── WBD_04_HU2_GPKG.gpkg
│   │   └── dem_acquisition_manifest.csv
│   │
│   └── boundary/
│       └── upper_manistee_boundary.gpkg
│
├── src/
│   ├── acquisition/
│   │   ├── download_dem.py
│   │   └── download_hydro.py
│   │
│   ├── processing/
│   │   ├── mosaic.py
│   │   ├── reproject.py
│   │   ├── condition_dem.py
│   │   └── derive_terrain.py
│   │
│   ├── validation/
│   │   ├── raster_qc.py
│   │   ├── vector_qc.py
│   │   └── terrain_qc.py
│   │
│   └── pipeline.py
│
├── tests/
│   ├── test_raster.py
│   ├── test_vector.py
│   └── test_pipeline.py
│
├── configs/
│   └── upper_manistee.yaml
│
├── outputs/
│   ├── raw/
│   ├── conditioned/
│   ├── flow/
│   └── qa/
│
└── docs/
    ├── methodology.md
    └── data_dictionary.md
```

Some directories and files above are planned rather than completed.

---

## 5. Environment

The project uses a Python virtual environment with:

```text
Python 3.14.7
```

Core packages currently installed and tested:

- rasterio
- geopandas
- shapely
- pyproj
- numpy
- matplotlib
- requests
- git-filter-repo

Additional packages/tools may be added as the pipeline develops.

Potential future tooling includes:

- GDAL
- WhiteboxTools / Whitebox
- pysheds
- xarray
- pyarrow
- GeoParquet tooling
- pytest

A Rust component may also be added later to demonstrate work with compiled geospatial processing and validation tooling.

---

## 6. Work Completed

### 6.1 Repository setup

The project was created locally at:

```text
C:\Users\jbwom\Downloads\PersonalProjects\terrain-processing-pipeline
```

A Git repository was initialized and pushed to GitHub.

The repository is intended to contain processing code, documentation, configuration, tests, and lightweight project metadata rather than large raw datasets.

Large data files were removed from Git history after an initial accidental commit and the repository was successfully pushed with the large files excluded.

---

### 6.2 WBD acquisition

The USGS WBD HU-2 Region 04 GeoPackage was downloaded and extracted into:

```text
data/raw/WBD_04_HU2_GPKG.gpkg
```

The GeoPackage contains the WBD hierarchy needed to define the study area.

---

### 6.3 Manistee HUC-8 identification

The `WBDHU8` layer was inspected.

The Manistee watershed was identified as:

```text
HUC-8: 04060103
Name: Manistee
```

---

### 6.4 HUC-10 inspection

The `WBDHU10` layer was filtered to HUC-10s beginning with `04060103`.

Seven HUC-10 units were identified:

```text
0406010301  North Branch Manistee River-Manistee River
0406010302  Silver Creek-Manistee River
0406010303  Peterson Creek-Manistee River
0406010304  Pine River
0406010305  Bear Creek
0406010306  Little Manistee River
0406010307  Manistee River
```

The four HUC-10s selected for the working Upper Manistee study area are:

```text
0406010301
0406010302
0406010303
0406010305
```

---

### 6.5 HUC-12 inspection

The `WBDHU12` layer was filtered using the four selected HUC-10 identifiers.

This produced:

```text
33 HUC-12 features
```

These were then dissolved into a single study-area polygon.

---

### 6.6 Study-area boundary creation

The resulting boundary was saved as:

```text
data/boundary/upper_manistee_boundary.gpkg
```

The output uses:

```text
EPSG:4269
```

For area calculation, the boundary was temporarily projected to EPSG:5070, resulting in an area of:

```text
3,352.73 km²
```

---

### 6.7 DEM source evaluation

Several USGS 3DEP 1-meter DEM products were evaluated against the study-area boundary.

The analysis identified DEM tiles by their actual geographic bounding boxes rather than relying only on tile naming conventions.

This showed that the Upper Manistee study area is covered by multiple 3DEP acquisition projects.

A project-level coverage analysis was performed to determine which tiles were required and to avoid downloading unnecessary data.

---

### 6.8 DEM acquisition

A final set of **71 1-meter DEM tiles** was selected.

The selected tiles were verified before downloading. Every selected source URL returned successfully.

The acquisition script was designed to:

- read the acquisition manifest
- download one tile at a time
- display progress
- skip already completed files
- write to a temporary `.part` file
- verify the downloaded file size
- rename the file only after successful verification
- report failed downloads
- allow the process to be safely restarted

All 71 tiles were successfully downloaded.

Final acquisition result:

```text
Manifest tiles: 71
Already complete: 0
Downloaded: 71
Failed: 0
Elapsed time: approximately 13.6 minutes
DEM files on disk: 71
DEM disk usage: approximately 16.61 GB
```

The acquisition manifest is retained at:

```text
data/raw/dem_acquisition_manifest.csv
```

---

## 7. Planned Processing Workflow

The final pipeline is expected to follow this general sequence:

```text
USGS 3DEP DEM
      │
      ▼
Data acquisition + provenance
      │
      ▼
Raw DEM inventory + QA/QC
      │
      ▼
Resolve overlapping DEM projects
      │
      ▼
Mosaic / tile management
      │
      ▼
Clip to Upper Manistee
      │
      ▼
CRS + resolution alignment
      │
      ▼
Hydrography acquisition
      │
      ▼
Hydrography QA/QC
      │
      ▼
DEM conditioning
      │
      ├── NoData / void handling
      ├── sink/depression handling
      └── hydrographic enforcement
      │
      ▼
Flow direction
      │
      ▼
Flow accumulation
      │
      ▼
Terrain derivatives
      ├── slope
      ├── aspect
      └── elevation statistics
      │
      ▼
Automated validation
      │
      ▼
Analysis-ready outputs
      │
      ├── COG raster
      └── GeoParquet/vector outputs
```

---

## 8. Immediate Next Steps

### Step 1 — Build DEM inventory and QA/QC

Create the initial raster validation tool:

```text
src/validation/raster_qc.py
```

The first version should inspect all 71 DEMs without loading the entire dataset into memory.

Initial checks should include:

- file readability
- CRS
- pixel size
- raster width/height
- number of bands
- datatype
- NoData value
- spatial bounds
- elevation minimum/maximum
- file size
- transform
- consistency between tiles

The tool should produce a machine-readable inventory, such as:

```text
outputs/qa/dem_inventory.csv
```

and a concise QA summary.

---

### Step 2 — Analyze DEM overlaps

Because the selected DEMs originate from multiple acquisition projects, overlapping coverage needs to be evaluated before mosaicking.

The analysis should determine:

- which tiles overlap
- which projects overlap
- how much area is affected
- whether overlapping projects have different resolutions or metadata
- whether elevation differences exist between overlapping datasets

This is an important part of the project because the USGS 1-meter DEM products are organized by acquisition project rather than being a single uniformly acquired regional surface.

The mosaicking strategy should therefore be based on an explicit, documented decision rather than simply combining all files in arbitrary order.

---

### Step 3 — Acquire hydrography

Identify an appropriate hydrography dataset for the study area.

Potential sources include USGS 3D Hydrography Program (3DHP) or other appropriate USGS hydrography products.

The selected hydrography should be documented in the same way as the DEM:

- source
- version
- date
- spatial coverage
- resolution/scale
- coordinate reference system
- download location
- licensing/public-domain status
- processing applied

Create:

```text
src/acquisition/download_hydro.py
```

if automated acquisition is appropriate.

---

### Step 4 — Mosaic and clip DEM

Develop tools for:

- mosaicking DEM tiles
- resolving overlaps
- clipping to the Upper Manistee boundary
- maintaining consistent CRS
- maintaining 1-meter resolution
- preserving appropriate NoData handling

The goal is to produce a clean study-area DEM suitable for subsequent terrain processing.

---

### Step 5 — Hydrologic conditioning

Develop:

```text
src/processing/condition_dem.py
```

Potential operations include:

- identifying sinks/depressions
- filling or breaching depressions where appropriate
- handling NoData/void areas
- hydrographic enforcement / stream burning
- validating the terrain before and after conditioning

The conditioning method should be explicitly justified and documented.

---

### Step 6 — Generate terrain and hydrologic derivatives

Generate:

- slope
- aspect
- flow direction
- flow accumulation
- drainage/network products
- potentially watershed or catchment delineations

These outputs will demonstrate that the processed DEM is suitable for hydrologic terrain analysis.

---

### Step 7 — Vector QA/QC

Develop:

```text
src/validation/vector_qc.py
```

Checks should eventually include:

- invalid geometries
- duplicate features
- missing attributes
- geometry type consistency
- topology
- connectivity
- spatial alignment
- hydrography/terrain consistency

---

### Step 8 — Final terrain QA/QC

Develop:

```text
src/validation/terrain_qc.py
```

Potential checks include:

- remaining NoData areas
- remaining sinks/depressions
- stream/terrain alignment
- flow connectivity
- elevation anomalies
- raster continuity across tile boundaries
- expected study-area coverage
- consistency between terrain derivatives

---

### Step 9 — Efficient output formats

Final analysis-ready datasets should use appropriate geospatial formats.

Potential outputs include:

- Cloud Optimized GeoTIFF (COG)
- GeoParquet
- GeoPackage

The project should document why each format was selected and validate the resulting files.

---

### Step 10 — Automated testing

Use `pytest` to create tests for:

- raster metadata
- expected CRS
- expected resolution
- expected dimensions
- geometry validity
- pipeline configuration
- processing functions
- edge cases
- QA/QC functions

---

### Step 11 — Reproducible configuration

Create:

```text
configs/upper_manistee.yaml
```

The configuration should eventually contain parameters such as:

- study-area path
- DEM source
- target CRS
- target resolution
- NoData handling
- conditioning parameters
- hydrography source
- output locations

This will allow the pipeline to be rerun for another study area without rewriting the processing code.

---

## 9. Portfolio / Lynker Relevance

This project is being developed to demonstrate skills relevant to geospatial scientist roles involving large-scale terrain and hydrographic processing.

Particular emphasis will be placed on:

### DEM acquisition and management

- source discovery
- API-based acquisition
- provenance
- tile management
- metadata
- coverage analysis
- licensing/source documentation

### Raster processing

- mosaicking
- clipping
- reprojection
- resampling
- NoData handling
- overlap management
- large raster management

### Hydrologic terrain processing

- sink/depression handling
- hydrographic enforcement
- flow direction
- flow accumulation
- watershed delineation

### Vector QA/QC

- geometry validation
- topology
- hydrography alignment
- attribute validation
- connectivity

### Efficient geospatial formats

Potential final outputs include:

- Cloud Optimized GeoTIFF (COG)
- GeoParquet
- GeoPackage

### Software engineering

The project will emphasize:

- modular Python
- command-line workflows
- automated tests
- configuration-driven processing
- Git/GitHub
- reproducibility
- documentation
- validation

A small Rust utility may be added later to demonstrate the ability to work with a Rust-based geospatial codebase.

---

## 10. Data Management

Raw and generated large datasets should not be committed to Git.

The repository should contain:

- source code
- configuration files
- tests
- documentation
- lightweight metadata
- acquisition manifests
- small example datasets where appropriate

Large raw and generated datasets remain outside the Git repository and are referenced through documentation and manifests.

### Current raw data

The project currently maintains approximately 16.6 GB of DEM data locally:

```text
data/raw/dem/
```

along with the WBD GeoPackage and supporting metadata.

These files are excluded from Git through `.gitignore`.

### Acquisition provenance

DEM acquisition information is preserved in:

```text
data/raw/dem_acquisition_manifest.csv
```

This allows the source URLs and selected tiles to be reconstructed without storing the large raster files in the repository.

Before adding additional data, verify that `.gitignore` is correctly named:

```text
.gitignore
```

and not:

```text
.gitignore.txt
```

The intended ignore rules include:

```text
.venv/

__pycache__/
*.py[cod]
.pytest_cache/

data/*
!data/.gitkeep

outputs/*

.DS_Store
Thumbs.db
.vscode/
```

---

## 11. Current Limitations / Decisions to Revisit

### Upper Manistee boundary

The current boundary is a project-defined working boundary based on four HUC-10s. It should not be presented as an official USGS "Upper Manistee" watershed designation.

If a specific management organization or agency provides a more appropriate Upper Manistee boundary, the project can compare the two and document the final decision.

### DEM source

The project selected USGS 3DEP project-based 1-meter DEMs after evaluating available coverage.

The newer Seamless 1-meter DEM (S1M) was investigated but did not provide coverage for the Upper Manistee study area.

The selected 71 tiles originate from multiple acquisition projects, so overlap and cross-project consistency must be evaluated before producing the final mosaic.

### DEM resolution

The working DEM resolution is **1 meter** based on the selected USGS 3DEP products.

The final processing workflow should preserve this resolution unless a specific processing step justifies resampling.

### DEM overlap

Multiple 3DEP acquisition projects overlap portions of the study area.

The project has not yet determined the final priority/order for resolving these overlaps. This will be addressed during DEM QA/QC and mosaicking.

### Hydrologic conditioning

No conditioning method has been implemented yet.

The final method should be selected based on:

- DEM characteristics
- hydrography source
- intended hydrologic analysis
- treatment of sinks/depressions
- treatment of streams
- reproducibility

---

## 12. Reproducibility Principle

A central goal of this project is that another geospatial professional should be able to understand:

1. Where the data came from
2. Why the study area was selected
3. Why the DEM source was selected
4. What transformations were applied
5. What assumptions were made
6. How overlapping datasets were handled
7. How data quality was evaluated
8. How to reproduce the outputs

The final project should therefore document not only the final maps and terrain products, but also the **processing decisions, validation results, and provenance of the input data**.

The DEM acquisition stage demonstrates this principle by preserving both the acquisition manifest and the reasoning behind the selected 1-meter dataset.

The next major focus is therefore **DEM QA/QC and overlap analysis before mosaicking**.