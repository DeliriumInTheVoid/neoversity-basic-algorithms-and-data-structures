import pytest
from sources.delimiters_checker import check_delimiters

@pytest.mark.parametrize("sequence,expected", [
    ("( ){[ 1 ]( 1 + 3 )( ){ }}", "Симетрично"),
    ("( 23 ( 2 - 3);", "Несиметрично"),
    ("(( 11 })", "Несиметрично"),
    ("", "Симетрично"),  # empty string
    ("[]", "Симетрично"),
    ("[(){}]", "Симетрично"),
    ("([{}])", "Симетрично"),
    ("([)]", "Несиметрично"),
    ("(((())))", "Симетрично"),
    ("(((()))", "Несиметрично"),
    ("{[()]}", "Симетрично"),
    ("{[(])}", "Несиметрично"),
    ("no delimiters", "Симетрично"),
    ("([{}]", "Несиметрично"),
    ("([{}]) extra )", "Несиметрично"),
    ("{[a+b]*(c+d)}", "Симетрично"),
    ("{[a+b]*(c+d)}]", "Несиметрично"),
])
def test_check_delimiters(sequence, expected):
    assert check_delimiters(sequence) == expected

