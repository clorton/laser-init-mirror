"""
Test suite for utility functions in the laser.init.utils module.

This module tests the iso_from_country_string function, which converts country names
and variations to their ISO 3166-1 alpha-3 codes. The tests cover:
- Exact ISO code matching (e.g., "USA" -> "USA")
- Exact country name matching (e.g., "United States of America" -> "USA")
- Fuzzy matching for misspellings and variants (e.g., "United States" -> "USA")
- Rejection of invalid/random strings (e.g., "xyz" -> None)
"""

import unittest

import pytest

from laser.init.utils import iso_from_country_string, level_from_string


class TestUtils(unittest.TestCase):
    @pytest.mark.skip(reason="Fuzzy matching tests are currently disabled.")
    def test_iso_from_country_string_fuzzy_match(self):
        """
        Test that fuzzy string matching works for misspelled or variant country names.

        This verifies that the function uses fuzzy matching (via rapidfuzz) to handle
        typos, alternative spellings, or minor variations in country names. Failure
        indicates the fuzzy matching algorithm is not working correctly.
        """
        # Africa : Burkina Faso, Eswatini, Democratic Republic of the Congo, Kenya, Madagascar, Mozambique, Nigeria, Senegal, South Africa, Sudan, Zambia  # noqa: E501
        self.assertEqual(iso_from_country_string("Burkina Fasso"), "BFA")  # Typo in Faso
        self.assertEqual(iso_from_country_string("Eswatini Kingdom"), "SWZ")  # Extra word
        self.assertEqual(iso_from_country_string("DRC"), "COD")  # Common abbreviation
        self.assertEqual(iso_from_country_string("Kenia"), "KEN")  # Alternative spelling
        self.assertEqual(iso_from_country_string("Madagaskar"), "MDG")  # Alternative spelling
        self.assertEqual(iso_from_country_string("Mocambique"), "MOZ")  # Alternative spelling
        self.assertEqual(iso_from_country_string("Nigera"), "NGA")  # Typo
        self.assertEqual(iso_from_country_string("Sénégal"), "SEN")  # Accent variation
        self.assertEqual(iso_from_country_string("S Africa"), "ZAF")  # Abbreviation
        self.assertEqual(iso_from_country_string("Soudan"), "SDN")  # French spelling
        self.assertEqual(iso_from_country_string("Zambiya"), "ZMB")  # Alternative spelling

        # Asia : Afghanistan, Cambodia, China, India, Japan, Pakistan, Vietnam
        self.assertEqual(iso_from_country_string("Afganistan"), "AFG")  # Missing 'h'
        self.assertEqual(iso_from_country_string("Cambodja"), "KHM")  # Alternative spelling
        self.assertEqual(iso_from_country_string("Chine"), "CHN")  # French spelling
        self.assertEqual(iso_from_country_string("Inde"), "IND")  # French spelling
        self.assertEqual(iso_from_country_string("Japon"), "JPN")  # French/Spanish spelling
        self.assertEqual(iso_from_country_string("Pakistán"), "PAK")  # Accent
        self.assertEqual(iso_from_country_string("Vietnam"), "VNM")  # Single word variant

        # Australia : Australia, New Zealand, Samoa, Papua New Guinea
        self.assertEqual(iso_from_country_string("Austrailia"), "AUS")  # Common typo
        self.assertEqual(iso_from_country_string("New Zeeland"), "NZL")  # Typo
        self.assertEqual(iso_from_country_string("Samoan"), "WSM")  # Demonym-like
        self.assertEqual(iso_from_country_string("Papua NG"), "PNG")  # Abbreviation

        # Europe : Azerbaijan, Bosnia and Herzegovina, Cyprus, Denmark, Estonia, Finland, Greece, Liechtenstein, Moldova, Portugal, San Marino, United Kingdom  # noqa: E501
        self.assertEqual(iso_from_country_string("Azerbajian"), "AZE")  # Typo
        self.assertEqual(iso_from_country_string("Bosnia"), "BIH")  # Partial name
        self.assertEqual(iso_from_country_string("Cypros"), "CYP")  # Typo
        self.assertEqual(iso_from_country_string("Danmark"), "DNK")  # Native spelling
        self.assertEqual(iso_from_country_string("Estland"), "EST")  # Alternative name
        self.assertEqual(iso_from_country_string("Finlande"), "FIN")  # French spelling
        self.assertEqual(iso_from_country_string("Grece"), "GRC")  # Missing accent
        self.assertEqual(iso_from_country_string("Lichtenstein"), "LIE")  # Typo
        self.assertEqual(iso_from_country_string("Moldavia"), "MDA")  # Alternative name
        self.assertEqual(iso_from_country_string("Portgual"), "PRT")  # Typo
        self.assertEqual(iso_from_country_string("San Merino"), "SMR")  # Typo
        self.assertEqual(iso_from_country_string("Great Britain"), "GBR")  # Alias

        # North America : Aruba, Belize, Canada, Dominican Republic, Guatemala, Saint Lucia, United States  # noqa: E501
        self.assertEqual(iso_from_country_string("Arba"), "ABW")  # Typo
        self.assertEqual(iso_from_country_string("Belise"), "BLZ")  # Typo
        self.assertEqual(iso_from_country_string("Canade"), "CAN")  # Typo
        self.assertEqual(iso_from_country_string("Domincan Republic"), "DOM")  # Typo
        self.assertEqual(iso_from_country_string("Guatamala"), "GTM")  # Typo
        self.assertEqual(iso_from_country_string("St Lucia"), "LCA")  # Abbreviation
        self.assertEqual(iso_from_country_string("United States"), "USA")  # Short form

        # South America : Argentina, Brazil, Chile, Colombia, Ecuador, Peru, Uruguay, Venezuela
        self.assertEqual(iso_from_country_string("Argentinia"), "ARG")  # Typo
        self.assertEqual(iso_from_country_string("Brasil"), "BRA")  # Portuguese spelling
        self.assertEqual(iso_from_country_string("Chili"), "CHL")  # Alternative spelling
        self.assertEqual(iso_from_country_string("Columbia"), "COL")  # Common typo
        self.assertEqual(iso_from_country_string("Equador"), "ECU")  # Alternative spelling
        self.assertEqual(iso_from_country_string("Perú"), "PER")  # With accent
        self.assertEqual(iso_from_country_string("Uraguay"), "URY")  # Typo
        self.assertEqual(iso_from_country_string("Venezuala"), "VEN")  # Typo


