import typer

from src.benchmark import timeit_once
from src.data_structures import Queue, Stack
from src.generators import (
    many_duplicates,
    nearly_sorted,
    rand_float_array,
    rand_int_array,
    reverse_sorted,
)
from src.sequences import factorial, factorial_recursive, fibo, fibo_recursive
from src.sorting import (
    bubble_sort,
    bucket_sort,
    counting_sort,
    heap_sort,
    quick_sort,
    radix_sort,
)

app = typer.Typer(help="Алгоритмический мини-пакет: последовательности, сортировки и структуры данных.")

INTERACTIVE_COMMANDS = {
    "help": "help - показать список доступных команд.",
    "quit": "quit - выйти из интерактивного режима.",
    "factorial": "factorial <n> - факториал числа n.",
    "factorial_rec": "factorial_recursive <n> - рекурсивный факториал числа n.",
    "fibo": "fibo <n> - n-е число Фибоначчи.",
    "fibo_rec": "fibo_recursive <n> - рекурсивное n-е число Фибоначчи.",
    "bubble": "bubble <числа> - сортировка пузырьком.",
    "quick": "quick <числа> - быстрая сортировка.",
    "counting": "counting <целые> - сортировка подсчетом.",
    "radix": "radix <целые> [base=<b>] - поразрядная сортировка с основанием b.",
    "bucket": "bucket <числа> - сортировка корзинами с нормализацией.",
    "heap": "heap <числа> - пирамидальная сортировка.",
    "stack_push": "stack_push <значение> - добавить значение в стек.",
    "stack_pop": "stack_pop - извлечь верх из стека.",
    "stack_peek": "stack_peek - посмотреть верх стека.",
    "stack_min": "stack_min - минимум в стеке.",
    "queue_enqueue": "queue_enqueue <значение> - добавить в очередь.",
    "queue_dequeue": "queue_dequeue - извлечь из очереди.",
    "queue_front": "queue_front - посмотреть первый элемент очереди.",
    "benchmark": "benchmark [числа] - замеры bubble/quick/heap/counting/radix/bucket, секунды суммарно (runs=100000 по умолчанию).",
}


@app.callback(invoke_without_command=True)
def entrypoint(ctx: typer.Context) -> None:
    """
    Точка входа. Без аргументов запускает интерактивный режим.
    """
    if ctx.invoked_subcommand is None:
        interactive_session()


def parse_single_number(token: str) -> int | float:
    value = float(token)
    return int(value) if value.is_integer() else value


def parse_numbers(tokens: list[str]) -> list[int | float]:
    if not tokens:
        raise ValueError("Нужно передать хотя бы одно число.")
    return [parse_single_number(token) for token in tokens]


def parse_ints(tokens: list[str]) -> list[int]:
    numbers = parse_numbers(tokens)
    ints: list[int] = []
    for number in numbers:
        if not isinstance(number, int):
            raise ValueError("Ожидались только целые числа.")
        ints.append(number)
    return ints


def format_value(value: object) -> str:
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        text = f"{value:.10f}".rstrip("0").rstrip(".")
        return text if text else "0"
    if isinstance(value, tuple):
        return "(" + ", ".join(format_value(part) for part in value) + ")"
    if isinstance(value, list):
        return format_sequence(value)
    return str(value)


def format_sequence(values: list[object]) -> str:
    return "[" + ", ".join(format_value(value) for value in values) + "]"


ALGOS = {
    "bubble": bubble_sort,
    "quick": quick_sort,
    "heap": heap_sort,
    "counting": counting_sort,
    "radix": radix_sort,
    "bucket": bucket_sort,
}


