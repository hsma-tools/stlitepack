# stlitepack

[<img src="https://img.shields.io/pypi/v/stlitepack?label=pypi%20package">](https://pypi.org/project/stlitepack/)

stlitepack is a Python utility that helps you turn your existing Streamlit apps into [stlite apps — lightweight, browser-only Streamlit apps that run entirely in the client without a server](https://github.com/whitphx/stlite).

With stlitepack, you can:

- 📦 Pack your Streamlit app into a stlite-ready format
- 🗂️ Include additional resources like config.toml
- 🚀 Generate GitHub Actions workflows to (almost) auto-deploy your app to GitHub Pages

## 📦 Installation

```bash
pip install stlitepack
```

## 🚀 Usage

```python
from stlitepack import pack

# Pack your Streamlit app (e.g., "app.py") into a stlite bundle
pack("app.py")
```

This will create an `index.html` file with all of the required stlite additions, which you can then serve as a static file using a hosting platform such as github pages.

## Documentation

Check out the quickstart guide at [sammirosser.com/stlitepack/stlitepack_docs/stlitepack_quickstart](http://sammirosser.com/stlitepack/stlitepack_docs/stlitepack_quickstart).

You can also find the full reference for each function at [sammirosser.com/stlitepack/reference/](http://sammirosser.com/stlitepack/reference/).

## 🔮 Roadmap

- ✅ v0.1: Single-page app packing
- ✅ v0.2: Helper functions for GitHub Pages auto-deploy (via GitHub Actions workflow generation)
- ✅ v0.3: Multi-page app support (for [`pages/` subfolder](https://webapps.hsma.co.uk/multipage.html#method-2-pages-subfolder) method) and simple additional file inclusion
- v0.4: Better support for resource bundling (images, CSVs, assets, config files etc.) of local or web-based files
- v0.5: Better multi-page app support (for [`st.navigation()`](https://webapps.hsma.co.uk/multipage.html#method-1-st.page-and-st.navigation) method)
- v0.6: Auto-handling of stlite-specific required changes (e.g. asyncio vs sleep)
- v0.7: Add support for generating the required package.json for [desktop app bundling](https://github.com/whitphx/stlite/tree/main/packages/desktop)
- v0.8: Add helpers for generating files for additional deployment options e.g. Docker, Caddy, Nginx, Apache
- v0.9: TOML or YAML file support as optional alternative to the packing function
- v1.0: Full toolkit for packaging, deploying, and managing stlite apps

## 🤝 Contributing
Contributions, feature requests, and feedback are welcome!

Open an issue or submit a pull request to help improve stlitepack.

## 📜 License
Apache 2.0 License. See LICENSE for details.

## Acknowledgements

- [whitphx](https://github.com/whitphx) for creating the amazing [stlite](https://github.com/whitphx/stlite) framework!

## Generative AI Use Disclosure

This package was developed with the assistance of ChatGPT (OpenAI’s GPT-5 model) as a coding and documentation partner.
All code and design decisions were reviewed and finalized by a human, and ChatGPT’s output was used as a foundation rather than a final product.
