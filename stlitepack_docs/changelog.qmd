# Version History

# HISTORY

All notable changes to `stlitepack` are documented in this file.

## [0.4.0]

### BREAKING CHANGES

- `extra_files` parameter split to `extra_files_to_embed` and `extra_files_to_link`
- `use_raw_api` default changed from `False` to `True`.

## Added

- Added 'find_

## [0.3.1]

### Fixed
- Added missing dependency to build file (requests)

### Documentation
- Quickstart guide in `.qmd` format, including detailed parameters for `pack()` and `publish()`.
- Added description of `stlite`, benefits of `stlitepack`, and Pyodide vs traditional server apps.
- Created contributor `CODE_OF_CONDUCT.md`.

## [0.3.0]

## Fixed
- GitHub Pages `setup_github_pages` documentation corrected.

## [0.2.0]

### Added
- Support for `raw` API with multipage apps.
- Conditional configuration and `extra_files` mounting.
- Support for relative paths in app file mounting.
- Function to fetch valid Stlite versions from GitHub.
- Terminal-friendly messages for version info.
- Warning if `pyodide_version` is set while using the raw API.

### Changed
- `pack()` function now accepts `app_file` as main entrypoint and maintains relative path handling.
- `publish()` / GitHub Pages workflow documentation clarified.
- Raw API template updated to support `streamlitConfig` and multipage apps.
- Version checks added for `stylesheet_version` and `js_bundle_version` (must be >= 0.76.0).

### Fixed
- Path handling in the raw API HTML template to work across OSes (forward slashes normalized).


## [0.1.0] - Initial release
- Basic `pack()` function for packaging Streamlit apps to Stlite.
- GitHub Pages deployment support with `setup_github_pages()`.
- Raw API HTML template for single-file apps.
