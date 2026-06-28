"""
Benchmark for Pollard's Rho implementation.

This script measures the practical performance of FactorLab's Pollard's
Rho implementation on randomly generated semiprimes.

For each smallest-factor size, several random semiprimes are generated.
The benchmark records the average runtime and success rate, providing
an estimate of the algorithm's practical capability.

This benchmark is intended for performance comparison between different
implementations (e.g. Floyd vs Brent), parameter tuning, and regression
testing.
"""

"""
Benchmark for Pollard's Rho implementation.

This script evaluates the practical performance of FactorLab's Pollard's
Rho implementation on randomly generated semiprimes.

For each benchmark case, a semiprime is generated from two random prime
numbers. The benchmark records the success rate and execution time,
allowing different implementations and parameter choices to be compared
objectively.
"""

from random import randrange, seed
from statistics import mean, median
from time import perf_counter

from gmpy2 import mpz

from factorlab.pollard_rho import pollard_rho
from factorlab.primality import is_prime


# ----------------------------------------------------------------------
# Benchmark configuration
# ----------------------------------------------------------------------

MIN_FACTOR_DIGITS = 10
MAX_FACTOR_DIGITS = 16

LARGE_FACTOR_DIGITS = 30

TRIALS = 20

RANDOM_SEED = 42

MAX_STEPS = 50_000_000
MAX_RESTARTS = 16


seed(RANDOM_SEED)

def random_prime(digits: int) -> mpz:
    """
    Generate a random prime number with a specified number of decimal digits.

    Parameters
    ----------
    digits : int
        Number of decimal digits.

    Returns
    -------
    mpz
        A random prime number.
    """

    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1

    while True:
        candidate = mpz(randrange(lower, upper))

        # Ensure the candidate is odd.
        candidate |= 1

        if is_prime(candidate):
            return candidate
        
def random_semiprime(
    small_digits: int,
    large_digits: int,
) -> tuple[mpz, mpz, mpz]:
    """
    Generate a random semiprime.

    Parameters
    ----------
    small_digits : int
        Number of digits of the smaller prime factor.

    large_digits : int
        Number of digits of the larger prime factor.

    Returns
    -------
    tuple[mpz, mpz, mpz]
        The semiprime and its two prime factors.

        (n, p, q)
    """

    p = random_prime(small_digits)

    while True:
        q = random_prime(large_digits)

        if q != p:
            break

    return p * q, p, q

def main() -> None:
    """
    Benchmark Pollard's Rho on random semiprimes.
    """

    print()
    print("Pollard's Rho Benchmark")
    print("=" * 72)
    print()

    print(
        f"{'Digits':>6}"
        f"{'Success':>10}"
        f"{'Average (s)':>15}"
        f"{'Median (s)':>15}"
        f"{'Maximum (s)':>15}"
    )

    print("-" * 72)

    for digits in range(MIN_FACTOR_DIGITS, MAX_FACTOR_DIGITS + 1):

        times: list[float] = []
        success = 0

        for _ in range(TRIALS):

            n, p, q = random_semiprime(
                digits,
                LARGE_FACTOR_DIGITS,
            )

            start = perf_counter()

            try:
                factor = pollard_rho(
                    n,
                    max_steps=MAX_STEPS,
                    max_restarts=MAX_RESTARTS,
                )

                elapsed = perf_counter() - start

                if factor in (p, q):
                    success += 1
                    times.append(elapsed)

            except RuntimeError:
                pass

        if times:

            avg = mean(times)
            med = median(times)
            worst = max(times)

            print(
                f"{digits:>6}"
                f"{success:>8}/{TRIALS:<2}"
                f"{avg:>15.4f}"
                f"{med:>15.4f}"
                f"{worst:>15.4f}"
            )

        else:

            print(
                f"{digits:>6}"
                f"{0:>8}/{TRIALS:<2}"
                f"{'-':>15}"
                f"{'-':>15}"
                f"{'-':>15}"
            )

    print()


if __name__ == "__main__":
    main()
