# Makefile for django-suit5 package management
#
# Usage:
#   make version           - Show current version
#   make bump-patch        - Bump patch version (0.2.28 -> 0.2.29)
#   make bump-minor        - Bump minor version (0.2.28 -> 0.3.0)
#   make bump-major        - Bump major version (0.2.28 -> 1.0.0)
#   make build             - Build the package
#   make publish           - Build and publish to PyPI
#   make publish-test      - Build and publish to TestPyPI
#   make release-patch     - Bump patch, commit, tag, and publish
#   make release-minor     - Bump minor, commit, tag, and publish
#   make release-major     - Bump major, commit, tag, and publish

.PHONY: version bump-patch bump-minor bump-major build clean publish publish-test release-patch release-minor release-major help

help:
	@echo "django-suit5 Package Management"
	@echo ""
	@echo "Version commands:"
	@echo "  make version        - Show current version"
	@echo "  make bump-patch     - Bump patch version (x.y.z -> x.y.z+1)"
	@echo "  make bump-minor     - Bump minor version (x.y.z -> x.y+1.0)"
	@echo "  make bump-major     - Bump major version (x.y.z -> x+1.0.0)"
	@echo ""
	@echo "Build commands:"
	@echo "  make build          - Build the package"
	@echo "  make clean          - Remove build artifacts"
	@echo ""
	@echo "Publish commands:"
	@echo "  make publish        - Build and publish to PyPI"
	@echo "  make publish-test   - Build and publish to TestPyPI"
	@echo ""
	@echo "Release commands (bump + commit + tag + publish):"
	@echo "  make release-patch  - Release a patch version"
	@echo "  make release-minor  - Release a minor version"
	@echo "  make release-major  - Release a major version"

version:
	@python scripts/bump_version.py --show

bump-patch:
	@python scripts/bump_version.py patch

bump-minor:
	@python scripts/bump_version.py minor

bump-major:
	@python scripts/bump_version.py major

clean:
	rm -rf dist/ build/ *.egg-info suit5.egg-info/

build: clean
	python -m build

publish:
	./scripts/publish.sh

publish-test:
	./scripts/publish.sh --test

release-patch:
	@echo "Releasing patch version..."
	@python scripts/bump_version.py patch
	@VERSION=$$(python scripts/bump_version.py --show) && \
		git add suit5/__init__.py && \
		git commit -m "Bump version to $$VERSION" && \
		git tag -a "v$$VERSION" -m "Release v$$VERSION" && \
		echo "Version $$VERSION committed and tagged." && \
		echo "Run 'git push && git push --tags && make publish' to complete the release."

release-minor:
	@echo "Releasing minor version..."
	@python scripts/bump_version.py minor
	@VERSION=$$(python scripts/bump_version.py --show) && \
		git add suit5/__init__.py && \
		git commit -m "Bump version to $$VERSION" && \
		git tag -a "v$$VERSION" -m "Release v$$VERSION" && \
		echo "Version $$VERSION committed and tagged." && \
		echo "Run 'git push && git push --tags && make publish' to complete the release."

release-major:
	@echo "Releasing major version..."
	@python scripts/bump_version.py major
	@VERSION=$$(python scripts/bump_version.py --show) && \
		git add suit5/__init__.py && \
		git commit -m "Bump version to $$VERSION" && \
		git tag -a "v$$VERSION" -m "Release v$$VERSION" && \
		echo "Version $$VERSION committed and tagged." && \
		echo "Run 'git push && git push --tags && make publish' to complete the release."
