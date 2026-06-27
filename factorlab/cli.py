"""
Command-line interface for FactorLab.

This module provides the command-line entry point for the FactorLab
library.

Users can invoke FactorLab directly from the terminal to perform prime
factorisation without writing any Python code. The command-line interface
parses the input integer, executes the recursive factorisation routine,
and displays the resulting prime factors in a human-readable format.

Future versions may support additional options such as verbose logging,
algorithm selection, structured output formats (e.g. JSON), and
performance statistics.
"""

import argparse
import logging

from gmpy2 import mpz

from factorlab.factor import factor

def cli() -> int:
    """
    Command-line entry point.
    """

    parser = argparse.ArgumentParser(
        prog="factorlab",
        description="Prime factorisation using FactorLab.",
    )

    parser.add_argument(
        "integer",
        type=mpz,
        help="Positive integer to be factorised.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
        )

    factors = factor(args.integer)

    print("\nPrime factorisation:\n")
    print(" × ".join(map(str, factors)))

    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
