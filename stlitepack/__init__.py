"""
stlitepack: Package Streamlit apps into stlite-ready bundles.

stlitepack helps you convert existing Streamlit applications into
self-contained stlite bundles that can run entirely in the browser
(without a server). The primary use case is packaging single-page
Streamlit apps into static HTML files suitable for deployment
on GitHub Pages or other static hosting services.

Main Features
-------------
- Pack a single-page Streamlit app into an ``index.html``.
- Embed app code and requirements directly into the stlite runtime.
- Output ready-to-deploy static bundles.

Planned Features
----------------
- Multi-page app support.
- Inclusion of additional resources (images, datasets, CSS).
- Automated GitHub Pages deployment via GitHub Actions.

Usage Example
-------------
>>> from stlitepack import pack
>>> pack("app.py", requirements="requirements.txt", title="My App")

The generated app will be available at ``docs/index.html`` by default.
"""

__version__ = "0.4.4"
__author__ = "Sammi Rosser"

from . import pack as _pack_module  # import the module itself
from .publish import setup_github_pages

# Expose the main function under a different name
pack = _pack_module.pack  # now `stlitepack.pack` refers to the function

__all__ = ["pack", "setup_github_pages"]
