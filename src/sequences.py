from functools import lru_cache


def factorial(n: int) -> int:
    """
    Итеративное вычисление n-го факториала.
    """
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")

    result = 1
    for value in range(2, n + 1):
        result *= value
    return result


@lru_cache(maxsize=None)
def factorial_recursive(n: int) -> int:
    """
    Рекурсивное вычисление n-го факториала.
    """
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    if n in (0, 1):
        return 1
    return n * factorial_recursive(n - 1)


def fibo(n: int) -> int:
    """
    Итеративное вычисление n-го числа Фибоначчи.
    Начальные условия: F(0) = 0, F(1) = 1.
    """
    if n < 0:
        raise ValueError("Числа Фибоначчи не определены для отрицательных значений")
    if n == 0:
        return 0
    previous, current = 0, 1
    for _ in range(1, n):
        previous, current = current, previous + current
    return current


@lru_cache(maxsize=None)
def fibo_recursive(n: int) -> int:
    """
    Рекурсивное вычисление n-го числа Фибоначчи с мемоизацией.
    Начальные условия: F(0) = 0, F(1) = 1.
    """
    if n < 0:
        raise ValueError("Числа Фибоначчи не определены для отрицательных значений")
    if n in (0, 1):
        return n
    return fibo_recursive(n - 1) + fibo_recursive(n - 2)
