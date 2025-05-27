# Documentation Archive Site

> **Note**: All documentation is written in English only.

To preserve the docs after the repository is archived, you can build
and publish a static site using **MkDocs**.

## Build the site

1. Install MkDocs:
   ```bash
   python -m pip install mkdocs
   ```
2. Generate the HTML output:
   ```bash
   mkdocs build --site-dir site
   ```
   The generated files under `site/` can be served by any static web host.

## Publish on GitHub Pages

1. Commit the `site/` directory on the `gh-pages` branch.
2. Enable **GitHub Pages** for that branch in the repository settings.
3. Future documentation updates only require rebuilding and pushing the
   `site/` directory.
