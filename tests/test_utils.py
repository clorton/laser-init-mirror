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

from laser.init.utils import iso_from_country_string


class TestUtils(unittest.TestCase):
    def test_iso_from_country_string_exact_ISO(self):
        """
        Test that ISO 3166-1 alpha-3 codes are correctly recognized and returned unchanged.

        This verifies that the function can handle direct ISO code input (e.g., "USA", "BFA")
        and return them as-is. Failure indicates the function cannot recognize valid ISO codes.
        """
        # Africa : Burkina Faso, Eswatini, Democratic Republic of the Congo, Kenya, Madagascar, Mozambique, Nigeria, Senegal, South Africa, Sudan, Zambia  # noqa: E501
        self.assertEqual(iso_from_country_string("BFA"), "BFA")  # Burkina Faso
        self.assertEqual(iso_from_country_string("SWZ"), "SWZ")  # Eswatini
        self.assertEqual(iso_from_country_string("COD"), "COD")  # Democratic Republic of the Congo
        self.assertEqual(iso_from_country_string("KEN"), "KEN")  # Kenya
        self.assertEqual(iso_from_country_string("MDG"), "MDG")  # Madagascar
        self.assertEqual(iso_from_country_string("MOZ"), "MOZ")  # Mozambique
        self.assertEqual(iso_from_country_string("NGA"), "NGA")  # Nigeria
        self.assertEqual(iso_from_country_string("SEN"), "SEN")  # Senegal
        self.assertEqual(iso_from_country_string("ZAF"), "ZAF")  # South Africa
        self.assertEqual(iso_from_country_string("SDN"), "SDN")  # Sudan
        self.assertEqual(iso_from_country_string("ZMB"), "ZMB")  # Zambia

        # Asia : Afghanistan, Cambodia, China, India, Japan, Pakistan, Vietnam
        self.assertEqual(iso_from_country_string("AFG"), "AFG")  # Afghanistan
        self.assertEqual(iso_from_country_string("KHM"), "KHM")  # Cambodia
        self.assertEqual(iso_from_country_string("CHN"), "CHN")  # China
        self.assertEqual(iso_from_country_string("IND"), "IND")  # India
        self.assertEqual(iso_from_country_string("JPN"), "JPN")  # Japan
        self.assertEqual(iso_from_country_string("PAK"), "PAK")  # Pakistan
        self.assertEqual(iso_from_country_string("VNM"), "VNM")  # Vietnam

        # Australia : Australia, New Zealand, Samoa, Papua New Guinea
        self.assertEqual(iso_from_country_string("AUS"), "AUS")  # Australia
        self.assertEqual(iso_from_country_string("NZL"), "NZL")  # New Zealand
        self.assertEqual(iso_from_country_string("WSM"), "WSM")  # Samoa
        self.assertEqual(iso_from_country_string("PNG"), "PNG")  # Papua New Guinea

        # Europe : Azerbaijan, Bosnia and Herzegovina, Cyprus, Denmark, Estonia, Finland, Greece, Liechtenstein, Moldova, Portugal, San Marino, United Kingdom  # noqa: E501
        self.assertEqual(iso_from_country_string("AZE"), "AZE")  # Azerbaijan
        self.assertEqual(iso_from_country_string("BIH"), "BIH")  # Bosnia and Herzegovina
        self.assertEqual(iso_from_country_string("CYP"), "CYP")  # Cyprus
        self.assertEqual(iso_from_country_string("DNK"), "DNK")  # Denmark
        self.assertEqual(iso_from_country_string("EST"), "EST")  # Estonia
        self.assertEqual(iso_from_country_string("FIN"), "FIN")  # Finland
        self.assertEqual(iso_from_country_string("GRC"), "GRC")  # Greece
        self.assertEqual(iso_from_country_string("LIE"), "LIE")  # Liechtenstein
        self.assertEqual(iso_from_country_string("MDA"), "MDA")  # Moldova
        self.assertEqual(iso_from_country_string("PRT"), "PRT")  # Portugal
        self.assertEqual(iso_from_country_string("SMR"), "SMR")  # San Marino
        self.assertEqual(iso_from_country_string("GBR"), "GBR")  # United Kingdom

        # North America : Aruba, Belize, Canada, Dominican Republic, Guatemala, Saint Lucia, United States  # noqa: E501
        self.assertEqual(iso_from_country_string("ABW"), "ABW")  # Aruba
        self.assertEqual(iso_from_country_string("BLZ"), "BLZ")  # Belize
        self.assertEqual(iso_from_country_string("CAN"), "CAN")  # Canada
        self.assertEqual(iso_from_country_string("DOM"), "DOM")  # Dominican Republic
        self.assertEqual(iso_from_country_string("GTM"), "GTM")  # Guatemala
        self.assertEqual(iso_from_country_string("LCA"), "LCA")  # Saint Lucia
        self.assertEqual(iso_from_country_string("USA"), "USA")  # United States

        # South America : Argentina, Brazil, Chile, Colombia, Ecuador, Peru, Uruguay, Venezuela
        self.assertEqual(iso_from_country_string("ARG"), "ARG")  # Argentina
        self.assertEqual(iso_from_country_string("BRA"), "BRA")  # Brazil
        self.assertEqual(iso_from_country_string("CHL"), "CHL")  # Chile
        self.assertEqual(iso_from_country_string("COL"), "COL")  # Colombia
        self.assertEqual(iso_from_country_string("ECU"), "ECU")  # Ecuador
        self.assertEqual(iso_from_country_string("PER"), "PER")  # Peru
        self.assertEqual(iso_from_country_string("URY"), "URY")  # Uruguay
        self.assertEqual(iso_from_country_string("VEN"), "VEN")  # Venezuela

    def test_iso_from_country_string_exact_country_names(self):
        """
        Test that exact country names are correctly mapped to their ISO 3166-1 alpha-3 codes.

        This verifies that the function can look up country names in the mapping dictionary
        and return the correct ISO code. Failure indicates incorrect or missing mappings.
        """
        # Africa : Burkina Faso, Eswatini, Democratic Republic of the Congo, Kenya, Madagascar, Mozambique, Nigeria, Senegal, South Africa, Sudan, Zambia  # noqa: E501
        self.assertEqual(iso_from_country_string("Burkina Faso"), "BFA")
        self.assertEqual(iso_from_country_string("Eswatini"), "SWZ")
        self.assertEqual(iso_from_country_string("Congo, The Democratic Republic of the"), "COD")
        self.assertEqual(iso_from_country_string("Kenya"), "KEN")
        self.assertEqual(iso_from_country_string("Madagascar"), "MDG")
        self.assertEqual(iso_from_country_string("Mozambique"), "MOZ")
        self.assertEqual(iso_from_country_string("Nigeria"), "NGA")
        self.assertEqual(iso_from_country_string("Senegal"), "SEN")
        self.assertEqual(iso_from_country_string("South Africa"), "ZAF")
        self.assertEqual(iso_from_country_string("Sudan"), "SDN")
        self.assertEqual(iso_from_country_string("Zambia"), "ZMB")

        # Asia : Afghanistan, Cambodia, China, India, Japan, Pakistan, Vietnam
        self.assertEqual(iso_from_country_string("Afghanistan"), "AFG")
        self.assertEqual(iso_from_country_string("Cambodia"), "KHM")
        self.assertEqual(iso_from_country_string("China"), "CHN")
        self.assertEqual(iso_from_country_string("India"), "IND")
        self.assertEqual(iso_from_country_string("Japan"), "JPN")
        self.assertEqual(iso_from_country_string("Pakistan"), "PAK")
        self.assertEqual(iso_from_country_string("Viet Nam"), "VNM")

        # Australia : Australia, New Zealand, Samoa, Papua New Guinea
        self.assertEqual(iso_from_country_string("Australia"), "AUS")
        self.assertEqual(iso_from_country_string("New Zealand"), "NZL")
        self.assertEqual(iso_from_country_string("Samoa"), "WSM")
        self.assertEqual(iso_from_country_string("Papua New Guinea"), "PNG")

        # Europe : Azerbaijan, Bosnia and Herzegovina, Cyprus, Denmark, Estonia, Finland, Greece, Liechtenstein, Moldova, Portugal, San Marino, United Kingdom  # noqa: E501
        self.assertEqual(iso_from_country_string("Azerbaijan"), "AZE")
        self.assertEqual(iso_from_country_string("Bosnia and Herzegovina"), "BIH")
        self.assertEqual(iso_from_country_string("Cyprus"), "CYP")
        self.assertEqual(iso_from_country_string("Denmark"), "DNK")
        self.assertEqual(iso_from_country_string("Estonia"), "EST")
        self.assertEqual(iso_from_country_string("Finland"), "FIN")
        self.assertEqual(iso_from_country_string("Greece"), "GRC")
        self.assertEqual(iso_from_country_string("Liechtenstein"), "LIE")
        self.assertEqual(iso_from_country_string("Moldova"), "MDA")
        self.assertEqual(iso_from_country_string("Portugal"), "PRT")
        self.assertEqual(iso_from_country_string("San Marino"), "SMR")
        self.assertEqual(iso_from_country_string("United Kingdom"), "GBR")

        # North America : Aruba, Belize, Canada, Dominican Republic, Guatemala, Saint Lucia, United States  # noqa: E501
        self.assertEqual(iso_from_country_string("Aruba"), "ABW")
        self.assertEqual(iso_from_country_string("Belize"), "BLZ")
        self.assertEqual(iso_from_country_string("Canada"), "CAN")
        self.assertEqual(iso_from_country_string("Dominican Republic"), "DOM")
        self.assertEqual(iso_from_country_string("Guatemala"), "GTM")
        self.assertEqual(iso_from_country_string("Saint Lucia"), "LCA")
        self.assertEqual(iso_from_country_string("United States of America"), "USA")

        # South America : Argentina, Brazil, Chile, Colombia, Ecuador, Peru, Uruguay, Venezuela
        self.assertEqual(iso_from_country_string("Argentina"), "ARG")
        self.assertEqual(iso_from_country_string("Brazil"), "BRA")
        self.assertEqual(iso_from_country_string("Chile"), "CHL")
        self.assertEqual(iso_from_country_string("Colombia"), "COL")
        self.assertEqual(iso_from_country_string("Ecuador"), "ECU")
        self.assertEqual(iso_from_country_string("Peru"), "PER")
        self.assertEqual(iso_from_country_string("Uruguay"), "URY")
        self.assertEqual(iso_from_country_string("Venezuela, Bolivarian Republic of"), "VEN")

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

    def test_random_strings(self):
        """
        Test that random/invalid strings correctly return None.

        This verifies that the function properly rejects inputs that don't match any
        known country names or ISO codes, even with fuzzy matching. Failure indicates
        the function is incorrectly matching invalid inputs to real countries.
        """
        # Test 20 different random strings of length 3 to 20 characters
        with pytest.warns(
            UserWarning,
            match="No exact match found for input string 'xyz'. Looking for potential matches.",
        ):
            with pytest.warns(
                UserWarning,
                match="Input string is too short for reliable matching. Returning None.",
            ):
                self.assertIsNone(iso_from_country_string("xyz"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("asdfgh"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("qwerty"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("zxcvbnm"))
        with pytest.warns(
            UserWarning, match="Input string is too short for reliable matching. Returning None."
        ):
            self.assertIsNone(iso_from_country_string("jkl"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("mnop"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("uvwxyz"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("abcdefghij"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("klmnopqrst"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("randomstring"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("notacountry"))
        with pytest.warns(
            UserWarning, match="Input string is too short for reliable matching. Returning None."
        ):
            self.assertIsNone(iso_from_country_string("foo"))
        with pytest.warns(
            UserWarning, match="Input string is too short for reliable matching. Returning None."
        ):
            self.assertIsNone(iso_from_country_string("bar"))
        with pytest.warns(
            UserWarning, match="Input string is too short for reliable matching. Returning None."
        ):
            self.assertIsNone(iso_from_country_string("baz"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("invalidcountryname"))
        with pytest.warns(
            UserWarning, match="Input string is too short for reliable matching. Returning None."
        ):
            self.assertIsNone(iso_from_country_string("zzz"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("abcdef"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("ghijkl"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("mnopqrstu"))
        with pytest.warns(
            UserWarning, match="Input string is too short for reliable matching. Returning None."
        ):
            self.assertIsNone(iso_from_country_string("aaa"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("nonsense"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("gibberish"))
        with pytest.warns(UserWarning, match="No fuzzy matches found. Returning None"):
            self.assertIsNone(iso_from_country_string("fakeplace"))


if __name__ == "__main__":
    unittest.main()
