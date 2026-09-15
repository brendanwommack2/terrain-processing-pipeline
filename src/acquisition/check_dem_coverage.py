from pathlib import Path
import re

import geopandas as gpd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BOUNDARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "boundary"
    / "upper_manistee_boundary.gpkg"
)


def main():

    # Read study area
    boundary = gpd.read_file(
        BOUNDARY_PATH,
        layer="upper_manistee",
    )

    print("Study area:")
    print(f"  CRS: {boundary.crs}")

    # Project-based Michigan DEMs are in UTM Zone 16N
    boundary_utm = boundary.to_crs("EPSG:32616")

    bounds = boundary_utm.total_bounds
    min_x, min_y, max_x, max_y = bounds

    print("\nBoundary bounds in UTM Zone 16N:")
    print(f"  X: {min_x:.0f} → {max_x:.0f}")
    print(f"  Y: {min_y:.0f} → {max_y:.0f}")

    # Determine the 10-km DEM tiles intersecting the boundary.
    # Tile names use x##y### where the numbers represent
    # 10-km UTM grid positions.
    min_x_tile = int(min_x // 10000)
    max_x_tile = int(max_x // 10000)

    min_y_tile = int(min_y // 10000)
    max_y_tile = int(max_y // 10000)

    print("\n10-km tile range covering the boundary:")
    print(f"  X: {min_x_tile} → {max_x_tile}")
    print(f"  Y: {min_y_tile} → {max_y_tile}")

    print("\nExpected tile names:")

    for x in range(min_x_tile, max_x_tile + 1):
        for y in range(min_y_tile, max_y_tile + 1):
            print(f"  x{x}y{y}")


if __name__ == "__main__":
    main()