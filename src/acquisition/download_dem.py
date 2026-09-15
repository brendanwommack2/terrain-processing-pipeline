from pathlib import Path
import csv
import sys
import time
import requests


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST_PATH = PROJECT_ROOT / "data" / "raw" / "dem_acquisition_manifest.csv"
DOWNLOAD_DIR = PROJECT_ROOT / "data" / "raw" / "dem"

CHUNK_SIZE = 1024 * 1024  # 1 MB
TIMEOUT = 60
MAX_RETRIES = 5


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def format_bytes(num_bytes):
    """Return a human-readable file size."""
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(num_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def load_manifest():
    """Read the verified DEM acquisition manifest."""
    if not MANIFEST_PATH.exists():
        print(f"ERROR: Manifest not found:")
        print(f"  {MANIFEST_PATH}")
        sys.exit(1)

    with MANIFEST_PATH.open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("ERROR: Manifest is empty.")
        sys.exit(1)

    return rows


def get_value(row, possible_names, required=True):
    """
    Find a value in a manifest row using several possible column names.
    """
    for name in possible_names:
        if name in row and row[name] not in ("", None):
            return row[name]

    if required:
        raise KeyError(
            f"Could not find any of these columns: {possible_names}\n"
            f"Available columns: {list(row.keys())}"
        )

    return None


def get_filename(row):
    """Get the local filename from the manifest or derive it from the URL."""

    filename = get_value(
        row,
        ["filename", "file_name", "name"],
        required=False,
    )

    if filename:
        return Path(filename).name

    url = get_value(
        row,
        ["download_url", "downloadURL", "url"],
    )

    return Path(url.split("?")[0]).name


def get_url(row):
    """Get the download URL from the manifest."""

    return get_value(
        row,
        ["download_url", "downloadURL", "url"],
    )


def get_expected_size(row):
    """
    Get expected byte count from the manifest.

    The verification step you already ran recorded the actual sizes,
    so this should normally be present.
    """

    value = get_value(
        row,
        [
            "actual_size_bytes",
            "size_bytes",
            "sizeInBytes",
            "nbytes",
            "expected_size_bytes",
        ],
        required=False,
    )

    if value is None:
        return None

    try:
        return int(float(value))
    except ValueError:
        return None


def download_file(url, destination, expected_size=None):
    """
    Download one file to destination.part.

    Returns:
        True if successful
        False if unsuccessful
    """

    part_path = destination.with_suffix(destination.suffix + ".part")

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            print()
            print(f"Downloading:")
            print(f"  {destination.name}")
            print(f"  Attempt {attempt}/{MAX_RETRIES}")

            # Start fresh for this attempt.
            if part_path.exists():
                part_path.unlink()

            with requests.get(
                url,
                stream=True,
                timeout=TIMEOUT,
            ) as response:

                response.raise_for_status()

                total_size = response.headers.get("content-length")

                if total_size is not None:
                    total_size = int(total_size)

                downloaded = 0
                start_time = time.time()

                with part_path.open("wb") as f:

                    for chunk in response.iter_content(
                        chunk_size=CHUNK_SIZE
                    ):

                        if not chunk:
                            continue

                        f.write(chunk)
                        downloaded += len(chunk)

                        elapsed = max(time.time() - start_time, 0.001)
                        speed = downloaded / elapsed

                        if total_size:
                            percent = downloaded / total_size * 100

                            print(
                                f"\r  Progress: {percent:6.2f}% "
                                f"({format_bytes(downloaded)} / "
                                f"{format_bytes(total_size)}) "
                                f"| {format_bytes(speed)}/s",
                                end="",
                                flush=True,
                            )
                        else:
                            print(
                                f"\r  Downloaded: "
                                f"{format_bytes(downloaded)} "
                                f"| {format_bytes(speed)}/s",
                                end="",
                                flush=True,
                            )

            print()

            # -------------------------------------------------------
            # Validate downloaded file size.
            # -------------------------------------------------------

            actual_size = part_path.stat().st_size

            if expected_size is not None:
                if actual_size != expected_size:
                    print(
                        f"  ERROR: Size mismatch."
                    )
                    print(
                        f"    Expected: {format_bytes(expected_size)}"
                    )
                    print(
                        f"    Received: {format_bytes(actual_size)}"
                    )

                    part_path.unlink(missing_ok=True)
                    continue

            if total_size is not None and actual_size != total_size:
                print(
                    f"  ERROR: Server Content-Length mismatch."
                )
                print(
                    f"    Expected: {format_bytes(total_size)}"
                )
                print(
                    f"    Received: {format_bytes(actual_size)}"
                )

                part_path.unlink(missing_ok=True)
                continue

            # -------------------------------------------------------
            # Only rename after successful validation.
            # -------------------------------------------------------

            part_path.replace(destination)

            print(
                f"  SUCCESS: {format_bytes(actual_size)}"
            )

            return True

        except requests.RequestException as e:

            print()
            print(f"  Download error: {e}")

            if part_path.exists():
                part_path.unlink()

            if attempt < MAX_RETRIES:
                wait_seconds = attempt * 5

                print(
                    f"  Retrying in {wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)

        except OSError as e:

            print()
            print(f"  File error: {e}")

            if part_path.exists():
                part_path.unlink()

            if attempt < MAX_RETRIES:
                wait_seconds = attempt * 5

                print(
                    f"  Retrying in {wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)

    print()
    print("  FAILED after maximum retries.")

    return False


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():

    print("=" * 70)
    print("Upper Manistee DEM Downloader")
    print("=" * 70)

    print()
    print(f"Manifest:")
    print(f"  {MANIFEST_PATH}")

    print()
    print(f"Download directory:")
    print(f"  {DOWNLOAD_DIR}")

    rows = load_manifest()

    print()
    print(f"Tiles in manifest: {len(rows)}")

    DOWNLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------------
    # Check existing files first.
    # ---------------------------------------------------------------

    remaining = []

    skipped = 0

    for row in rows:

        filename = get_filename(row)
        destination = DOWNLOAD_DIR / filename

        expected_size = get_expected_size(row)

        if destination.exists():

            actual_size = destination.stat().st_size

            if (
                expected_size is not None
                and actual_size == expected_size
            ):
                print(
                    f"Already downloaded: "
                    f"{filename} "
                    f"({format_bytes(actual_size)})"
                )

                skipped += 1
                continue

            elif expected_size is None:
                print(
                    f"File exists but manifest has no size: "
                    f"{filename}"
                )

                print("  Will verify by re-downloading.")

        remaining.append(row)

    print()
    print("=" * 70)
    print(f"Already complete: {skipped}")
    print(f"Remaining:        {len(remaining)}")
    print("=" * 70)

    if not remaining:
        print()
        print("All DEM tiles are already downloaded and verified.")
        return

    # ---------------------------------------------------------------
    # Download remaining tiles.
    # ---------------------------------------------------------------

    successful = 0
    failed = 0

    start_time = time.time()

    for index, row in enumerate(remaining, start=1):

        filename = get_filename(row)
        url = get_url(row)
        expected_size = get_expected_size(row)

        destination = DOWNLOAD_DIR / filename

        print()
        print("#" * 70)
        print(
            f"Tile {index} of {len(remaining)}"
        )
        print("#" * 70)

        print(f"Filename: {filename}")

        if expected_size:
            print(
                f"Expected size: "
                f"{format_bytes(expected_size)}"
            )

        print(f"URL: {url}")

        success = download_file(
            url=url,
            destination=destination,
            expected_size=expected_size,
        )

        if success:
            successful += 1
        else:
            failed += 1

            print()
            print(
                "WARNING: This tile failed."
            )
            print(
                "The script will continue with the remaining tiles."
            )

    # ---------------------------------------------------------------
    # Final summary.
    # ---------------------------------------------------------------

    elapsed = time.time() - start_time

    print()
    print()
    print("=" * 70)
    print("DOWNLOAD SUMMARY")
    print("=" * 70)

    print(f"Manifest tiles:    {len(rows)}")
    print(f"Already complete:  {skipped}")
    print(f"Downloaded:        {successful}")
    print(f"Failed:            {failed}")

    print(
        f"Elapsed time:      {elapsed / 60:.1f} minutes"
    )

    # Calculate current disk usage.
    total_bytes = 0
    file_count = 0

    for path in DOWNLOAD_DIR.glob("*.tif"):

        total_bytes += path.stat().st_size
        file_count += 1

    print()
    print(
        f"DEM files on disk: {file_count}"
    )

    print(
        f"DEM disk usage:    {format_bytes(total_bytes)}"
    )

    print("=" * 70)

    if failed:
        print()
        print(
            "Some downloads failed."
        )
        print(
            "Run this script again to retry the failed tiles."
        )
    else:
        print()
        print(
            "All DEM downloads completed successfully."
        )


if __name__ == "__main__":
    main()