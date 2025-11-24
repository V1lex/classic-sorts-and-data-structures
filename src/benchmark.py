import time
from typing import Callable


def timeit_once(func: Callable, *args, **kwargs) -> float:
    """
    Измеряет время выполнения функции.
    """
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    return end - start


def benchmark_sorts(
    arrays: dict[str, list],
    algos: dict[str, Callable[[list], list]],
    runs: int = 1,
) -> dict[str, dict[str, float]]:
    """
    Бенчмарк выбранных алгоритмов сортировки на наборе входных массивов.
    """
    if runs < 1:
        raise ValueError("runs должно быть не меньше 1")

    results = {}
    for array_name, array_values in arrays.items():
        results[array_name] = {}
        for algo_name, algo in algos.items():
            total = 0.0
            for run in range(runs):
                # Копируем вход, чтобы алгоритм не изменил исходные данные.
                total += timeit_once(algo, array_values.copy())
            results[array_name][algo_name] = total / runs
    return results
