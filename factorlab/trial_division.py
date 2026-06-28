"""
Trial Division

This module implements trial division using a precomputed table of prime
numbers.

Trial division is the first stage of the factorisation pipeline. It
efficiently removes small prime factors before more expensive algorithms
such as Pollard's Rho or ECM are invoked.

The module returns both the factors discovered by trial division and the
remaining unfactored cofactor.
"""

from gmpy2 import mpz

from factorlab.primes import PRIMES


def trial_division(
    n: mpz,
    limit: int | None = None,
) -> tuple[list[mpz], mpz]:
    """
    Remove small prime factors from an integer using trial division.

    Parameters
    ----------
    n : mpz
        Integer to be factorised.

    limit : int, optional
        Largest prime to test. If omitted, the entire precomputed prime
        table is used.

    Returns
    -------
    tuple[list[mpz], mpz]
        A tuple consisting of

        - the list of prime factors found by trial division;
        - the remaining cofactor.
    """

    factors: list[mpz] = []

    for p in PRIMES:

        if limit is not None and p > limit:
            break

        if mpz(p) * p > n:
            break

        while n % p == 0:
            factors.append(mpz(p))
            n //= p

    return factors, n
