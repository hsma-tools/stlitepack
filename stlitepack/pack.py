import json
from pathlib import Path
from packaging import version
import requests
import warnings
import re
import os
import base64
import fnmatch

TEMPLATE = """<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <title>{title}</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@stlite/browser@{stylesheet_version}/build/stlite.css"
    />
    <script
      type="module"
      src="https://cdn.jsdelivr.net/npm/@stlite/browser@{js_bundle_version}/build/stlite.js"
    ></script>
  </head>
  <body>
    <streamlit-app>
{app_files}
{requirements}
    </streamlit-app>
  </body>
</html>
"""


TEMPLATE_MOUNT = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>{title}</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@stlite/browser@{stylesheet_version}/build/style.css"
    />
  </head>
  <body>
    <div id="root"></div>
    <script type="module">
      import {{ mount }} from "https://cdn.jsdelivr.net/npm/@stlite/browser@{js_bundle_version}/build/stlite.js";
      mount(
        {{
          {pyodide_version}
          requirements: {requirements},
          entrypoint: "{entrypoint}",
          files: {{
{files}
          }},
        }},
        document.getElementById("root")
      );
    </script>
  </body>
</html>"""

def _read_file_flexibly(path: Path):
  try:
      # Try reading as UTF-8 text
      return path.read_text(encoding="utf-8")
  except UnicodeDecodeError:
      # Fallback: read as bytes and encode as base64
      binary_content = path.read_bytes()
      return base64.b64encode(binary_content).decode("utf-8")

def pack(
        app_file: str,
        extra_files_to_embed: list[str] | None = None,
        extra_files_to_link: list[str] | dict | None = None,
        prepend_github_path: str | None = None,
        github_branch: str = "main",
        requirements: list[str] | None = None,
        title: str = "App",
        output_dir: str = "docs",
        output_file: str = "index.html",
        stylesheet_version: str = "0.84.1",
        js_bundle_version: str = "0.84.1",
        use_raw_api: bool = True,
        pyodide_version: str = "default",
        # patch_session_state: bool = True
        ):
    """
    Pack a Streamlit app into a stlite-compatible index.html file.

    This function reads a Streamlit Python script, injects it into an HTML
    template compatible with stlite, and writes the output as ``index.html``.
    The resulting HTML can be served as static content (e.g., via GitHub Pages).

    If additional pages are found in a 'pages' folder at the same level as the main app file,
    these will be added in as additional files.

    Parameters
    ----------
    app_file : str
        Path to the main Streamlit application file (entrypoint) (e.g., ``"app.py"``).
        If additional pages are found in a 'pages' folder at the same level as this main app file,
        these will be added in as additional files.
    extra_files_to_embed : list[str], optional
        Additional files to mount directly into the app (e.g. .streamlit/config.toml).
        These must be additional files that are primarily text-based (e.g. .py, .toml, .csv).
        If binary files are provided,
    extra_files_to_link : list[str] or dict, optional
        Additional files to hyperlink to.
        - If passed as a list, must be used with the argument 'prepend_github_path'.
          The list must be a list of relative filepaths.
        - If passed as a dict, expects key:value pairs of relative_filepath: url
        Can only be used with the raw API (use_raw_api=True).
        Defaults to None
    prepend_github_path : str, optional
        If files to be linked are stored on github, you can pass them as relative paths in the
        extra_files_to
        Needs to passed in the format username/reponam
        Ignored if 'extra_files_to_link' is None.
        Can only be used with the raw API (use_raw_api=True).
        Defaults to None
    github_branch: str, optional
        If files to be linked to on Github need to come from a branch other than main, provide
        the name of the desired branch here.
        Ignored if 'extra_files_to_link' is None or prepend_github_path is None.
        Can only be used with the raw API (use_raw_api=True).
        Defaults to 'main'
    requirements : str or list of str
        Either:
          - Path to a ``requirements.txt`` file (str), or
          - A list of required Python packages (list of str).
    title : str, optional
        Title to insert into the HTML ``<title>`` tag. Default is ``"stlite app"``.
    output_dir : str, optional
        Directory where the generated ``index.html`` will be written.
        Default is ``"dist"``.
    use_raw_api : bool, optional
        If True, will use the version of the template that calls the `mount()` API explicitly.
        Default is `True`.
    pyodide_version: str, optional
        If not 'default', tries to serve the requested pyodide version from the pyodide CDN.
        Only works with raw API.
        Versions can be found here: https://pyodide.org/en/stable/project/changelog.html
        Default is 'default' (use default pyodide version, which is linked to stlite version)
    patch_session_state: bool, optional
        Attempts to mimic streamlit's session state via a workaround.
        Will automatically include the workaround code and inject the required import at the start
        of the entrypoint file.
        Limitation is that this form of session state will only work with serializable objects.
        Default is `True`

    Raises
    ------
    FileNotFoundError
        If the specified app_file does not exist.
    ValueError
        If ``requirements`` is not a list or a valid requirements file path.

    Notes
    -----
    - Currently supports only single-page Streamlit apps.
    - Future versions will support multi-page apps, additional resources,
      and GitHub Pages deployment automation.

    Examples
    --------
    Pack an app using a requirements file:

    >>> from stlitepack import pack
    >>> pack("app.py", requirements="requirements.txt", title="My App")

    Pack an app with inline requirements:

    >>> pack("app.py", requirements=["pandas", "numpy"], title="Data Explorer")

    The resulting HTML file will be written to ``dist/index.html`` by default.
    """
    # --- Version check ---
    min_version = version.parse("0.76.0")
    for v_name, v_str in [("stylesheet_version", stylesheet_version),
                          ("js_bundle_version", js_bundle_version)]:
        if version.parse(v_str) < min_version:
            raise ValueError(f"{v_name} must be >= 0.76.0, got {v_str}")

    app_path = Path(app_file)
    if not app_path.exists():
        raise FileNotFoundError(f"App file not found: {app_file}")

    base_dir = app_path.parent

    # Gather files: entrypoint first, then optional pages/*
    files_to_pack = [app_path]
    pages_dir = base_dir / "pages"
    if pages_dir.is_dir():
        files_to_pack.extend(sorted(pages_dir.glob("*.py")))

    # Add extra files explicitly
    if extra_files_to_embed:
        files_to_pack.extend(Path(f) for f in extra_files_to_embed)

    # Normalize requirements
    if requirements is None:
        req_list = []
    elif isinstance(requirements, str):
        with open(requirements) as f:
            req_list = [
                line.split("#", 1)[0].strip()
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
    else:
        req_list = requirements

    # Build for raw API
    if use_raw_api:
        file_entries = []
        # Pack main files
        for f in files_to_pack:
            rel_name = f.relative_to(base_dir).as_posix()
            content = _read_file_flexibly(f)
            file_entries.append(
                f'"{rel_name}": `\n{content}\n            `'
            )

        # NOTE - Here will add in the step of including any additional linked files
        # where instead of embedding the code
        if isinstance(extra_files_to_link, dict):
            for k, v in extra_files_to_link.items():
                file_entries.append(
                    f'"{k}": {{\nurl: "{v}"\n}}'
                )
        elif isinstance(extra_files_to_link, list) and prepend_github_path is not None:
            for f in extra_files_to_link:
                file_entries.append(
                    f'"{f}": {{\nurl: "https://raw.githubusercontent.com/{prepend_github_path}/refs/heads/{github_branch}/{f}"\n}}'
                )
        elif isinstance(extra_files_to_link, list) and prepend_github_path is None:
            warnings.warn(
                  "pyodide_version is ignored when use_raw_api=False. "
                  "The simple API uses Pyodide version linked to the chosen stlite release.",
                  UserWarning
                )

        # Finalise the string of additional files
        files_js = ",\n".join(file_entries)

        if pyodide_version != "default":
            if not use_raw_api:
                warnings.warn(
                  "pyodide_version is ignored when use_raw_api=False. "
                  "The simple API uses Pyodide version linked to the chosen stlite release.",
                  UserWarning
                )
                pyodide_version_string = ""
            else:
                pyodide_version_string = f'pyodideUrl: "https://cdn.jsdelivr.net/pyodide/v{pyodide_version}/full/pyodide.js",'
        else:
            pyodide_version_string = ""

        html = TEMPLATE_MOUNT.format(
            title=title,
            stylesheet_version=stylesheet_version,
            js_bundle_version=js_bundle_version,
            requirements=json.dumps(req_list),
            entrypoint=app_path.relative_to(base_dir).as_posix(),
            files=files_js,
            pyodide_version=pyodide_version_string
        )

    # Build for <streamlit-app> template
    else:
        # Build <app-file> blocks
        app_file_blocks = []
        for f in files_to_pack:
            code = f.read_text(encoding="utf-8")
            rel_name = f.relative_to(base_dir).as_posix()
            entry_attr = " entrypoint" if f == app_path else ""
            app_file_blocks.append(
                f'  <app-file name="{rel_name}"{entry_attr}>\n'
                + "\n".join("    " + line for line in code.splitlines())
                + "\n  </app-file>"
            )
        app_files_section = "\n".join(app_file_blocks)

        # Requirements block
        if req_list:
            reqs = "<app-requirements>\n" + "\n".join(req_list) + "\n</app-requirements>"
        else:
            reqs = ""

        html = TEMPLATE.format(
            title=title,
            app_files=app_files_section,
            requirements=reqs,
            stylesheet_version=stylesheet_version,
            js_bundle_version=js_bundle_version,
        )

    # Write to output dir
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / output_file
    outfile.write_text(html, encoding="utf-8")

    print(f"Packed app written to {outfile}")

def get_stlite_versions():
    """
    Fetch the list of released Stlite versions from GitHub and print a nicely formatted message.

    Returns
    -------
    list[str]
        A list of version strings (e.g., ["0.84.1", "0.84.0", ...]).

    Raises
    ------
    RuntimeError
        If the GitHub API request fails.
    """
    url = "https://api.github.com/repos/whitphx/stlite/releases"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch Stlite releases: HTTP {resp.status_code}")

    releases = resp.json()
    versions = [r["tag_name"].lstrip("v") for r in releases]

    if not versions:
        print("No versions found on GitHub.")
        return []

    newest = versions[0]
    other_versions = versions[1:]

    # Terminal-friendly formatting
    print("\n=== Stlite Versions ===")
    print(f"Newest release: {newest}\n")

    if other_versions:
        print("Other valid releases:")
        # print in columns of 5
        for i in range(0, len(other_versions), 5):
            print("  " + ", ".join(other_versions[i:i+5]))
    print("=======================\n")

    return versions

def list_files_in_folders(folders, recursive=False, pattern=None, invert=False):
    """
    Given a list of folder paths, return a list of all files inside them
    with their relative paths (including the folder name).

    Parameters
    ----------
    folders : list of str
        List of folder paths to search in.
    recursive : bool, default=False
        If True, include files in subfolders recursively.
    pattern : str, optional
        A glob pattern (e.g., "*.csv") or regex to filter file paths.
        If None, all files are included.
    invert : bool, default=False
        If True, include all files *except* those that match the pattern.
    """
    all_files = []

    # Convert glob to regex if needed
    if pattern:
        # Simple heuristic: treat pattern as glob if it contains *, ?, or []
        if any(char in pattern for char in "*?[]"):
            regex = re.compile(fnmatch.translate(pattern))
        else:
            regex = re.compile(pattern)
    else:
        regex = None

    for folder in folders:
        folder = os.path.abspath(folder)  # normalize path
        if recursive:
            for root, _, files in os.walk(folder):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), start=os.path.dirname(folder))
                    rel_path = rel_path.replace(os.sep, "/")
                    if regex:
                        match = bool(regex.search(rel_path))
                        if match != invert:
                            all_files.append(rel_path)
                    else:
                        all_files.append(rel_path)
        else:
            for file in os.listdir(folder):
                full_path = os.path.join(folder, file)
                if os.path.isfile(full_path):
                    rel_path = os.path.relpath(full_path, start=os.path.dirname(folder))
                    rel_path = rel_path.replace(os.sep, "/")
                    if regex:
                        match = bool(regex.search(rel_path))
                        if match != invert:
                            all_files.append(rel_path)
                    else:
                        all_files.append(rel_path)

    return all_files
