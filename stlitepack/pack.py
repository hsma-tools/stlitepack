import json
from pathlib import Path
from packaging import version
import requests

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

def pack(
        app_file: str,
        extra_files: list[str] | None = None,
        requirements: list[str] | None = None,
        title: str = "App",
        output_dir: str = "docs",
        output_file: str = "index.html",
        stylesheet_version: str = "0.84.1",
        js_bundle_version: str = "0.84.1",
        use_raw_api: bool = False,
        pyodide_version: str = "default"
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
    extra_files : list[str], optional
        Additional files to mount into the app (e.g. .streamlit/config.toml).
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
        Multi-page apps are not currently supported with the raw API, so set this to False if you
        wish to create a multi-page app.
        Default is `False`.

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
    for v_name, v_str in [("stylesheet_version", stylesheet_version), ("js_bundle_version", js_bundle_version)]:
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
    if extra_files:
        files_to_pack.extend(Path(f) for f in extra_files)

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
        for f in files_to_pack:
            rel_name = f.relative_to(base_dir).as_posix()
            code = f.read_text(encoding="utf-8")
            file_entries.append(
                f'            "{rel_name}": `\n{code}\n            `'
            )
        files_js = ",\n".join(file_entries)

        html = TEMPLATE_MOUNT.format(
            title=title,
            stylesheet_version=stylesheet_version,
            js_bundle_version=js_bundle_version,
            requirements=json.dumps(req_list),
            entrypoint=app_path.relative_to(base_dir).as_posix(),
            files=files_js,
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
    import requests

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
