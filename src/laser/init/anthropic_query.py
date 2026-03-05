#!/usr/bin/env python3
"""
This module provides functionality to query the Anthropic API for country information.
"""

if __name__ == "__main__":
    import argparse

    from .utils import iso_from_country_string

    parser = argparse.ArgumentParser(description="Query the Anthropic API for country information.")
    parser.add_argument("country_name", type=str, help="The name of the country to query.")
    args = parser.parse_args()

    iso_code = iso_from_country_string(args.country_name)
    if iso_code:
        print(f"The ISO 3166-1 alpha-3 code for '{args.country_name}' is: {iso_code}")
    else:
        print(f"No ISO code found for '{args.country_name}'.")
