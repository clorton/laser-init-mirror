# Plan to Build Documentation with MkDocs

Here's a comprehensive plan for building and deploying documentation with MkDocs for the laser-init project:

## Phase 1: Configuration & Setup

1. Update mkdocs.yml configuration

- Set proper site name, description, and repository URL
- Configure navigation structure to organize all existing docs
- Add theme configuration (recommend Material for MkDocs for better features)
- Configure markdown extensions for code highlighting, admonitions, tables, etc.
- Set up search functionality
- Configure site metadata (author, copyright, etc.)

2. Install additional MkDocs plugins (add to pyproject.toml [dev] section)

- mkdocs-material - Modern responsive theme with many features
- mkdocstrings[python] - Auto-generate API docs from docstrings
- mkdocs-git-revision-date-localized-plugin - Show last updated dates
- mkdocs-include-markdown-plugin - Include/reuse markdown content
- mkdocs-awesome-pages-plugin - Simplified navigation management (optional)

## Phase 2: Content Organization

3. Restructure existing documentation

- Convert docs/index.md from MkDocs boilerplate to actual landing page (can use README.md as source)
- Review and update all existing docs:
  - docs/userguide.md
  - docs/datasources.md
  - docs/models.md
  - docs/architecture.md
  - docs/configuration.md
  - docs/contributing.md
- Create additional pages as needed:
  - Installation guide
  - Quick start tutorial
  - Troubleshooting guide
  - API reference (auto-generated)

4. Create API reference documentation

- Set up mkdocstrings to auto-generate API docs from your Google-style docstrings
- Create API reference pages for:
  - Core modules (config, cli, utils)
  - Extractors (gadm, geoboundaries, worldpop, unwpp, unocha)
  - Transformers (gadm, geoboundaries, unwpp, unocha)
  - Models (si, sir, seir, plot)
- Ensure all docstrings follow Google style and include Args, Returns, Raises sections

## Phase 3: Enhancement

5. Add code examples and tutorials

- Create runnable code examples in docstrings
- Add practical tutorials with real use cases
- Include sample outputs and visualizations
- Document common workflows and best practices

6. Add media and assets

- Create/add diagrams for architecture and workflows
- Include example plots and outputs
- Add logos or branding if applicable
- Create favicon for the docs site

## Phase 4: Build & Test

7. Local testing

- Run mkdocs serve to preview documentation locally
- Verify all internal links work correctly
- Check that code highlighting renders properly
- Ensure navigation is intuitive and complete
- Test search functionality
- Verify responsive design on mobile/tablet

8. Build static site

- Run mkdocs build to generate static HTML
- Review build warnings/errors
- Check output in site/ directory
- Validate HTML/CSS if needed

## Phase 5: Deployment

9. Choose deployment strategy

- Option A: GitHub Pages (recommended for open source)
  - Use mkdocs gh-deploy command for automatic deployment
  - Configure GitHub repository settings
  - Set up custom domain if needed
- Option B: ReadTheDocs
  - Import project to ReadTheDocs
  - Configure .readthedocs.yaml
  - Enable versioned documentation
- Option C: Self-hosted
  - Deploy site/ directory to web server
  - Configure web server (nginx/apache)

10. Set up automated deployment

- Create GitHub Actions workflow for automatic builds on push/PR
- Configure to deploy to GitHub Pages or other platform
- Add documentation build status badge to README


## Phase 6: Maintenance

11. Documentation maintenance process

- Add documentation review to PR checklist
- Keep docs in sync with code changes
- Regularly update examples and tutorials
- Monitor and fix broken links
- Update changelog in docs

12. Create documentation contribution guide

- Document how to build docs locally
- Explain documentation structure
- Provide style guide for documentation
- Include instructions for adding new pages

----

## Recommended Package Dependencies (for pyproject.toml [dependency-groups] dev)