@pytest.mark.parametrize(
    "input_string, expected_iso",
    [
        ("BFA", "BFA"),
        ("SWZ", "SWZ"),
        ("COD", "COD"),
        ("KEN", "KEN"),
        ("MDG", "MDG"),
        ("MOZ", "MOZ"),
        ("NGA", "NGA"),
        ("SEN", "SEN"),
        ("ZAF", "ZAF"),
        ("SDN", "SDN"),
        ("ZMB", "ZMB"),
        ("AFG", "AFG"),
        ("KHM", "KHM"),
        ("CHN", "CHN"),
        ("IND", "IND"),
        ("JPN", "JPN"),
        ("PAK", "PAK"),
        ("VNM", "VNM"),
        ("AUS", "AUS"),
        ("NZL", "NZL"),
        ("WSM", "WSM"),
        ("PNG", "PNG"),
        ("AZE", "AZE"),
        ("BIH", "BIH"),
        ("CYP", "CYP"),
        ("DNK", "DNK"),
        ("EST", "EST"),
        ("FIN", "FIN"),
        ("GRC", "GRC"),
        ("LIE", "LIE"),
        ("MDA", "MDA"),
        ("PRT", "PRT"),
        ("SMR", "SMR"),
        ("GBR", "GBR"),
        ("ABW", "ABW"),
        ("BLZ", "BLZ"),
        ("CAN", "CAN"),
        ("DOM", "DOM"),
        ("GTM", "GTM"),
        ("LCA", "LCA"),
        ("USA", "USA"),
        ("ARG", "ARG"),
        ("BRA", "BRA"),
        ("CHL", "CHL"),
        ("COL", "COL"),
        ("ECU", "ECU"),
        ("PER", "PER"),
        ("URY", "URY"),
        ("VEN", "VEN"),
    ],
)
def test_iso_from_country_string_exact_ISO(input_string, expected_iso):
    """
    Test that ISO 3166-1 alpha-3 codes are correctly recognized and returned unchanged.

    This verifies that the function can handle direct ISO code input (e.g., "USA", "BFA")
    and return them as-is. Failure indicates the function cannot recognize valid ISO codes.
    """
    assert iso_from_country_string(input_string) == expected_iso

    return


