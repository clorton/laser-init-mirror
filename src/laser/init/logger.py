"""
Logging setup for laser-init. Configures both console and file logging with appropriate levels and formats.
- Console: WARN and above, with timestamps.
- File: DEBUG and above, with timestamps and logger names, saved to a timestamped file in a configurable log directory (defaulting to a "logs" folder in the project root).
- Uses the standard Python logging library, and is designed to be imported and used across the laser.init package for consistent logging.
"""

import logging

# Set up logging: console at WARN+, file at DEBUG+ with timestamped filename
from datetime import datetime
from pathlib import Path

from .config import configuration as config

__all__ = ["logger"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler (WARN or higher)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARN)
console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# File handler (all logs, timestamped file)
log_dir = Path(config.get("log_dir", Path(__file__).parent.parent.parent.parent / "logs"))
log_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"laser-init_{timestamp}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

logger.propagate = False
