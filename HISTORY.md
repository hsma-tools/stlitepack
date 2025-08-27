# Version History

All notable changes to `stlitepack` are documented in this file.

Please note that prior to version 1.0, breaking API changes may occur at any time. The API should
not be considered stable until the 1.0 release. After the version 1 release, all breaking changes will
only occur on major version increments (e.g. version 1 --> version 2).

During the pre v1 phase, all breaking changes will be clearly highlighted in the release notes below.

## [0.4.3]

### Improved

- Changed default stlite version to [0.80.5](https://github.com/whitphx/stlite/releases/tag/v0.80.5) as this was observed to work particularly well in testing. This version was release in March 2024.
- Improved docstrings for embedding vs linking.

## [0.4.2]

### Added

- Automatic creation of a 404 redirect page when publishing, with either 'relative' option, or option to pass an absolute URL to redirect to.

### Improved

- [BREAKING] Some publish steps now rely on passing the relative or absolute path to the root of the repository instead of a less clear 'output_dir' parameter.
- Ports for preview server now default to a random free port in the range 8000-8999. A fixed port can still be set if preferred.
- Linting of key files with ruff
- Changed how directories are handled by the preview server so that change of directories doesn't persist for subsequent steps in packing script

## [0.4.1]

### Fixes

- Fix bug where indendation level of subsequent code may be incorrect when async fixes are applied to spinner usage
- Prevent directory change for preview server if just putting the folder in docs (smarter handling of this planned in the future!)

### Added

- Added option to toggle automatic stlite fixes (like adding async await to spinner) on and off with `automated_stlite_fixes` parameter in pack.

## [0.4.0]

### BREAKING CHANGES

- `extra_files` parameter split to `extra_files_to_embed` and `extra_files_to_link`
- added `prepend_github_path` parameter to allow users to quickly point to hosted files
- added `list_files_in_folders` helper for quick gathering of files meeting criteria to either link or embed
- `use_raw_api` default changed from `False` to `True`.
    - Too many features are not available within the simplified (non-mount) API. Therefore, swiching
    to the mount API as default ensures other parameters will work as expected. Turning this to
    'False' should now be considered a step for advanced users only.

### Added

- Added automatic fix to ensure st.spinner gets displayed and the code running within the block does not block all execution
    - This is achieved by automatically inserting an `await async.sleep(1) block in the relevant part of the code
- Add fix for material icon display
    - This is achieved via embedding of material icon font. Bonus feature - you can select your preferred material font style.
- Add ability to automatically start a preview server after packing the app
- Add more flexibility in where the output files will go (better at handling cases where app is contained within e.g. app subfolder of repo)


## [0.3.1]

### Fixed
- Added missing dependency to build file (requests)

### Documentation
- Quickstart guide in `.qmd` format, including detailed parameters for `pack()` and `publish()`.
- Added description of `stlite`, benefits of `stlitepack`, and Pyodide vs traditional server apps.
- Created contributor `CODE_OF_CONDUCT.md`.

## [0.3.0]

### Fixed
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
