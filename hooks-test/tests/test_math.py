from src.math_utils import add_numbers, multiply


def test_add_numbers():
    assert add_numbers(2, 3) == 5


def test_multiply():
    assert multiply(3, 4) == 12


def test_add_negative():
    assert add_numbers(-1, 1) == 0


def test_deliberate_failure():
    """This test should fail to trigger the PostToolUseFailure hook."""
    assert add_numbers(1, 1) == 3
