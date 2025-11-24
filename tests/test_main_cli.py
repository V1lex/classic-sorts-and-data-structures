import pytest
from typer.testing import CliRunner

from src.main import app
from src.sorting import bubble_sort


runner = CliRunner()


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

def test_cli_sort_commands() -> None:
    int_values = ["3", "1", "2"]
    float_values = ["0.5", "0.25", "0.75"]

    for command in ("bubble", "quick", "heap", "counting", "radix"):
        result = runner.invoke(app, [command, *int_values])
        assert result.exit_code == 0
        assert "[1, 2, 3]" in result.stdout

    bucket_result = runner.invoke(app, ["bucket", *float_values])
    assert bucket_result.exit_code == 0
    assert "[0.25, 0.5, 0.75]" in bucket_result.stdout


def test_cli_sequences() -> None:
    assert runner.invoke(app, ["factorial", "5"]).stdout.strip() == "120"
    assert runner.invoke(app, ["factorial-rec", "5"]).stdout.strip() == "120"
    assert runner.invoke(app, ["fibo", "7"]).stdout.strip() == "13"
    assert runner.invoke(app, ["fibo-rec", "7"]).stdout.strip() == "13"


def test_cli_stack_and_queue_demos() -> None:
    stack_result = runner.invoke(app, ["stack-demo", "5", "2"])
    assert stack_result.exit_code == 0
    assert "верх=2" in stack_result.stdout
    assert "pop -> 2" in stack_result.stdout

    queue_result = runner.invoke(app, ["queue-demo", "1", "4"])
    assert queue_result.exit_code == 0
    assert "первый=1" in queue_result.stdout
    assert "dequeue -> 1" in queue_result.stdout


def test_cli_benchmark_command() -> None:
    result = runner.invoke(app, ["benchmark", "5", "2", "3", "--runs", "5"])
    assert result.exit_code == 0
    assert "custom (n=3)" in result.stdout
    for key in ("bubble:", "quick:", "heap:", "counting:", "radix:", "bucket:"):
        assert key in result.stdout
    assert "runs=5" in result.stdout
    assert "среднее" in result.stdout


def test_interactive_session_help_and_quit() -> None:
    user_input = "help\nquit\n"
    result = runner.invoke(app, ["interactive"], input=user_input)
    assert result.exit_code == 0
    assert "Доступные команды" in result.stdout
    assert "Выход из интерактивного режима." in result.stdout


def test_cli_validation_errors() -> None:
    bad_counting = runner.invoke(app, ["counting", "1", "2.5"])
    assert bad_counting.exit_code != 0

    bad_radix = runner.invoke(app, ["radix", "1", "base", "10"])
    assert bad_radix.exit_code != 0


def test_interactive_commands_flow() -> None:
    commands = "\n".join(
        [
            "",
            "factorial 3",
            "counting 3 1",
            "radix 2 1 base=2",
            "stack_push 5",
            "stack_peek",
            "stack_min",
            "queue_enqueue 7",
            "queue_front",
            "queue_dequeue",
            "benchmark 1 2 runs=2",
            "unknown",
            "quit",
        ]
    )
    result = runner.invoke(app, ["interactive"], input=commands + "\n")
    assert result.exit_code == 0
    assert "6" in result.stdout
    assert "[1, 3]" in result.stdout
    assert "[1, 2]" in result.stdout
    assert "peek -> 5" in result.stdout
    assert "min -> 5" in result.stdout
    assert "front -> 7" in result.stdout
    assert "runs=2" in result.stdout
    assert "среднее" in result.stdout
    assert "Неизвестная команда" in result.stdout


def test_argument_parsers_errors() -> None:
    from typer import BadParameter
    from src.main import numbers_argument, parse_numbers

    with pytest.raises(ValueError):
        parse_numbers([])
    with pytest.raises(BadParameter):
        numbers_argument([])


def test_no_command_runs_interactive() -> None:
    result = runner.invoke(app, input="quit\n")
    assert result.exit_code == 0


def test_benchmark_invalid_runs() -> None:
    from src.benchmark import benchmark_sorts

    with pytest.raises(ValueError):
        benchmark_sorts({"a": [1, 2]}, {"bubble": bubble_sort}, runs=0)
