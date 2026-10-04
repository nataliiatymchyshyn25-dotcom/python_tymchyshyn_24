import unittest

from src.bracket_validator.bracket_validator import validate_brackets


class TestValidateBrackets(unittest.TestCase):

    def test_valid_strings(self):
        valid_strings = [
            "",
            "Hello world",
            "(test)",
            "{test}",
            "<test>",
            "[test]",
            "({<>})",
            "<div>{([test])}</div>"
        ]

        for text in valid_strings:
            with self.subTest(text=text):
                validate_brackets(text)

    def test_extra_closing_bracket(self):
        with self.assertRaises(ValueError) as error:
            validate_brackets("(test))")

        self.assertIn("[6]", str(error.exception))

    def test_unclosed_bracket(self):
        with self.assertRaises(ValueError) as error:
            validate_brackets("((test)")

        self.assertIn("[0]", str(error.exception))

    def test_closing_without_opening(self):
        with self.assertRaises(ValueError) as error:
            validate_brackets(")test")

        self.assertIn("[0]", str(error.exception))

    def test_multiple_extra_closing_brackets(self):
        with self.assertRaises(ValueError) as error:
            validate_brackets("(test)))")

        self.assertIn("[6, 7]", str(error.exception))

    def test_multiple_unclosed_brackets(self):
        with self.assertRaises(ValueError) as error:
            validate_brackets("text({[")

        self.assertIn("[4, 5, 6]", str(error.exception))


if __name__ == "__main__":
    unittest.main()