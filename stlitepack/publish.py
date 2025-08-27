from pathlib import Path
import os
import traceback


def _create_nojekyll():
    """Create a .nojekyll file in the given directory."""
    out_path_root = Path(".nojekyll")
    out_path_root.touch(exist_ok=True)
    print(f".nojekyll file written to {out_path_root.resolve()}")
    return out_path_root


def _create_404(url):
    """Create a 404.html file in the given directory."""
    out_path = Path("404.html")
    content_404 = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0; URL={url}" />
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <title>Stlite App</title>
  </head>
  <body>
  <div id="root">
    <p> Redirecting you to the app </p>
  </div>
  </body>
</html>
    """
    out_path.write_text(content_404)
    print(f"404.html file written to {out_path.resolve()}")
    return out_path


def _create_workflow(
    use_docs: bool = True,
    only_on_index: bool = True,
    print_only: bool = False,
    branch: str = "main",
):
    """Internal helper to create a gh-pages workflow file."""

    # Determine where to put the workflow file
    workflow_dir = Path(".github/workflows")

    workflow_dir.mkdir(parents=True, exist_ok=True)
    target_dir = "docs" if use_docs else ""

    on_push = f"""
on:
  push:
    branches:
      - {branch}
"""
    if only_on_index:
        on_push += f"""    paths:
      - '{target_dir}{"/" if target_dir != "" else ""}index.html'
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
          path: {"docs" if use_docs else "."}

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    if print_only:
        print(workflow)
    else:
        workflow_path = workflow_dir / "deploy.yml"
        workflow_path.write_text(workflow)
        print(f"deploy.yml file written to {workflow_path.resolve()}")
        return workflow_path


def setup_github_pages(
    root_dir: str = "current_dir",
    use_docs: bool = True,
    mode: str = "gh-actions",
    create_nojekyll: bool = True,
    create_404: str = "relative",
    only_on_index: bool = True,
    branch: str = "main",
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
        If you have used the pack function previously to create your app file, match the option you
        used there.
        Defaults to `True` (which matches the pack function.)
    only_on_index : bool, optional
        If True, trigger deployment only when `index.html` changes.
        Ignored if mode = "manual"
        Defaults to `True`
    branch: str, optional
        Branch to use as source.
        Ignored if mode = "manual"
        Defaults to 'main'.
    root_dir: str, optional
        Determine whether to move to a different directory prior to creation of outputs.
        The function needs to know where the root (top-level) folder of your repository is in relation
        to the folder the script running the function is.
        Should only be needed if folder packing file is being run from is not the repository root
        (e.g. you have your app stored within an 'apps' folder).
        To move up one directory, pass ".."
        To move up two directories, pass "../.."
        And so on.
        Default is 'current_dir'.
    create_nojekyll: bool, optional
        Determines whether to create a .nojekyll file, which will prevent the deployed app from being
        run through post-processing steps on Github.
        Default is True.
    create_404: str, optional
        Determines whether to create a 404 file, which will ensure you are redirected in the case of
        a url path not being found. This is more common with stlite files as refreshing while on
        a subpage or trying to navigate directly to a subpage will cause an error.
        If "relative", the 404 will just try to navigate the user one level up, which should generally
        be correct unless they have arrived via a faulty URL.
        If "none", will not be created.
        If any other value, this will be treated as the absolute URL to redirect to.
        Default is "relative".

    Returns
    -------
    Path or None
        Path to created workflow file (gh-actions mode), or Path to helper instructions file (main mode).

        In both cases, a .nojekyll file will be created in the repo root and in the docs folder if it
        is present.

        In gh-actions model, a deploy.yml will be created in the .github/workflows folder, relative to
        the provided file. This folder will be created if it does not exist.
    """
    if root_dir == "current_dir":
        target_dir = "docs" if use_docs else "."
    else:
        target_dir = f"{root_dir}/docs" if use_docs else root_dir
        os.chdir(root_dir)
    # Create nojekyll file in both docs and target dir

    if create_nojekyll:
        try:
            _create_nojekyll()
        except Exception as e:  # narrowed to Exception
            print("Issues creating nojekyll file in root folder:")
            traceback.print_exc()

    if create_404 != "none":
        try:
            _create_404("." if create_404 == "relative" else create_404)
        except Exception as e:
            print("Issues creating 404 file in root folder:")
            traceback.print_exc()

    if mode == "manual":
        # no workflow, just helper message
        msg = f"""
[stlitepack] Manual deployment mode selected.

To complete setup:
1. Commit your `index.html` into `{target_dir}/` on the `{branch}` branch.
2. Commit `.nojekyll` and `404.html` into the root of your repository on the `{branch}` branch.
3. Go to your repository **Settings -> Pages**.
4. Under "Build and deployment", set:
   - Source: **Deploy from a branch**
   - Branch: **{branch}**
   - Folder: **/{target_dir}**

No GitHub Actions workflow is required.
"""
        print(msg)
        if root_dir == "current_dir":
            helpfile = Path("PAGES_SETUP.md")
        else:
            helpfile = Path(f"{root_dir}/PAGES_SETUP.md")
        helpfile.write_text(msg.strip() + "\n")
        return helpfile

    elif mode == "gh-actions":
        msg = """
[stlitepack] Github Pages Workflow mode selected.

To complete setup:
1. **BEFORE COMMITING THE NEWLY CREATED FILES**, Go to your repository **Settings -> Pages**.
2. Under "Build and deployment", set:
  - Source: **Github Actions**
3. **NOW** commit the following files:
  - the deploy.yml file that has been created in .github/workflows
  - the `index.html` and `.nojekyll` files that have been created in the root of your repository
4. Visit your deployed app at https://your-github-username.github.io/your-repo-name/
  - note that it may take a few minutes for the app to finish deploying

            """
        print(msg)
        helpfile = Path("PAGES_SETUP.md")
        helpfile.write_text(msg.strip() + "\n")

        return _create_workflow(
            use_docs=use_docs, only_on_index=only_on_index, branch=branch
        )

    else:
        raise ValueError("mode must be 'gh-actions' or 'main'")
