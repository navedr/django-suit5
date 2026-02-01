#!/bin/bash
#
# Publish django-suit5 to PyPI
#
# Usage:
#   ./scripts/publish.sh              # Bump patch version and publish to PyPI
#   ./scripts/publish.sh --minor      # Bump minor version and publish
#   ./scripts/publish.sh --major      # Bump major version and publish
#   ./scripts/publish.sh --test       # Publish to TestPyPI
#   ./scripts/publish.sh --dry-run    # Build only, don't upload
#
# Prerequisites:
#   pip install build twine
#
# Authentication:
#   Set TWINE_USERNAME and TWINE_PASSWORD environment variables, or
#   configure ~/.pypirc, or use a PyPI API token.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Parse arguments
TEST_PYPI=false
DRY_RUN=false
BUMP_TYPE=patch

for arg in "$@"; do
    case $arg in
        --test)
            TEST_PYPI=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --patch)
            BUMP_TYPE=patch
            shift
            ;;
        --minor)
            BUMP_TYPE=minor
            shift
            ;;
        --major)
            BUMP_TYPE=major
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --patch     Bump patch version (default): 0.2.29 -> 0.2.30"
            echo "  --minor     Bump minor version: 0.2.29 -> 0.3.0"
            echo "  --major     Bump major version: 0.2.29 -> 1.0.0"
            echo "  --test      Upload to TestPyPI instead of PyPI"
            echo "  --dry-run   Build only, don't upload"
            echo "  --help      Show this help message"
            exit 0
            ;;
    esac
done

# Bump version
echo "Bumping $BUMP_TYPE version..."
python scripts/bump_version.py $BUMP_TYPE

# Get new version
VERSION=$(python scripts/bump_version.py --show)
echo "Publishing django-suit5 version $VERSION"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info suit5.egg-info/ django_suit5.egg-info/ django-suit5.egg-info/

# Build the package
echo "Building package..."
python -m build

# List built files
echo ""
echo "Built packages:"
ls -la dist/

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "Dry run complete. Packages built but not uploaded."
    exit 0
fi

# Upload to PyPI
echo ""
if [ "$TEST_PYPI" = true ]; then
    echo "Uploading to TestPyPI..."
    python -m twine upload --repository testpypi dist/*
    echo ""
    echo "Package uploaded to TestPyPI!"
    echo "Install with: pip install --index-url https://test.pypi.org/simple/ django-suit5==$VERSION"
else
    echo "Uploading to PyPI..."
    python -m twine upload dist/*
    echo ""
    echo "Package uploaded to PyPI!"
    echo "Install with: pip install django-suit5==$VERSION"
fi
