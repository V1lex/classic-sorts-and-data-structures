from functools import cmp_to_key
import pytest

from src.sorting import (
    bubble_sort,
    bucket_sort,
    counting_sort,
    heap_sort,
    quick_sort,
    radix_sort,
)


def assert_sorted(func, data):
    original = data.copy()
    result = func(original)
    assert result == sorted(original)
    assert original == data  # убеждаемся, что исходный список не изменился


def test_basic_sorts() -> None:
    data = [5, -2, 9, 0, 3, 3, -2]
    for sorter in (bubble_sort, quick_sort, counting_sort, heap_sort, radix_sort):
        assert_sorted(sorter, data)


def test_sorting_with_floats() -> None:
    floats = [2.5, -1.0, 3.3, 2.5, 0.0]
    for sorter in (bubble_sort, quick_sort):
        assert_sorted(sorter, floats)


def test_sorts_with_key() -> None:
    words = ["bbb", "a", "dddd", "cc"]
    expected = sorted(words, key=len)
    for sorter in (bubble_sort, quick_sort, counting_sort, radix_sort, heap_sort, bucket_sort):
        assert sorter(words, key=len) == expected


def test_sorts_with_cmp() -> None:
    data = [5, -2, 9, 0, 3]

    def reverse_cmp(left: int, right: int) -> int:
        return (right > left) - (right < left)

    expected = sorted(data, key=cmp_to_key(reverse_cmp))
    for sorter in (bubble_sort, quick_sort, counting_sort, radix_sort, bucket_sort, heap_sort):
        assert sorter(data, cmp=reverse_cmp) == expected


def test_radix_with_base() -> None:
    data = [10, -1, 0, 5, 3, -9]
    assert radix_sort(data, base=2) == sorted(data)


def test_counting_sort_empty() -> None:
    assert counting_sort([]) == []


def test_bucket_sort_empty() -> None:
    assert bucket_sort([]) == []


def test_bucket_sort_normalizes() -> None:
    floats = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]
    assert bucket_sort(floats) == sorted(floats)

    outside_range = [5.0, -3.0, 1.0, 0.0]
    assert bucket_sort(outside_range) == sorted(outside_range)


def test_heap_sort_single_element() -> None:
    assert heap_sort([1]) == [1]


def test_radix_sort_validation() -> None:
    with pytest.raises(ValueError):
        radix_sort([1, 2, 3], base=1)
    with pytest.raises(ValueError):
        radix_sort([1, 2.5, 3])


def test_radix_sort_empty() -> None:
    assert radix_sort([]) == []


def test_bucket_sort_non_numeric_raises() -> None:
    with pytest.raises(ValueError):
        bucket_sort(["a", "b"])


def test_counting_sort_validation() -> None:
    with pytest.raises(ValueError):
        counting_sort([1, 2.5, 3])
