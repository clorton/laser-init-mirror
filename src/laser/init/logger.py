"""Logging configuration and setup for laser-init.

This module configures a dual-handler logging system with different output levels
for console and file logging. The logger is automatically configured when the module
is imported, providing consistent logging across the entire laser-init package.

Logging Configuration:
    Console Handler:
        - Level: WARNING and above
        - Format: "%(asctime)s - %(levelname)s - %(message)s"
        - Output: stderr (standard error stream)
        - Purpose: Show important warnings and errors to users during execution

    File Handler:
        - Level: DEBUG and above (captures all log messages)
        - Format: "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        - Output: Timestamped log file in configured log directory
        - Filename: laser-init_YYYYMMDD_HHMMSS.log
        - Default Location: ~/.laser/logs/
        - Purpose: Complete diagnostic information for troubleshooting

Log Directory Configuration:
    The log directory can be configured via the configuration file:
        - Config key: "log_dir"
        - Default: ~/.laser/logs/
        - Directory is created automatically if it doesn't exist

Module Attributes:
    logger (logging.Logger): Pre-configured logger instance named "laser-init".
        Use this throughout the package for consistent logging.

Usage:
    ```python
    from laser.init.logger import logger

    # Log at different levels
    logger.debug("Detailed diagnostic information")
    logger.info("General informational message")
    logger.warning("Warning message (shown in console)")
    logger.error("Error message (shown in console)")
    logger.critical("Critical error (shown in console)")
    ```

Effects of Importing This Module:
    - Creates ~/.laser/logs/ directory if it doesn't exist
    - Creates a new timestamped log file for this session
    - Configures the global "laser-init" logger with dual handlers
    - Sets logger.propagate = False to prevent duplicate messages

Log Levels:
    - DEBUG (10): Detailed information for diagnosing problems
    - INFO (20): General informational messages about execution
    - WARNING (30): Warnings about potential issues (shown on console)
    - ERROR (40): Error messages for failures (shown on console)
    - CRITICAL (50): Critical errors requiring immediate attention (shown on console)

Notes:
    - Each execution creates a new log file with a unique timestamp
    - Old log files are not automatically deleted (manual cleanup required)
    - Console output is minimal (warnings and errors only) to avoid cluttering output
    - File logs contain complete execution trace for debugging
    - The logger name "laser-init" is used consistently across the package

Examples:
    Import and use the logger in any module:

    ```python
    from laser.init.logger import logger

    def download_data(url):
        logger.info(f"Downloading data from {url}")
        try:
            # ... download logic ...
            logger.debug(f"Download completed: {len(data)} bytes")
        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise
    ```

    Check log files for detailed execution history:

    ```shell
    # View most recent log file
    ls -t ~/.laser/logs/ | head -1 | xargs -I {} cat ~/.laser/logs/{}

    # Monitor logs in real-time
    tail -f ~/.laser/logs/laser-init_*.log
    ```
"""

import logging

# Set up logging: console at WARN+, file at DEBUG+ with timestamped filename
from datetime import datetime
from pathlib import Path

from .config import configuration as config

__all__ = ["logger"]

logger = logging.getLogger("laser-init")
logger.setLevel(logging.DEBUG)

# Console handler (WARN or higher)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARN)
console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# File handler (all logs, timestamped file)
log_dir = Path(config.get("log_dir", Path("~").expanduser() / ".laser" / "logs"))
log_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"laser-init_{timestamp}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

logger.propagate = False
