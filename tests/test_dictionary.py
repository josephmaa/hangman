import unittest

from lib.parser import parse_dictionary


class TestDictionaryParsing(unittest.TestCase):
    def test_dictionary_parsing_keys_match(self):
        dictionary_input = "media/dictionary.txt"
        parsed = parse_dictionary(dictionary_input)
        keys = [
            0,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            24,
            28,
            29,
        ]
        self.assertEqual(sorted(parsed.keys()), keys)


if __name__ == "__main__":
    unittest.main()
