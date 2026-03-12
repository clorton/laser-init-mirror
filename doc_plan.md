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

Phase 2 part 3 is now complete:
- ✅ Landing page (index.md) converted from boilerplate
- ✅ Installation guide created
- ✅ Quick start guide created
- ✅ All existing docs reviewed (userguide, datasources, models, architecture, configuration, contributing)

### What's Next

Remaining tasks for Phase 2:
- Create troubleshooting guide page
- Create API reference structure (Phase 2 part 4)

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
- [ ] Create troubleshooting guide page
- [ ] Create API reference structure

#### 4. Create API reference documentation
- [x] Set up mkdocstrings configuration in mkdocs.yml
- [ ] Create API reference page for core modules (config, cli, utils)
- [ ] Create API reference page for logger module
- [ ] Create API reference page for extractors (gadm, geoboundaries, worldpop, unwpp, unocha)
- [ ] Create API reference page for transformers (gadm, geoboundaries, unwpp, unocha)
- [ ] Create API reference page for models (si, sir, seir, plot)
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
- [ ] Decide on deployment platform (GitHub Pages, ReadTheDocs, or self-hosted)
- [ ] If GitHub Pages: Use `mkdocs gh-deploy` for deployment
- [ ] If GitHub Pages: Configure GitHub repository settings
- [ ] If GitHub Pages: Set up custom domain (if needed)
- [ ] If ReadTheDocs: Import project to ReadTheDocs
- [ ] If ReadTheDocs: Configure .readthedocs.yaml
- [ ] If ReadTheDocs: Enable versioned documentation
- [ ] If self-hosted: Deploy site/ directory to web server
- [ ] If self-hosted: Configure web server (nginx/apache)

#### 10. Set up automated deployment
- [ ] Create GitHub Actions workflow file
- [ ] Configure workflow to build docs on push/PR
- [ ] Configure workflow to deploy to chosen platform
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
