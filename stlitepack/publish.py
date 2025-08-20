from pathlib import Path


def _create_nojekyll(output_dir: str = "."):
    """Create a .nojekyll file in the given directory."""
    out_path = Path(output_dir) / ".nojekyll"
    out_path.touch(exist_ok=True)
    return out_path


def _create_workflow(use_docs: bool = True,
                     only_on_index: bool = True,
                     print_only: bool = False,
                     branch: str = "main"):
    """Internal helper to create a gh-pages workflow file."""
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    target_dir = "docs" if use_docs else "."

    on_push = f"""
on:
  push:
    branches:
      - {branch}
"""
    if only_on_index:
        on_push += f"""    paths:
      - '{target_dir}/index.html'
"""

    workflow = f"""name: Deploy to GitHub Pages

{on_push}

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: {target_dir}

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    if print_only:
        print(workflow)
    else:
        workflow_path = workflow_dir / "deploy.yml"
        workflow_path.write_text(workflow)
        return workflow_path


def setup_github_pages(
    mode: str = "gh-actions",
    use_docs: bool = True,
    only_on_index: bool = True,
    branch: str = "main"
):
    """
Set up GitHub Pages deployment for a stlite app.

Parameters
----------
mode : {"gh-actions", "manual"}, optional
    Deployment mode.
    - "gh-actions": Deploys from a branch with GitHub Actions. Mostly hands-off, though note that
      you will still need to go to your repos settings --> pages --> Github Actions so that the
      generated workflow has permission to run.
    - "manual": Deploy directly from a branch - manual github pages settings required. This will
      still generate some additional required files, but you will need to follow the provided
      instructions to get the files to build.
use_docs : bool, optional
    If True, serve from the `docs/` folder. Otherwise serve from the repo root.
only_on_index : bool, optional
    If True, trigger deployment only when `index.html` changes (gh-actions mode only).
branch: str, optional
    Branch to use as source. Defaults to main.

Returns
-------
Path or None
    Path to created workflow file (gh-actions mode), or Path to helper instructions file (main mode).

    In both cases, a .nojekyll file will be created in the repo root and in the docs folder if it
    is present.

    In gh-actions model, a deploy.yml will be created in the .github/workflows folder, relative to
    the provided file. This folder will be created if it does not exist.
    """
    target_dir = "docs" if use_docs else "."
    # Create nojekyll file in both docs and target dir
    _create_nojekyll(".")

    if target_dir != ".":
        _create_nojekyll(target_dir)

    if mode == "manual":
        # no workflow, just helper message
        msg = f"""
[stlitepack] Manual deployment mode selected.

To complete setup:
1. Commit your `index.html` (and `.nojekyll`) into `{target_dir}/` on the `{branch}` branch.
2. Go to your repository **Settings -> Pages**.
3. Under "Build and deployment", set:
   - Source: **Deploy from a branch**
   - Branch: **{branch}**
   - Folder: **/{target_dir}**

No GitHub Actions workflow is required.
"""
        print(msg)
        helpfile = Path("PAGES_SETUP.md")
        helpfile.write_text(msg.strip() + "\n")
        return helpfile

    elif mode == "gh-actions":
        msg = f"""
[stlitepack] Github Pages Workflow mode selected.

To complete setup:
1. Go to your repository **Settings -> Pages**.
2. Under "Build and deployment", set:
  - Source: **Github Actions**
3. Commit the following files:
  - the deploy.yml file that has been created in .github/workflows
  - the `index.html` and `.nojekyll` files that have been created in {target_dir}
4. Visit your deployed app at https://your-github-username.github.io/your-repo-name/
  - note that it may take a few minutes for the app to finish deploying

            """
        print(msg)
        helpfile = Path("PAGES_SETUP.md")
        helpfile.write_text(msg.strip() + "\n")

        return _create_workflow(
            use_docs=use_docs,
            only_on_index=only_on_index,
            branch=branch
            )

    else:
        raise ValueError("mode must be 'gh-pages' or 'main'")