```
dev = [
    "mkdocs>=1.6.1",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.26.0",
    "mkdocs-git-revision-date-localized-plugin>=1.3.0",
    "mkdocs-include-markdown-plugin>=7.0.0",
    "pytest>=9.0.2",
    "pytest-cov>=6.0.0",
]
```

## Quick Commands Reference

Once configured, you'll use these commands:
- `mkdocs serve` - Start development server with live reload
- `mkdocs build` - Build static site to site/ directory
- `mkdocs build` --strict - Build with warnings as errors
- `mkdocs gh-deploy` - Build and deploy to GitHub Pages
- `mkdocs --help` - View all available commands

----

This plan provides a systematic approach to building professional documentation for laser-init. The most impactful early steps would be:

Phase 1 items 1-2: Configure mkdocs.yml and install plugins
Phase 2 item 3: Update docs/index.md to be a proper landing page
Phase 4 item 7: Test locally with mkdocs serve

----

## Verifcation

1. Check that all dependencies are installed:

```shell
uv sync
```

2. Test the MkDocs configuration:

```shell
mkdocs --version
```

3. Preview the documentation locally:

```shell
mkdocs serve
```

This will start a development server at http://127.0.0.1:8000. Open this in your browser to see the documentation site with the Material theme.

**Note:** You may see griffe warnings about missing type annotations. These are informational only and don't affect the documentation output. To suppress them, use:

```shell
PYTHONWARNINGS="ignore" mkdocs serve
```

Or to suppress only griffe warnings:

```shell
mkdocs serve 2>&1 | grep -v "griffe:"
```

4. Check for configuration errors:

```shell
mkdocs build --strict
```

This will build the site and report any warnings as errors. Note: This will show warnings about missing pages (like installation.md, quickstart.md, etc.) which is expected - we'll create those in Phase 2.

### What You Should See:

- When running `mkdocs serve`, you should see the Material theme with indigo colors
- Light/dark mode toggle in the header
- Navigation tabs for different sections
- Search functionality
- The existing docs (`index.md`, `userguide.md`, etc.) rendered with the new theme
- The build will warn about missing API reference pages, which is expected - those - will be created in later phases.

## Verification for Phase 2 Part 3

After completing Phase 2 part 3, verify the work by:

### 1. Check that all documentation files exist:

```shell
ls -1 docs/
```

You should see:
- index.md (updated landing page)
- installation.md (new)
- quickstart.md (new)
- userguide.md (reviewed)
- configuration.md (reviewed)
- datasources.md (reviewed)
- models.md (reviewed)
- architecture.md (reviewed)
- contributing.md (reviewed)

### 2. Preview the documentation:

```shell
mkdocs serve
```

Then visit http://127.0.0.1:8000 and verify:

- [ ] Home page loads with laser-init overview
- [ ] "Getting Started" section appears in navigation with Installation and Quick Start
- [ ] All navigation links work
- [ ] No major formatting issues
- [ ] Light/dark mode toggle works
- [ ] Search function works (try searching for "laser-init")

### 3. Build the documentation:

```shell
mkdocs build
```

You should see output like:
```
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: site
INFO    -  Documentation built in X.XX seconds
```

