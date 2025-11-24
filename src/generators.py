import random


def rand_int_array(n: int, lo: int, hi: int, *, distinct: bool = False, seed: int | None = None) -> list[int]:
    """
    Генерирует массив случайных целых чисел.
    """
    rng = random.Random(seed)
    if distinct:
        if hi - lo + 1 < n:
            raise ValueError("Ошибка: диапазон слишком мал для отдельных значений")
        return rng.sample(range(lo, hi + 1), k=n)
    return [rng.randint(lo, hi) for number in range(n)]


def nearly_sorted(n: int, swaps: int, *, seed: int | None = None) -> list[int]:
    """
    Возвращает почти отсортированный массив: отсортированный список с ограниченным числом swap операций.
    """
    rng = random.Random(seed)
    arr = list(range(n))
    for swap in range(swaps):
        i, j = rng.sample(range(n), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def many_duplicates(n: int, k_unique: int = 5, *, seed: int | None = None) -> list[int]:
    """Генерация массива длины n с ограниченным числом уникальных значений."""
    if k_unique <= 0:
        raise ValueError("Ошибка: k_unique должно быть положительным")
    rng = random.Random(seed)
    pool = [rng.randint(-10 * k_unique, 10 * k_unique) for pool_number in range(k_unique)]
    return [rng.choice(pool) for number in range(n)]


def reverse_sorted(n: int) -> list[int]:
    """Массив длины n, отсортированный по убыванию."""
    return list(range(n, 0, -1))


def rand_float_array(n: int, lo: float = 0.0, hi: float = 1.0, *, seed: int | None = None) -> list[float]:
    """Генерация массива случайных чисел с плавающей точкой."""
    rng = random.Random(seed)
    return [rng.uniform(lo, hi) for number in range(n)]