def benchmark_lines(arrays: dict[str, list[object]], runs: int) -> list[str]:
    lines = [f"runs={runs}, единицы: секунды (суммарно)"]
    totals_per_algo: dict[str, float] = {name: 0.0 for name in ALGOS}
    counts_per_algo: dict[str, int] = {name: 0 for name in ALGOS}
    for name, array in arrays.items():
        lines.append("")
        lines.append(f"{name} (n={len(array)}):")
        for algo_name, algo in ALGOS.items():
            total = 0.0
            try:
                for _ in range(runs):
                    total += timeit_once(algo, array.copy())
                totals_per_algo[algo_name] += total
                counts_per_algo[algo_name] += 1
                lines.append(f"  {algo_name}: {format_value(total)} s")
            except Exception as exc:
                lines.append(f"  {algo_name}: не поддерживается ({exc})")
    lines.append("")
    lines.append("среднее время:")
    for algo_name in ALGOS:
        if counts_per_algo[algo_name]:
            average = totals_per_algo[algo_name] / counts_per_algo[algo_name]
            lines.append(f"  {algo_name}: {format_value(average)} s")
        else:
            lines.append(f"  {algo_name}: нет поддерживаемых наборов")
    return lines


def build_benchmark_inputs(custom: list[int] | None) -> dict[str, list[object]]:
    if custom is not None:
        return {"custom": custom}
    size = 20
    return {
        "rand_int_array": rand_int_array(size, -50, 50, seed=7),
        "nearly_sorted": nearly_sorted(size, swaps=3, seed=1),
        "many_duplicates": many_duplicates(size, k_unique=5, seed=2),
        "reverse_sorted": reverse_sorted(size),
        "rand_float_array": rand_float_array(size, seed=3),
    }


def build_benchmark_report(custom: list[int] | None, runs: int) -> str:
    arrays = build_benchmark_inputs(custom)
    return "\n".join(benchmark_lines(arrays, runs))


def print_commands() -> None:
    typer.echo("Доступные команды:")
    for name, description in INTERACTIVE_COMMANDS.items():
        typer.echo(f"  {name:<15} {description}")


@app.command("interactive")
def interactive_session() -> None:
    """
    Запускает интерактивную сессию с командами сортировок, последовательностей и структур данных.
    """
    stack = Stack()
    queue = Queue()
    typer.echo("Интерактивный режим. Введите help для списка команд, quit/exit для выхода.")
    while True:
        user_input = typer.prompt("cmd").strip()
        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command in {"quit", "exit"}:
            typer.echo("Выход из интерактивного режима.")
            break
        if command == "help":
            print_commands()
            continue

        try:
            if command == "factorial":
                typer.echo(factorial(int(args[0])))
            elif command == "factorial_rec":
                typer.echo(factorial_recursive(int(args[0])))
            elif command == "fibo":
                typer.echo(fibo(int(args[0])))
            elif command == "fibo_rec":
                typer.echo(fibo_recursive(int(args[0])))
            elif command == "bubble":
                values = parse_numbers(args)
                typer.echo(format_sequence(bubble_sort(values)))
            elif command == "quick":
                values = parse_numbers(args)
                typer.echo(format_sequence(quick_sort(values)))
            elif command == "counting":
                values = parse_ints(args)
                typer.echo(format_sequence(counting_sort(values)))
            elif command == "radix":
                base = 10
                if args and args[-1].startswith("base="):
                    base = int(args.pop().split("=", maxsplit=1)[1])
                values = parse_ints(args)
                typer.echo(format_sequence(radix_sort(values, base=base)))
            elif command == "bucket":
                values = parse_numbers(args)
                typer.echo(format_sequence(bucket_sort(values)))
            elif command == "heap":
                values = parse_numbers(args)
                typer.echo(format_sequence(heap_sort(values)))
            elif command == "stack_push":
                value = parse_ints([args[0]])[0]
                stack.push(value)
                typer.echo(f"В стеке {len(stack)} элементов. Верхний: {stack.peek()}")
            elif command == "stack_pop":
                typer.echo(f"pop -> {stack.pop()}")
            elif command == "stack_peek":
                typer.echo(f"peek -> {stack.peek()}")
            elif command == "stack_min":
                typer.echo(f"min -> {stack.min()}")
            elif command == "queue_enqueue":
                value = parse_ints([args[0]])[0]
                queue.enqueue(value)
                typer.echo(f"В очереди {len(queue)} элементов. Первый: {queue.front()}")
            elif command == "queue_dequeue":
                typer.echo(f"dequeue -> {queue.dequeue()}")
            elif command == "queue_front":
                typer.echo(f"front -> {queue.front()}")
            elif command == "benchmark":
                runs = 100000
                if args and args[-1].startswith("runs="):
                    runs = int(args.pop().split("=", maxsplit=1)[1])
                numbers = parse_ints(args) if args else None
                typer.echo(build_benchmark_report(numbers, runs))
            else:
                typer.echo(f"Неизвестная команда: {command}. Введите help для списка.")
        except Exception as exc:
            typer.echo(f"Ошибка: {exc}")


