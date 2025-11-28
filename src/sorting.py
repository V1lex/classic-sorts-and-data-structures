from typing import Callable, TypeVar

T = TypeVar("T")


def compare(left: T, right: T, key: Callable[[T], object] | None, cmp: Callable[[T, T], int] | None) -> int:
    """
    Возвращает отрицательное значение, если left < right, положительное – если left > right,
    и 0 при равенстве. Приоритет отдается cmp, иначе используется key/identity.
    """
    if cmp is not None:
        return cmp(left, right)
    left_key = key(left) if key else left
    right_key = key(right) if key else right
    return (left_key > right_key) - (left_key < right_key)


def bubble_sort(
    a: list[T],
    key: Callable[[T], object] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]:
    """
    Сортировка пузырьком. Поддерживает произвольные элементы с key или cmp.
    """
    result = a.copy()
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if compare(result[j], result[j + 1], key, cmp) > 0:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def quick_sort(
    a: list[T],
    key: Callable[[T], object] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]:
    """
    Быстрая сортировка (рекурсивная реализация). Поддерживает key и cmp.
    """
    if len(a) <= 1:
        return a.copy()

    pivot = a[len(a) // 2]
    less = [x for x in a if compare(x, pivot, key, cmp) < 0]
    equal = [x for x in a if compare(x, pivot, key, cmp) == 0]
    greater = [x for x in a if compare(x, pivot, key, cmp) > 0]

    return quick_sort(less, key=key, cmp=cmp) + equal + quick_sort(greater, key=key, cmp=cmp)


def counting_sort(
    a: list[T],
    key: Callable[[T], object] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]:
    """
    Сортировка подсчетом, поддерживает отрицательные целые. Поддерживает key и cmp.
    При переданном cmp выполняется сортировка вставками, иначе требуется целочисленный ключ (по умолчанию сам элемент).
    """
    if not a:
        return []

    if cmp is not None:
        result = a.copy()
        for i in range(1, len(result)):
            current = result[i]
            j = i - 1
            while j >= 0 and compare(result[j], current, key, cmp) > 0:
                result[j + 1] = result[j]
                j -= 1
            result[j + 1] = current
        return result

    key_func = key or (lambda x: x)
    keyed_values = [(key_func(value), value) for value in a]

    if any(not isinstance(key_value, int) for key_value, _ in keyed_values):
        raise ValueError("counting_sort работает только с целыми числами или целочисленным key")

    min_value = min(key_value for key_value, original_value in keyed_values)
    max_value = max(key_value for key_value, original_value in keyed_values)
    range_size = max_value - min_value + 1
    counts = [[] for bucket_index in range(range_size)]

    for key_value, original in keyed_values:
        counts[key_value - min_value].append(original)

    result = []
    for bucket in counts:
        result.extend(bucket)
    return result


def radix_sort(
    a: list[T],
    base: int = 10,
    key: Callable[[T], object] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]:
    """
    Поразрядная сортировка целых чисел (base задает систему счисления). Поддерживает key и cmp.
    Числа подаются в десятичной записи, поддерживаются отрицательные значения. При cmp выполняется сортировка вставками.
    """
    if base < 2:
        raise ValueError("Основание должно быть не меньше 2")

    if not a:
        return []

    if cmp is not None:
        result = a.copy()
        for i in range(1, len(result)):
            current = result[i]
            j = i - 1
            while j >= 0 and compare(result[j], current, key, cmp) > 0:
                result[j + 1] = result[j]
                j -= 1
            result[j + 1] = current
        return result

    key_func = key or (lambda x: x)
    keyed_values = [(key_func(value), value) for value in a]

    if any(not isinstance(key_value, int) for key_value, _ in keyed_values):
        raise ValueError("radix_sort принимает только целочисленные значения или key")

    non_negative = [(key_value, value) for key_value, value in keyed_values if key_value >= 0]
    negative = [(-key_value, value) for key_value, value in keyed_values if key_value < 0]

    sorted_non_negative = []
    if non_negative:
        result_pairs = non_negative.copy()
        max_value = max(key_value for key_value, original_value in result_pairs)
        exponent = 1
        while max_value // exponent > 0:
            buckets_non_negative = [[] for bucket in range(base)]
            for key_value, original in result_pairs:
                digit = (key_value // exponent) % base
                buckets_non_negative[digit].append((key_value, original))
            result_pairs = [pair for bucket in buckets_non_negative for pair in bucket]
            exponent *= base
        sorted_non_negative = result_pairs

    sorted_negative = []
    if negative:
        result_pairs = negative.copy()
        max_negative = max(key_value for key_value, original_value in result_pairs)
        exponent = 1
        while max_negative // exponent > 0:
            buckets_negative = [[] for bucket in range(base)]
            for key_value, original in result_pairs:
                digit = (key_value // exponent) % base
                buckets_negative[digit].append((key_value, original))
            result_pairs = [pair for bucket in buckets_negative for pair in bucket]
            exponent *= base
        sorted_negative = result_pairs

    negative_part = [value for key_value, value in reversed(sorted_negative)]
    non_negative_part = [value for key_value, value in sorted_non_negative]
    return negative_part + non_negative_part


def bucket_sort(
    a: list[T],
    buckets: int | None = None,
    key: Callable[[T], object] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]:
    """
    Сортировка с использованием buckets. Поддерживает key и cmp. По умолчанию рассчитана на числа из [0, 1),
    но при необходимости нормализует данные к этому диапазону. При cmp сортирует вставками с использованием компаратора.
    """
    if len(a) < 2:
        return a.copy()

    if cmp is not None:
        result = a.copy()
        for i in range(1, len(result)):
            current = result[i]
            j = i - 1
            while j >= 0 and compare(result[j], current, key, cmp) > 0:
                result[j + 1] = result[j]
                j -= 1
            result[j + 1] = current
        return result

    key_func = key or (lambda x: x)
    key_values = [key_func(value) for value in a]
    if any(not isinstance(key_value, (int, float)) for key_value in key_values):
        raise ValueError("bucket_sort поддерживает только числовые значения или key")

    bucket_count = buckets or max(1, int(len(a) ** 0.5))
    minimum, maximum = min(key_values), max(key_values)

    # Нормализуем значения к [0, 1) если выходят за диапазон.
    range_span = maximum - minimum or 1.0
    normalized = [(key_value - minimum) / range_span for key_value in key_values]

    buckets_storage = [[] for bucket in range(bucket_count)]
    for original_value, norm in zip(a, normalized):
        index = min(bucket_count - 1, int(norm * bucket_count))
        buckets_storage[index].append(original_value)

    result = []
    for bucket in buckets_storage:
        for i in range(1, len(bucket)):
            current_value = bucket[i]
            j = i - 1
            while j >= 0 and compare(bucket[j], current_value, key_func, None) > 0:
                bucket[j + 1] = bucket[j]
                j -= 1
            bucket[j + 1] = current_value
        result.extend(bucket)
    return result


def heap_sort(
    a: list[T],
    key: Callable[[T], object] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]:
    """
    Сортировка кучей (пирамидальная сортировка). Поддерживает key и cmp.
    """
    result = a.copy()
    n = len(result)

    for i in range(n // 2 - 1, -1, -1):
        root = i
        while True:
            child = 2 * root + 1
            if child >= n:
                break
            if child + 1 < n and compare(result[child], result[child + 1], key, cmp) < 0:
                child += 1
            if compare(result[root], result[child], key, cmp) < 0:
                result[root], result[child] = result[child], result[root]
                root = child
            else:
                break

    for i in range(n - 1, 0, -1):
        result[0], result[i] = result[i], result[0]
        root = 0
        while True:
            child = 2 * root + 1
            if child >= i:
                break
            if child + 1 < i and compare(result[child], result[child + 1], key, cmp) < 0:
                child += 1
            if compare(result[root], result[child], key, cmp) < 0:
                result[root], result[child] = result[child], result[root]
                root = child
            else:
                break

    return result
