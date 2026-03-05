# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Comprehensive test suite for `iso_from_country_string` utility function
  - Added 46 test cases for exact ISO 3166-1 alpha-3 code matching
  - Added 46 test cases for exact country name to ISO code conversion
  - Added 46 test cases for fuzzy matching of misspelled/variant country names
  - Added 20 test cases for rejecting invalid/random input strings
  - Added detailed docstrings to all test functions explaining purpose and failure implications
  - Added module-level docstring to test file
- Added build system configuration to `pyproject.toml` for proper package installation
- Added `pytest-cov` to development dependencies for test coverage reporting

### Fixed
- Fixed pytest configuration error by adding missing `pytest-cov` dependency
- Fixed module import issues by configuring hatchling build backend with correct package paths
- Corrected coverage module name from `laser_init` to `laser.init` in pytest configuration
- Fixed `openai-query.py` OpenAI SDK incompatibility by switching to `responses.create(text={"format": ...})` for JSON schema structured outputs (openai==2.x)
- Removed hardcoded OpenAI API key from `openai-query.py` demo; now reads `OPENAI_API_KEY` from environment
- Added extensive inline documentation in `openai_query.py` explaining schema design and OpenAI Responses API arguments
- Improved `iso_from_country_string` matching by normalizing case/diacritics (e.g., "Sénégal") before exact/fuzzy matching
- Added explicit aliases for common French country spellings (e.g., "Chine", "Inde", "Japon")
- Added explicit alias "Estland" for Estonia (EST)
- Added French country names to name mapping.
