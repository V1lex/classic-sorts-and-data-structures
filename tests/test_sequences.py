import pytest

from src.sequences import factorial, factorial_recursive, fibo, fibo_recursive


@pytest.mark.parametrize("value,expected", [(0, 1), (1, 1), (5, 120), (7, 5040)])
def test_factorial(value: int, expected: int) -> None:
    assert factorial(value) == expected
    assert factorial_recursive(value) == expected


@pytest.mark.parametrize("value", [-1, -10])
def test_factorial_negative(value: int) -> None:
    with pytest.raises(ValueError):
        factorial(value)
    with pytest.raises(ValueError):
        factorial_recursive(value)


@pytest.mark.parametrize("value,expected", [(0, 0), (1, 1), (2, 1), (10, 55)])
def test_fibonacci(value: int, expected: int) -> None:
    assert fibo(value) == expected
    assert fibo_recursive(value) == expected


def test_fibonacci_negative() -> None:
    with pytest.raises(ValueError):
        fibo_recursive(-5)
    with pytest.raises(ValueError):
        fibo(-3)


def test_sequences_consistency() -> None:
    for value in range(0, 10):
        assert factorial(value) == factorial_recursive(value)
        assert fibo(value) == fibo_recursive(value)
