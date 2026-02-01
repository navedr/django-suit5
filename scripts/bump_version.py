#!/usr/bin/env python3
"""
Version bump script for django-suit5.

Usage:
    python scripts/bump_version.py patch   # 0.2.28 -> 0.2.29
    python scripts/bump_version.py minor   # 0.2.28 -> 0.3.0
    python scripts/bump_version.py major   # 0.2.28 -> 1.0.0
    python scripts/bump_version.py --show  # Show current version
"""
import argparse
import re
import sys
from pathlib import Path
from typing import Tuple

VERSION_FILE = Path(__file__).parent.parent / "suit5" / "__init__.py"
VERSION_PATTERN = re.compile(r"^VERSION\s*=\s*['\"](\d+\.\d+\.\d+)['\"]", re.MULTILINE)


def get_current_version() -> str:
    """Read the current version from __init__.py."""
    content = VERSION_FILE.read_text()
    match = VERSION_PATTERN.search(content)
    if not match:
        raise ValueError(f"Could not find VERSION in {VERSION_FILE}")
    return match.group(1)


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse a version string into (major, minor, patch) tuple."""
    parts = version.split(".")
    return int(parts[0]), int(parts[1]), int(parts[2])


def bump_version(version: str, bump_type: str) -> str:
    """Bump the version according to the specified type."""
    major, minor, patch = parse_version(version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_version_file(new_version: str) -> None:
    """Update the version in __init__.py."""
    content = VERSION_FILE.read_text()
    new_content = VERSION_PATTERN.sub(f"VERSION = '{new_version}'", content)
    VERSION_FILE.write_text(new_content)


def main():
    parser = argparse.ArgumentParser(description="Bump the package version")
    parser.add_argument(
        "bump_type",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Type of version bump",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show current version without modifying",
    )
    parser.add_argument(
        "--set",
        metavar="VERSION",
        help="Set a specific version (e.g., --set 1.0.0)",
    )

    args = parser.parse_args()

    current_version = get_current_version()

    if args.show:
        print(current_version)
        return

    if args.set:
        # Validate the version format
        if not re.match(r"^\d+\.\d+\.\d+$", args.set):
            print(f"Error: Invalid version format '{args.set}'. Use X.Y.Z format.", file=sys.stderr)
            sys.exit(1)
        new_version = args.set
    elif args.bump_type:
        new_version = bump_version(current_version, args.bump_type)
    else:
        parser.print_help()
        sys.exit(1)

    update_version_file(new_version)
    print(f"Version bumped: {current_version} -> {new_version}")


if __name__ == "__main__":
    main()
