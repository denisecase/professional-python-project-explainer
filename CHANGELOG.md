# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.1.0] - 2026-10-10

### Added

- initial versioned release

### Changed

- changed from `.pre-commit-config.yaml` to `prek.toml`
- professional python update with `uvx pup-up@latest`.
- added project `docs` and `zensical.toml`

---

## Notes on Versioning and Releases

- We use **SemVer**:
  - **MAJOR** - breaking changes
  - **MINOR** - backward-compatible
  - **PATCH** - fixes, documentation, tooling
- Versions are driven by git tags.
- Tag `vX.Y.Z` to release.

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. `CITATION.cff` - update `version` and `date-released`
1.2. `pyproject.toml` - update `version`
1.3. CHANGELOG.md: add section, move unreleased entries, update links

### Task 2. Validate

```shell
.\sit.ps1

# Update GitHub Actions and pin all action references to immutable SHAs
uvx gha-tools autoupdate --pin=all --write .github/workflows

# Then audit the resulting GitHub configuration for security findings
uvx zizmor@latest .github/

# Run checks
uvx cffconvert --validate
npx markdownlint-cli2 --fix

# Generate the Marimo application inside the Zensical source tree
uv run marimo export html-wasm src/app.py -o docs/app --mode run

# Verify the exported application
Test-Path docs/app/index.html
Test-Path docs/app/public/data.toml

# Build the complete website
uv run python -m zensical build

# Verify both entry points
Test-Path site/index.html
Test-Path site/app/index.html
```

### Task 4. Commit, push, tag

```shell
git add -A
git commit -m "Prepare X.Y.Z"
git push -u origin main
```

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/denisecase/professional-python-project-explainer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/denisecase/professional-python-project-explainer/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->
