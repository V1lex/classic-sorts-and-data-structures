import pytest

from src.generators import (
    many_duplicates,
    nearly_sorted,
    rand_float_array,
    rand_int_array,
    reverse_sorted,
)


def test_rand_int_array_ranges_and_seed() -> None:
    result = rand_int_array(5, -2, 3, seed=7)
    assert result == [0, -1, 1, 3, -2]
    assert all(-2 <= value <= 3 for value in result)


def test_rand_int_array_distinct_and_validation() -> None:
    result = rand_int_array(4, 1, 10, distinct=True, seed=3)
    assert result == [4, 9, 3, 8]
    assert len(set(result)) == 4
    with pytest.raises(ValueError):
        rand_int_array(5, 1, 3, distinct=True)


def test_nearly_sorted_is_deterministic() -> None:
    result = nearly_sorted(6, 3, seed=2)
    assert result == [2, 5, 1, 3, 4, 0]
    assert sorted(result) == list(range(6))


def test_many_duplicates_pool_and_validation() -> None:
    result = many_duplicates(6, 3, seed=5)
    assert result == [-14, 17, 17, 17, 17, 9]
    assert len(set(result)) <= 3
    with pytest.raises(ValueError):
        many_duplicates(4, 0)


def test_reverse_sorted() -> None:
    assert reverse_sorted(5) == [5, 4, 3, 2, 1]


def test_rand_float_array_ranges_and_seed() -> None:
    result = rand_float_array(3, 0.0, 1.0, seed=11)
    assert result == [0.4523795535098186, 0.559772386080496, 0.9242105840237294]
    assert all(0.0 <= value <= 1.0 for value in result)
