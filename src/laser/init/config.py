import json
import warnings
from pathlib import Path

import yaml

from laser.init import __version__

__all__ = ["VERSION", "configuration"]

VERSION = __version__

configuration = {}

# look for laser_config.yaml in the user's home directory / .laser, then in the
# current working directory
for path in [
    Path.home() / ".laser" / "laser_config.yaml",
    Path.cwd() / "laser_config.yaml",
    Path.home() / ".laser" / "laser_config.json",
    Path.cwd() / "laser_config.json",
]:
    if path.is_file():
        if path.suffix.lower() == ".yaml":
            try:
                configuration = yaml.safe_load(path.read_text())
            except yaml.YAMLError as e:
                warnings.warn(f"Error parsing YAML configuration file {path}: {e}", stacklevel=2)
                configuration = {}
            break
        elif path.suffix.lower() == ".json":
            try:
                configuration = json.loads(path.read_text())
            except json.JSONDecodeError as e:
                warnings.warn(f"Error parsing JSON configuration file {path}: {e}", stacklevel=2)
                configuration = {}
            break
