# stlitepack

stlitepack is a Python utility that helps you turn your existing Streamlit apps into [stlite apps — lightweight, browser-only Streamlit apps that run entirely in the client without a server](https://github.com/whitphx/stlite).

With stlitepack, you can:

- 📦 Pack your Streamlit app into a stlite-ready format (current functionality).
- 🚀 (Upcoming) Generate GitHub Actions workflows to auto-deploy your app to GitHub Pages.
- 🗂️ (Planned) Add support for multi-page apps, external resources, and more.

## 📦 Installation

```bash
pip install stlitepack
```

## 🚀 Usage

```python
from stlitepack import pack

# Pack your Streamlit app (e.g., "app.py") into a stlite bundle
pack("app.py", output_dir="docs")
```

This will create a docs/ folder containing your stlite-ready app files, which you can serve as static files.

## 🔮 Roadmap

- v0.1: Single-page app packing via function
- v0.2: GitHub Pages auto-deploy (via GitHub Actions workflow generation)
- v0.3: TOML or YAML file support as optional alternative to the packing function
- v0.4: Multi-page app support
- v0.5: Resource bundling (images, CSVs, assets, etc.)
- v0.6: Auto-handling of stlite-specific features (e.g. asyncio vs sleep)
- v1.0: Full toolkit for packaging, deploying, and managing stlite apps

## 🤝 Contributing
Contributions, feature requests, and feedback are welcome!
Open an issue or submit a pull request to help improve stlitepack.

## 📜 License
Apache 2.0 License. See LICENSE for details.

## Acknowledgements

- [whitphx](https://github.com/whitphx) for creating the amazing [stlite](https://github.com/whitphx/stlite) framework!
