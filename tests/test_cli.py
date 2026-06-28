"""
Unit tests for the FactorLab command-line interface.
"""

from factorlab.cli import cli


def test_cli_factorisation(capsys) -> None:
    """The CLI should print the complete prime factorisation."""

    exit_code = cli(["360"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Prime factorisation:" in captured.out
    assert "2 × 2 × 2 × 3 × 3 × 5" in captured.out


def test_cli_prime(capsys) -> None:
    """The CLI should correctly print a prime number."""

    exit_code = cli(["97"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Prime factorisation:" in captured.out
    assert "97" in captured.out


def test_cli_verbose(capsys) -> None:
    """Verbose mode should print factorisation progress."""

    exit_code = cli(["15", "--verbose"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "[Factor]" in captured.out
    assert "Prime factorisation:" in captured.out
    assert "3 × 5" in captured.out