def numbers_argument(values: list[str]) -> list[int | float]:
    try:
        return parse_numbers(values)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


def int_argument(values: list[str]) -> list[int]:
    try:
        return parse_ints(values)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


@app.command("bubble")
def bubble_cmd(values: list[str] = typer.Argument(..., help="Числа через пробел")) -> None:
    typer.echo(format_sequence(bubble_sort(numbers_argument(values))))


@app.command("quick")
def quick_cmd(values: list[str] = typer.Argument(..., help="Числа через пробел")) -> None:
    typer.echo(format_sequence(quick_sort(numbers_argument(values))))


@app.command("counting")
def counting_cmd(values: list[str] = typer.Argument(..., help="Целые числа через пробел")) -> None:
    typer.echo(format_sequence(counting_sort(int_argument(values))))


@app.command("radix")
def radix_cmd(
    values: list[str] = typer.Argument(..., help="Целые числа через пробел"),
    base: int = typer.Option(10, min=2, help="Основание системы счисления"),
) -> None:
    typer.echo(format_sequence(radix_sort(int_argument(values), base=base)))


@app.command("bucket")
def bucket_cmd(
    values: list[str] = typer.Argument(..., help="Числа через пробел"),
    buckets: int | None = typer.Option(None, min=1, help="Количество корзин"),
) -> None:
    typer.echo(format_sequence(bucket_sort(numbers_argument(values), buckets=buckets)))


@app.command("heap")
def heap_cmd(values: list[str] = typer.Argument(..., help="Числа через пробел")) -> None:
    typer.echo(format_sequence(heap_sort(numbers_argument(values))))


@app.command("factorial")
def factorial_cmd(n: int = typer.Argument(..., help="Натуральное число")) -> None:
    typer.echo(factorial(n))


@app.command("factorial-rec")
def factorial_rec_cmd(n: int = typer.Argument(..., help="Натуральное число")) -> None:
    typer.echo(factorial_recursive(n))


@app.command("fibo")
def fibo_cmd(n: int = typer.Argument(..., help="Номер числа Фибоначчи")) -> None:
    typer.echo(fibo(n))


@app.command("fibo-rec")
def fibo_rec_cmd(n: int = typer.Argument(..., help="Номер числа Фибоначчи")) -> None:
    typer.echo(fibo_recursive(n))


@app.command("stack-demo")
def stack_demo(values: list[int] = typer.Argument([3, 1, 4], help="Числа для последовательных push")) -> None:
    stack = Stack()
    for value in values:
        stack.push(value)
    typer.echo(f"Стек после push: размер={len(stack)}, верх={stack.peek()}, min={stack.min()}")
    popped = stack.pop()
    typer.echo(f"pop -> {popped}; новый размер={len(stack)}; новый min={stack.min() if not stack.is_empty() else 'n/a'}")


@app.command("queue-demo")
def queue_demo(values: list[int] = typer.Argument([1, 2, 3], help="Числа для последовательных enqueue")) -> None:
    queue = Queue()
    for value in values:
        queue.enqueue(value)
    typer.echo(f"Очередь: размер={len(queue)}, первый={queue.front()}")
    dequeued = queue.dequeue()
    typer.echo(f"dequeue -> {dequeued}; новый размер={len(queue)}; первый={queue.front() if not queue.is_empty() else 'n/a'}")


@app.command("benchmark")
def benchmark_cmd(
    values: list[str] = typer.Argument(
        None,
        help="Необязательно: свои числа для замера. Если пусто — используется набор генераторов.",
    ),
    runs: int = typer.Option(100000, min=1, help="Сколько раз повторить каждую сортировку"),
) -> None:
    numbers = int_argument(values) if values else None
    report = build_benchmark_report(numbers, runs)
    typer.echo(report)


if __name__ == "__main__":
    app()  # pragma: no cover