@pytest.mark.parametrize(
    "input_string, expected_iso",
    [
        ("Burkina Faso", "BFA"),
        ("Eswatini", "SWZ"),
        ("Congo, The Democratic Republic of the", "COD"),
        ("Kenya", "KEN"),
        ("Madagascar", "MDG"),
        ("Mozambique", "MOZ"),
        ("Nigeria", "NGA"),
        ("Senegal", "SEN"),
        ("South Africa", "ZAF"),
        ("Sudan", "SDN"),
        ("Zambia", "ZMB"),
        ("Afghanistan", "AFG"),
        ("Cambodia", "KHM"),
        ("China", "CHN"),
        ("India", "IND"),
        ("Japan", "JPN"),
        ("Pakistan", "PAK"),
        ("Viet Nam", "VNM"),
        ("Australia", "AUS"),
        ("New Zealand", "NZL"),
        ("Samoa", "WSM"),
        ("Papua New Guinea", "PNG"),
        ("Azerbaijan", "AZE"),
        ("Bosnia and Herzegovina", "BIH"),
        ("Cyprus", "CYP"),
        ("Denmark", "DNK"),
        ("Estonia", "EST"),
        ("Finland", "FIN"),
        ("Greece", "GRC"),
        ("Liechtenstein", "LIE"),
        ("Moldova", "MDA"),
        ("Portugal", "PRT"),
        ("San Marino", "SMR"),
        ("United Kingdom", "GBR"),
        ("Aruba", "ABW"),
        ("Belize", "BLZ"),
        ("Canada", "CAN"),
        ("Dominican Republic", "DOM"),
        ("Guatemala", "GTM"),
        ("Saint Lucia", "LCA"),
        ("United States of America", "USA"),
        ("Argentina", "ARG"),
        ("Brazil", "BRA"),
        ("Chile", "CHL"),
        ("Colombia", "COL"),
        ("Ecuador", "ECU"),
        ("Peru", "PER"),
        ("Uruguay", "URY"),
        ("Venezuela, Bolivarian Republic of", "VEN"),
    ],
)
def test_iso_from_country_string_exact_country_names(input_string, expected_iso):
    """
    Test that exact country names are correctly mapped to their ISO 3166-1 alpha-3 codes.

    This verifies that the function can look up country names in the mapping dictionary
    and return the correct ISO code. Failure indicates incorrect or missing mappings.
    """
    assert iso_from_country_string(input_string) == expected_iso

    return


@pytest.mark.parametrize(
    "input_string, expected_iso",
    [
        ("xyz", None),
        ("asdfgh", None),
        ("qwerty", None),
        ("zxcvbnm", None),
        ("jkl", None),
        ("mnop", None),
        ("uvwxyz", None),
        ("abcdefghij", None),
        ("klmnopqrst", None),
        ("randomstring", None),
        ("notacountry", None),
        ("foo", None),
        ("bar", None),
        ("baz", None),
        ("invalidcountryname", None),
        ("zzz", None),
        ("abcdef", None),
        ("ghijkl", None),
        ("mnopqrstu", None),
        ("aaa", None),
        ("nonsense", None),
        ("gibberish", None),
        ("fakeplace", None),
    ],
)
def test_random_strings(input_string, expected_iso):
    """
    Test that random/invalid strings correctly return None.

    This verifies that the function properly rejects inputs that don't match any
    known country names or ISO codes, even with fuzzy matching. Failure indicates
    the function is incorrectly matching invalid inputs to real countries.
    """

    assert iso_from_country_string(input_string) is None

    return


@pytest.mark.parametrize(
    "input_string, expected_level",
    [
        ("ADMIN0", 0),
        ("ADMIN1", 1),
        ("ADMIN2", 2),
        ("ADMIN3", 3),
        ("ADMIN4", 4),
        ("admin0", 0),
        ("admin1", 1),
        ("admin2", 2),
        ("admin3", 3),
        ("admin4", 4),
        ("ADM0", 0),
        ("ADM1", 1),
        ("ADM2", 2),
        ("ADM3", 3),
        ("ADM4", 4),
        ("adm0", 0),
        ("adm1", 1),
        ("adm2", 2),
        ("adm3", 3),
        ("adm4", 4),
        ("0", 0),
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
    ],
)
def test_level_from_string(input_string, expected_level):
    """
    Test that various level string formats are correctly parsed to standardized level codes.

    This verifies that the function can handle different formats for administrative levels,
    including "adminX", "admX", and just "X". Failure indicates the function cannot
    correctly interpret level strings.
    """

    assert level_from_string(input_string) == expected_level

    return


if __name__ == "__main__":
    unittest.main()
