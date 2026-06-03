# GitHub Pages Deployment Design

## Goal

Deploy this public repository as a GitHub Pages static site at the repository Pages URL, with a usable root homepage and stable links to the existing App Store support documents.

## Current Context

The repository contains static documentation only. There is no build tool, package manifest, or generated site pipeline. Existing public content lives under `AppStore/`, including privacy policies, terms, and technical support pages.

## Recommended Approach

Use GitHub Pages with GitHub Actions. Add a Pages workflow that uploads the repository's static files as the Pages artifact and deploys them on pushes to `main`.

This keeps deployment behavior in version control and avoids moving the existing `AppStore/` files, so existing URLs remain stable.

## Files and Responsibilities

- `index.html`: Root homepage for the Pages site. It links to the existing privacy policy, terms, technical support, and related documents.
- `.nojekyll`: Disables Jekyll processing so GitHub Pages serves the static files exactly as committed.
- `.github/workflows/pages.yml`: GitHub Actions workflow that deploys the static repository content to GitHub Pages.
- Existing `AppStore/*.html`: Continue to be served from the same relative paths.

## Data Flow

1. A commit is pushed to `main`.
2. GitHub Actions packages the repository static files.
3. GitHub Pages deploys the artifact.
4. Visitors open `https://leotan1990.github.io/databases/` and use `index.html` as the document directory.

## Error Handling

The workflow should use GitHub's official Pages actions. If Pages is not set to use GitHub Actions as its source, the workflow may run without becoming the active Pages deployment. In that case, the repository owner needs to select `GitHub Actions` in the repository's Pages settings.

## Testing

Local verification should confirm that:

- `index.html` exists at the repository root.
- `index.html` links point to committed files.
- `.github/workflows/pages.yml` is valid YAML.
- The deployment workflow uses the official Pages action sequence: configure Pages, upload artifact, and deploy Pages.

## Scope

This change does not redesign the existing policy or support pages, introduce a static site generator, change repository visibility, or configure a custom domain.
