# Installation

This guide covers different ways to install laser-init on your system.

## Prerequisites

Before installing laser-init, ensure you have:

- **Python 3.10 or higher** - Check your version with `python3 --version`
- **Internet connection** - Required for downloading data sources
- **Disk space** - ~500MB-2GB for cached data (varies by country and data source)

## Recommended Installation (uv)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that provides excellent dependency resolution and virtual environment management.

### Install uv

If you don't have uv installed:

=== "macOS/Linux"
    ```shell
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows"
    ```shell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

### Install laser-init with uv

```shell
# Clone the repository
git clone https://github.com/laser-base/laser-init.git
cd laser-init

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\\Scripts\\activate     # Windows
```

The `uv sync` command automatically:

- Creates a virtual environment in `.venv/`
- Installs laser-init and all dependencies
- Locks dependencies for reproducibility

## Alternative Installation (pip)

If you prefer using pip:

```shell
# Clone the repository
git clone https://github.com/laser-base/laser-init.git
cd laser-init

# Create and activate virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\\Scripts\\activate     # Windows

# Install the package in editable mode
pip install -e .
```

## Verify Installation

After installation, verify that laser-init is working:

```shell
# Check that the command is available
laser-init --help

# Check the version
laser-init --version
```

You should see the help message with available commands and options.

## Development Installation

If you plan to contribute to laser-init or modify the code:

```shell
# Clone the repository
git clone https://github.com/laser-base/laser-init.git
cd laser-init

# Install with development dependencies
uv sync --group dev

# This installs additional tools:
# - pytest and pytest-cov for testing
# - ruff for linting
# - mkdocs and plugins for documentation
```

## System Dependencies

laser-init uses several Python packages that may require system-level dependencies:

### GDAL/Geospatial Libraries

The geospatial functionality relies on GDAL, which is typically installed automatically via Python packages. However, if you encounter issues:

=== "macOS"
    ```shell
    brew install gdal
    ```

=== "Ubuntu/Debian"
    ```shell
    sudo apt-get update
    sudo apt-get install gdal-bin libgdal-dev
    ```

=== "Windows"
    GDAL wheels are usually available on PyPI, but if needed, see [OSGeo4W](https://www.osgeo.org/projects/osgeo4w/)

## Troubleshooting

### ImportError: No module named 'laser.init'

If you encounter this error after installation:

1. Ensure you're in the correct virtual environment
2. Try reinstalling: `uv sync --refresh` or `pip install -e . --force-reinstall`

### Command not found: laser-init

If the command isn't found after installation:

1. Ensure you've activated the virtual environment
2. Check that the package is installed: `pip list | grep laser-init`
3. Try running directly: `python -m laser.init.cli --help`

### GDAL/Geospatial Errors

If you encounter errors related to GDAL or geospatial operations:

1. Install system GDAL libraries (see above)
2. Ensure GDAL Python bindings match your system GDAL version
3. Check `import gdal` works in Python

### Permission Errors

If you encounter permission errors:

- Don't use `sudo` with pip/uv - use virtual environments instead
- Ensure you have write permissions to the installation directory
- Use `--user` flag with pip if needed (not recommended)

## Upgrading

To upgrade to the latest version:

=== "uv"
    ```shell
    cd laser-init
    git pull origin main
    uv sync
    ```

=== "pip"
    ```shell
    cd laser-init
    git pull origin main
    pip install -e . --upgrade
    ```

## Uninstalling

To uninstall laser-init:

```shell
# If installed with pip
pip uninstall laser-init

# Remove the cloned repository
rm -rf laser-init
```

## Next Steps

After installation, proceed to:

- [Quick Start](quickstart.md) - Run your first model
- [Configuration](configuration.md) - Set up optional configuration
- [User Guide](userguide.md) - Learn detailed usage
