from src.benchmark import benchmark_sorts, timeit_once
from src.sorting import bubble_sort


def test_benchmark_runs_and_timeit_once() -> None:
    arr = [3, 1, 2]
    time = timeit_once(bubble_sort, arr.copy())
    assert time >= 0

    report = benchmark_sorts({"sample": arr}, {"bubble": bubble_sort}, runs=2)
    assert "sample" in report
    assert "bubble" in report["sample"]
    assert report["sample"]["bubble"] >= 0
