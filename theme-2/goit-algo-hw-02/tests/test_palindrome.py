import pytest
from sources.palindrome import is_palindrome

@pytest.mark.parametrize("test_input,expected", [
    ("A man, a plan, a canal: Panama", True),
    ("racecar", True),
    ("No lemon, no melon", True),
    ("Was it a car or a cat I saw?", True),
    ("hello", False),
    ("Python", False),
    ("", True),  # empty string is a palindrome
    ("a", True), # single character is a palindrome
    ("12321", True),
    ("12345", False),
    ("Able was I ere I saw Elba", True),
    ("Madam In Eden, I'm Adam", True),
    ("Not a palindrome", False),
    ("!@#$$#@!", True), # only special characters, cleaned to empty
    ("1a2", False),
])
def test_is_palindrome(test_input, expected):
    assert is_palindrome(test_input) == expected
