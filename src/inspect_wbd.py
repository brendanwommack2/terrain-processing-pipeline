import geopandas as gpd
from pathlib import Path

gpkg = "data/raw/WBD_04_HU2_GPKG.gpkg"

# HUC-10 units defining our working Upper Manistee study area
upper_huc10 = [
    "0406010301",
    "0406010302",
    "0406010303",
    "0406010305"
]

print("Reading WBDHU12 layer...")
wbd12 = gpd.read_file(gpkg, layer="WBDHU12")

# Select all HUC-12s within the four Upper Manistee HUC-10s
upper_huc12 = wbd12[
    wbd12["huc12"].str[:10].isin(upper_huc10)
].copy()

print(f"Selected HUC-12 features: {len(upper_huc12)}")

# Dissolve into a single study-area boundary
boundary = upper_huc12.dissolve()

# Create boundary directory
output_dir = Path("data/boundary")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "upper_manistee_boundary.gpkg"

# Save
boundary.to_file(
    output_file,
    layer="upper_manistee",
    driver="GPKG"
)

print()
print(f"Saved boundary to: {output_file}")
print(f"CRS: {boundary.crs}")
print(f"Area (sq km): {boundary.to_crs('EPSG:5070').area.iloc[0] / 1_000_000:.2f}")