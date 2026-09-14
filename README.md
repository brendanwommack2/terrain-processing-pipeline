# Upper Manistee Terrain Processing Pipeline

An automated geospatial processing pipeline for turning raw elevation and hydrography data into analysis-ready terrain products for the Upper Manistee River study area in Michigan.

The project is designed as a portfolio project emphasizing reproducible geospatial data processing, DEM quality control, hydrologic terrain conditioning, raster/vector data management, automation, and validation.

## Project Status

**Current stage:** Study-area definition and data preparation

Completed:
- Project environment and repository structure created
- Python 3.14.7 virtual environment configured
- Core geospatial Python packages installed and tested
- Git repository initialized and pushed to GitHub
- USGS Watershed Boundary Dataset (WBD) HU-2 Region 04 GeoPackage acquired
- Manistee HUC-8 identified
- Four HUC-10 units selected as the working Upper Manistee study area
- 33 HUC-12 units identified within those HUC-10s
- HUC-12s dissolved into a single study-area boundary
- Boundary saved as a GeoPackage

Next major stage:
- Select and acquire an appropriate USGS 3DEP DEM
- Build the DEM acquisition, processing, conditioning, and QA/QC pipeline

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

### Watershed Boundary Dataset

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

## 4. Repository Structure

Current/planned structure:

```text
terrain-processing-pipeline/
├── README.md
├── data/
│   ├── raw/
│   │   └── WBD_04_HU2_GPKG.gpkg
│   └── boundary/
│       └── upper_manistee_boundary.gpkg
├── src/
│   ├── acquisition/
│   │   ├── download_dem.py
│   │   └── download_hydro.py
│   ├── processing/
│   │   ├── mosaic.py
│   │   ├── reproject.py
│   │   ├── condition_dem.py
│   │   └── derive_terrain.py
│   ├── validation/
│   │   ├── raster_qc.py
│   │   ├── vector_qc.py
│   │   └── terrain_qc.py
│   └── pipeline.py
├── tests/
│   ├── test_raster.py
│   ├── test_vector.py
│   └── test_pipeline.py
├── configs/
│   └── upper_manistee.yaml
├── outputs/
│   ├── raw/
│   ├── conditioned/
│   ├── flow/
│   └── qa/
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

Additional packages/tools may be added as the pipeline develops.

Potential future tooling includes:

- GDAL
- WhiteboxTools / Whitebox
- pysheds
- xarray
- pyarrow
- GeoParquet tooling
- pytest

A Rust component may also be added later to demonstrate work with compiled geospatial processing/validation tooling.

---

## 6. Work Completed

### 6.1 Repository setup

The project was created locally at:

```text
C:\Users\jbwom\Downloads\PersonalProjects\terrain-processing-pipeline
```

A Git repository was initialized and pushed to GitHub.

The repository is intended to contain the processing code, documentation, configuration, tests, and lightweight project metadata—not the large raw datasets.

### 6.2 WBD acquisition

The USGS WBD HU-2 Region 04 GeoPackage was downloaded and extracted into:

```text
data/raw/WBD_04_HU2_GPKG.gpkg
```

The GeoPackage contains the WBD hierarchy needed to define the study area.

### 6.3 Manistee HUC-8 identification

The `WBDHU8` layer was inspected.

The Manistee watershed was identified as:

```text
HUC-8: 04060103
Name: Manistee
```

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

### 6.5 HUC-12 inspection

The `WBDHU12` layer was filtered using the four selected HUC-10 identifiers.

This produced:

```text
33 HUC-12 features
```

These were then dissolved into a single study-area polygon.

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

## 7. Planned Processing Workflow

The final pipeline is expected to follow this general sequence:

```text
USGS 3DEP DEM
      │
      ▼
Data acquisition + provenance
      │
      ▼
Raw DEM validation
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
DEM conditioning
      │
      ├── NoData / void handling
      ├── sink handling
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
Hydrography QA/QC
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

### Step 1 — Select the DEM source

Determine the most appropriate USGS 3DEP product and resolution for the 3,352.73 km² study area.

The choice should balance:

- spatial resolution
- data volume
- processing time
- coverage
- licensing/provenance
- suitability for hydrologic terrain analysis

The project should document why the selected DEM product was chosen.

### Step 2 — Determine DEM tile coverage

Use the study-area boundary to determine which elevation tiles intersect the Upper Manistee study area.

The goal is to acquire only the necessary data rather than downloading an unnecessarily large regional dataset.

### Step 3 — Build DEM acquisition script

Create:

```text
src/acquisition/download_dem.py
```

The script should eventually:

- identify required DEM tiles
- download them
- preserve source metadata
- record provenance
- verify downloaded files
- avoid downloading files that already exist

### Step 4 — Build raster QA/QC

Create:

```text
src/validation/raster_qc.py
```

Initial checks should include:

- CRS
- pixel dimensions
- spatial resolution
- raster width/height
- bounding box
- NoData value
- datatype
- minimum/maximum elevation
- file readability
- missing/corrupt tiles

Later checks can include:

- compression
- tiling
- COG compliance
- internal overviews

### Step 5 — Mosaic and clip DEM

Create processing tools for:

- mosaicking tiles
- clipping to the Upper Manistee boundary
- reprojection
- raster alignment
- resampling when necessary

### Step 6 — Hydrologic conditioning

Develop:

```text
src/processing/condition_dem.py
```

Potential operations:

- sink identification
- sink filling
- depression handling
- hydrographic enforcement / stream burning
- before/after validation

The exact conditioning method should be documented and justified rather than treated as a black box.

### Step 7 — Terrain derivatives

Generate:

- slope
- aspect
- flow direction
- flow accumulation
- potentially watershed/catchment products

### Step 8 — Vector QA/QC

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
- alignment between hydrography and terrain

### Step 9 — Automated testing

Use `pytest` to create tests for:

- raster metadata
- expected CRS
- expected dimensions/resolution
- geometry validity
- pipeline configuration
- processing functions
- edge cases

### Step 10 — Reproducible configuration

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
- output locations

This will allow the pipeline to be rerun for another study area without rewriting the processing code.

---

## 9. Portfolio / Lynker Relevance

This project is being developed to demonstrate skills relevant to geospatial scientist roles involving large-scale terrain and hydrographic processing.

Particular emphasis will be placed on:

### DEM acquisition and management

- source discovery
- provenance
- tile management
- metadata
- licensing/source documentation

### Raster processing

- mosaicking
- clipping
- reprojection
- resampling
- NoData handling
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

A small Rust utility may be added later to demonstrate the ability to work with a Rust-based geospatial codebase.

---

## 10. Data Management

Raw and generated large datasets should not be committed to Git.

The repository should contain:

- source code
- configuration files
- tests
- documentation
- metadata
- small example datasets where appropriate

Large raw and generated datasets should remain outside the Git repository and be referenced through documentation.

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

### DEM resolution

The DEM resolution has **not yet been selected**.

The next stage should evaluate available 3DEP products before committing to a resolution.

### Hydrologic conditioning method

No conditioning method has been implemented yet. The final method should be selected based on the DEM characteristics and hydrography available for the study area.

---

## 12. Reproducibility Principle

A central goal of this project is that another geospatial professional should be able to understand:

1. Where the data came from
2. Why the study area was selected
3. What transformations were applied
4. What assumptions were made
5. How data quality was evaluated
6. How to reproduce the outputs

The final project should therefore document not only the final maps and terrain products, but also the **processing decisions, validation results, and provenance of the input data**.
