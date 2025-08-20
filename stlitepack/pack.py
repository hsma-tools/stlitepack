import json
from pathlib import Path

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
      import * as stlite from "https://cdn.jsdelivr.net/npm/@stlite/browser@{js_bundle_version}/build/stlite.js";
      stlite.mount(
        {{
          requirements: {requirements},
          entrypoint: "{entrypoint}",
          files: {{
            "{entrypoint}": `
{code}
            `
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
        use_raw_api: bool = False
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

    # Build <app-file> blocks
    app_file_blocks = []
    for f in files_to_pack:
        if not f.exists():
            raise FileNotFoundError(f"Extra file not found: {f}")
        code = f.read_text(encoding="utf-8")
        rel_name = str(f.relative_to(base_dir).as_posix())
        entry_attr = " entrypoint" if f == app_path else ""
        app_file_blocks.append(
            f'  <app-file name="{rel_name}"{entry_attr}>\n'
            + "\n".join("    " + line for line in code.splitlines())
            + "\n  </app-file>"
        )

    app_files_section = "\n".join(app_file_blocks)

    # Normalize requirements
    if requirements is None:
        if use_raw_api:
            reqs = "[]"
        else:
            reqs = ""
    else:
        if isinstance(requirements, str):
            with open(requirements) as f:
                requirements = [line.split("#", 1)[0].strip() for line in f if line.strip() and not line.strip().startswith("#")]

        if use_raw_api:
            req_list = [f'"{req}"' for req in requirements]
            reqs = "[" + ", ".join(req_list) + "]"
        else:
            req_list = [f'{req}' for req in requirements]
            reqs = "<app-requirements>\n" + "\n".join(req_list) + "\n</app-requirements>"

    # Fill template
    if use_raw_api:
        html = TEMPLATE_MOUNT.format(
        title=title,
        entrypoint=app_path.name,
        requirements=reqs,
        code=code,
        stylesheet_version=stylesheet_version,
        js_bundle_version=js_bundle_version
    )

    else:
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