Warnings about missing API reference pages (api/*.md) are expected at this stage.

### 4. Check the built site:

```shell
ls -1 site/
```

You should see generated HTML files including:
- index.html
- installation/
- quickstart/
- userguide/
- etc.

### What's Complete

Phase 2 parts 3 and 4 are now complete:

**Part 3 - Documentation restructuring:**
- ✅ Landing page (index.md) converted from boilerplate
- ✅ Installation guide created
- ✅ Quick start guide created
- ✅ Troubleshooting guide created
- ✅ All existing docs reviewed (userguide, datasources, models, architecture, configuration, contributing)

**Part 4 - API reference:**
- ✅ API reference directory structure created
- ✅ Core module API pages (cli, config, utils, logger)
- ✅ Extractor API pages (gadm, geoboundaries, worldpop, unwpp, unocha)
- ✅ Transformer API pages (gadm, geoboundaries, unwpp, unocha)
- ✅ Model API pages (si, sir, seir, plot)
- ✅ mkdocs.yml navigation updated with troubleshooting page

### What's Next

Remaining tasks for Phase 2:
- Verify all docstrings follow Google style (manual code review)
- Ensure all docstrings include Args, Returns, Raises sections (manual code review)

These tasks are best done through code review and are not part of the automated documentation setup.

## Verification for Phase 2 Parts 3 & 4 (Complete)

After completing all Phase 2 work, verify by:

### 1. Check all documentation files exist:

```shell
ls -1 docs/
ls -1 docs/api/
ls -1 docs/api/extractors/
ls -1 docs/api/transformers/
ls -1 docs/api/models/
```

You should see all documentation and API reference files.

### 2. Preview the complete documentation:

```shell
mkdocs serve
```

Then visit http://127.0.0.1:8000 and verify:

- [ ] Home page loads correctly
- [ ] All navigation sections work (Getting Started, User Guide, Configuration, etc.)
- [ ] Troubleshooting page appears in navigation
- [ ] API Reference section expands with all modules
- [ ] All API reference pages load and show module documentation
- [ ] Code examples are syntax highlighted
- [ ] Search works for all content
- [ ] Light/dark mode toggle works

### 3. Build the complete site:

```shell
mkdocs build
```

Should complete without errors. Warnings about docstrings are OK and expected.

### 4. Verify API documentation renders:

Visit these pages in your browser after running `mkdocs serve`:

- http://127.0.0.1:8000/api/cli/
- http://127.0.0.1:8000/api/extractors/gadm/
- http://127.0.0.1:8000/api/transformers/unocha/
- http://127.0.0.1:8000/api/models/seir/

Each should show:
- Module/class documentation from docstrings
- Function signatures
- Source code toggle (if docstrings exist)

### 5. Test navigation flow:

Try navigating through the documentation as a new user would:

1. Start at Home
2. Go to Installation
3. Follow Quick Start
4. Explore API Reference
5. Check Troubleshooting for common issues

### Summary of Created Files

**New documentation pages:**
- docs/installation.md
- docs/quickstart.md
- docs/troubleshooting.md

**API reference pages (17 total):**
- docs/api/cli.md
- docs/api/config.md
- docs/api/utils.md
- docs/api/logger.md
- docs/api/extractors/gadm.md
- docs/api/extractors/geoboundaries.md
- docs/api/extractors/worldpop.md
- docs/api/extractors/unwpp.md
- docs/api/extractors/unocha.md
- docs/api/transformers/gadm.md
- docs/api/transformers/geoboundaries.md
- docs/api/transformers/unwpp.md
- docs/api/transformers/unocha.md
- docs/api/models/si.md
- docs/api/models/sir.md
- docs/api/models/seir.md
- docs/api/models/plot.md

**Modified files:**
- docs/index.md (updated from boilerplate)
- mkdocs.yml (added troubleshooting to navigation)

## Verification for Phase 5: GitHub Pages Deployment

After setting up GitHub Pages deployment, follow these steps:

### 1. Enable GitHub Pages in Repository Settings

Before the workflow can deploy, you need to enable GitHub Pages:

1. Go to your GitHub repository: https://github.com/laser-base/laser-init
2. Click **Settings** (top navigation)
3. Click **Pages** (left sidebar under "Code and automation")
4. Under "Build and deployment":
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select "gh-pages" and "/ (root)"
   - Click **Save**

**Note**: The `gh-pages` branch will be created automatically by the workflow on first deployment.

### 2. Commit and Push the Workflow

```shell
# Stage the new workflow and updated files
git add .github/workflows/docs.yml
git add .gitignore
git add docs/
git add mkdocs.yml

# Commit
git commit -m "Add GitHub Pages deployment workflow for documentation"

# Push to main branch (triggers the workflow)
git push origin main
```

### 3. Monitor the Workflow Execution

1. Go to the **Actions** tab in your GitHub repository
2. You should see a "Documentation" workflow running
3. Click on the workflow to see detailed logs
4. Wait for it to complete (usually 2-5 minutes)

### 4. Verify Deployment

After the workflow completes successfully:

1. Go to **Settings** → **Pages** to see the deployment URL
2. Your documentation should be available at: `https://laser-base.github.io/laser-init/`
3. Visit the URL and verify:
   - [ ] Site loads correctly
   - [ ] Navigation works
   - [ ] Search functionality works
   - [ ] All pages render properly
   - [ ] API documentation displays correctly

### 5. Test Automatic Updates

Make a small change to test automatic deployment:

```shell
# Edit a documentation file
echo "\n## Test Update\n\nThis verifies automatic deployment." >> docs/index.md

# Commit and push
git add docs/index.md
git commit -m "Test: Verify automatic documentation deployment"
git push origin main
```

Watch the Actions tab to see the workflow trigger automatically. After completion, verify the change appears on the live site.

### 6. Add Documentation Badge to README (Optional)

Add a badge to show documentation build status:

```markdown
[![Documentation](https://github.com/laser-base/laser-init/actions/workflows/docs.yml/badge.svg)](https://github.com/laser-base/laser-init/actions/workflows/docs.yml)
```

### Troubleshooting Deployment Issues

#### Workflow Fails with Permission Error

If you see permission errors:
1. Go to **Settings** → **Actions** → **General**
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click **Save**

#### GitHub Pages Not Showing

If GitHub Pages settings don't show the `gh-pages` branch:
1. Wait for the workflow to complete successfully first
2. Refresh the Pages settings page
3. The `gh-pages` branch should now be available

#### 404 Error on Documentation Site

If you get a 404 error:
1. Check that the `gh-pages` branch exists: `git ls-remote origin gh-pages`
2. Verify the branch has content: Check the `gh-pages` branch on GitHub
3. Wait 5-10 minutes for GitHub Pages to build and deploy

#### Build Fails in Workflow

Check the workflow logs for specific errors:
1. Missing dependencies: Ensure `pyproject.toml` has all required packages
2. Import errors: Make sure `__init__.py` files exist in all module directories
3. Broken links: Fix any broken internal links reported by `mkdocs build --strict`

### What's Complete

Phase 5 deployment is now set up:
- ✅ GitHub Actions workflow created (`.github/workflows/docs.yml`)
- ✅ Automated build on push to main branch
- ✅ Automated deployment to GitHub Pages
- ✅ Build validation on pull requests (no deployment)
- ✅ `.gitignore` updated to exclude `site/` directory

### What's Next

Optional enhancements:
- Add documentation badge to README
- Set up custom domain (if desired)
- Configure version management with mike
- Add link checking workflow

----

## Task Checklist

### Phase 1: Configuration & Setup

#### 1. Update mkdocs.yml configuration
- [x] Set proper site name, description, and repository URL
- [x] Configure navigation structure to organize all existing docs
- [x] Add theme configuration (Material for MkDocs)
- [x] Configure markdown extensions for code highlighting
- [x] Configure markdown extensions for admonitions
- [x] Configure markdown extensions for tables
- [x] Set up search functionality
- [x] Configure site metadata (author, copyright, etc.)

#### 2. Install additional MkDocs plugins
- [x] Add mkdocs-material to pyproject.toml [dev] section
- [x] Add mkdocstrings[python] to pyproject.toml [dev] section
- [x] Add mkdocs-git-revision-date-localized-plugin to pyproject.toml [dev] section
- [x] Add mkdocs-include-markdown-plugin to pyproject.toml [dev] section
- [ ] (Optional) Add mkdocs-awesome-pages-plugin to pyproject.toml [dev] section
- [x] Run `uv sync` to install new dependencies

### Phase 2: Content Organization

#### 3. Restructure existing documentation
- [x] Convert docs/index.md from boilerplate to landing page (use README.md as source)
- [x] Review and update docs/userguide.md
- [x] Review and update docs/datasources.md
- [x] Review and update docs/models.md
- [x] Review and update docs/architecture.md
- [x] Review and update docs/configuration.md
- [x] Review and update docs/contributing.md
- [x] Create installation guide page
- [x] Create quick start tutorial page
- [x] Create troubleshooting guide page
- [x] Create API reference structure

#### 4. Create API reference documentation
- [x] Set up mkdocstrings configuration in mkdocs.yml
- [x] Create API reference page for core modules (config, cli, utils)
- [x] Create API reference page for logger module
- [x] Create API reference page for extractors (gadm, geoboundaries, worldpop, unwpp, unocha)
- [x] Create API reference page for transformers (gadm, geoboundaries, unwpp, unocha)
- [x] Create API reference page for models (si, sir, seir, plot)
- [ ] Verify all docstrings follow Google style
- [ ] Ensure all docstrings include Args, Returns, Raises sections

### Phase 3: Enhancement

#### 5. Add code examples and tutorials
- [ ] Add runnable code examples to docstrings
- [ ] Create practical tutorial for basic usage
- [ ] Create tutorial for advanced customization
- [ ] Include sample outputs and visualizations in tutorials
- [ ] Document common workflows
- [ ] Document best practices

#### 6. Add media and assets
- [ ] Create architecture diagram
- [ ] Create workflow diagram
- [ ] Add example plots to docs
- [ ] Add example outputs to docs
- [ ] Add logo or branding (if applicable)
- [ ] Create favicon for docs site

### Phase 4: Build & Test

#### 7. Local testing
- [ ] Run `mkdocs serve` to preview documentation
- [ ] Verify all internal links work correctly
- [ ] Check that code highlighting renders properly
- [ ] Ensure navigation is intuitive and complete
- [ ] Test search functionality
- [ ] Verify responsive design on mobile
- [ ] Verify responsive design on tablet

#### 8. Build static site
- [ ] Run `mkdocs build` to generate static HTML
- [ ] Review build warnings
- [ ] Review build errors
- [ ] Check output in site/ directory
- [ ] Validate HTML/CSS if needed

### Phase 5: Deployment

#### 9. Choose deployment strategy
- [x] Decide on deployment platform (GitHub Pages, ReadTheDocs, or self-hosted)
- [x] If GitHub Pages: Use `mkdocs gh-deploy` for deployment
- [x] If GitHub Pages: Configure GitHub repository settings
- [ ] If GitHub Pages: Set up custom domain (if needed)
- [ ] If ReadTheDocs: Import project to ReadTheDocs
- [ ] If ReadTheDocs: Configure .readthedocs.yaml
- [ ] If ReadTheDocs: Enable versioned documentation
- [ ] If self-hosted: Deploy site/ directory to web server
- [ ] If self-hosted: Configure web server (nginx/apache)

#### 10. Set up automated deployment
- [x] Create GitHub Actions workflow file
- [x] Configure workflow to build docs on push/PR
- [x] Configure workflow to deploy to chosen platform
- [ ] Add documentation build status badge to README
- [ ] Test automated deployment with a test commit

### Phase 6: Maintenance

#### 11. Documentation maintenance process
- [ ] Add documentation review to PR checklist
- [ ] Document process for keeping docs in sync with code changes
- [ ] Set up schedule for regularly updating examples and tutorials
- [ ] Set up process for monitoring and fixing broken links
- [ ] Create process for updating changelog in docs

#### 12. Create documentation contribution guide
- [ ] Document how to build docs locally in CONTRIBUTING.md
- [ ] Explain documentation structure
- [ ] Provide style guide for documentation
- [ ] Include instructions for adding new pages
- [ ] Document how to preview changes locally
