import json
from pathlib import Path

TEMPLATE = """<!DOCTYPE html>
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
        requirements,
        title: str = "App",
        output_dir: str = "docs",
        stylesheet_version: str = "0.77.0",
        js_bundle_version: str = "0.76.0"
        ):
    """
    Pack a single-page Streamlit app into a stlite-compatible index.html file.

    This function reads a Streamlit Python script, injects it into an HTML
    template compatible with stlite, and writes the output as ``index.html``.
    The resulting HTML can be served as static content (e.g., via GitHub Pages).

    Parameters
    ----------
    app_file : str
        Path to the Streamlit application file (e.g., ``"app.py"``).
    requirements : str or list of str
        Either:
          - Path to a ``requirements.txt`` file (str), or
          - A list of required Python packages (list of str).
    title : str, optional
        Title to insert into the HTML ``<title>`` tag. Default is ``"stlite app"``.
    output_dir : str, optional
        Directory where the generated ``index.html`` will be written.
        Default is ``"dist"``.

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

    # Read app code
    code = Path(app_file).read_text(encoding="utf-8")

    # Normalize requirements
    if isinstance(requirements, str) and requirements.endswith(".txt"):
        reqs = Path(requirements).read_text(encoding="utf-8").splitlines()
        reqs = [r.strip() for r in reqs if r.strip()]
    elif isinstance(requirements, list):
        reqs = requirements
    else:
        raise ValueError("requirements must be a list or a path to requirements.txt")

    # Fill template
    html = TEMPLATE.format(
        title=title,
        entrypoint=app_path.name,
        requirements=json.dumps(reqs),
        code=code,
        stylesheet_version=stylesheet_version,
        js_bundle_version=js_bundle_version
    )

    # Write to output dir
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "index.html"
    outfile.write_text(html, encoding="utf-8")

    print(f"Packed app written to {outfile}")
