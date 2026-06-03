# GitHub Pages Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy the repository as a GitHub Pages static site with a root homepage that links to the existing App Store documents.

**Architecture:** This is a no-build static deployment. GitHub Actions uploads the repository contents as a Pages artifact, and GitHub Pages serves committed HTML files directly.

**Tech Stack:** Static HTML, GitHub Actions, GitHub Pages official actions.

---

## File Structure

- Create `index.html`: Root document directory page with links to existing `AppStore` documents.
- Create `.nojekyll`: Empty marker file to disable Jekyll processing.
- Create `.github/workflows/pages.yml`: Workflow that deploys static content from `main`.

### Task 1: Add Root Homepage

**Files:**
- Create: `index.html`

- [ ] **Step 1: Confirm the target documents exist**

Run:

```bash
test -f AppStore/privacy_zh-CN.html
test -f AppStore/privacy_en.html
test -f AppStore/terms_zh-CN.html
test -f AppStore/terms_en.html
test -f AppStore/technical-support.html
```

Expected: exit 0.

- [ ] **Step 2: Create `index.html`**

Create a static HTML page with:

- Title: `THDatabase Documents`
- Heading: `THDatabase Documents`
- Links to:
  - `AppStore/privacy_zh-CN.html`
  - `AppStore/privacy_en.html`
  - `AppStore/terms_zh-CN.html`
  - `AppStore/terms_en.html`
  - `AppStore/technical-support.html`
  - `AppStore/app_store_listing.md`
  - `AppStore/screenshot_guide.md`
- Styling compatible with the existing policy pages.

- [ ] **Step 3: Verify homepage links point to committed files**

Run:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            href = attrs.get("href")
            if href and not href.startswith(("http://", "https://", "mailto:")):
                self.hrefs.append(href)

parser = LinkParser()
parser.feed(Path("index.html").read_text())
missing = [href for href in parser.hrefs if not Path(href).is_file()]
if missing:
    raise SystemExit(f"Missing link targets: {missing}")
print(f"Checked {len(parser.hrefs)} local links")
PY
```

Expected: `Checked 7 local links`.

### Task 2: Add GitHub Pages Deployment

**Files:**
- Create: `.nojekyll`
- Create: `.github/workflows/pages.yml`

- [ ] **Step 1: Create `.nojekyll`**

Create an empty `.nojekyll` file at the repository root.

- [ ] **Step 2: Create `.github/workflows/pages.yml`**

Use this workflow:

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: .

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: Verify workflow syntax and required action names**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path(".github/workflows/pages.yml").read_text()
required = [
    "actions/checkout@v6",
    "actions/configure-pages@v5",
    "actions/upload-pages-artifact@v4",
    "actions/deploy-pages@v4",
    "pages: write",
    "id-token: write",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"Missing required workflow content: {missing}")
print("Workflow contains required Pages actions and permissions")
PY
```

Expected: `Workflow contains required Pages actions and permissions`.

### Task 3: Final Verification and Commit

**Files:**
- Verify: `index.html`
- Verify: `.nojekyll`
- Verify: `.github/workflows/pages.yml`

- [ ] **Step 1: Review changed files**

Run:

```bash
git diff -- index.html .nojekyll .github/workflows/pages.yml
```

Expected: diff only contains the root homepage, `.nojekyll`, and Pages workflow.

- [ ] **Step 2: Verify all deployment files exist**

Run:

```bash
test -f index.html
test -f .nojekyll
test -f .github/workflows/pages.yml
```

Expected: exit 0.

- [ ] **Step 3: Commit deployment files**

Run:

```bash
git add index.html .nojekyll .github/workflows/pages.yml docs/superpowers/plans/2026-06-03-github-pages-deployment.md
git commit -m "chore: deploy static docs to github pages"
```

Expected: commit succeeds.
