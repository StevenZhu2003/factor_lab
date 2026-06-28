"""
Pollard's Rho Integer Factorisation Algorithm

This module implements Pollard's Rho algorithm for finding a non-trivial
factor of a composite integer.

Pollard's Rho is a probabilistic factorisation algorithm proposed by
John Pollard in 1975. It performs a pseudo-random walk over the finite
field modulo n and detects cycles using Floyd's cycle-finding algorithm.
Whenever two iterates become congruent modulo an unknown prime factor,
the greatest common divisor (GCD) of their difference and n reveals
a non-trivial factor.

This implementation is intended for educational purposes. The focus is
on clarity and readability rather than absolute performance.
"""

from random import randrange
from gmpy2 import gcd, mpz

from factorlab.primality import is_prime

def _f(x: mpz, c: mpz, n: mpz) -> mpz:
    """
    Polynomial used for the pseudo-random walk.

    The function is defined as

        f(x) = x² + c (mod n)

    where c is a non-zero constant.

    Parameters
    ----------
    x : mpz
        Current position.

    c : mpz
        Polynomial constant.

    n : mpz
        Modulus.

    Returns
    -------
    mpz
        Next position in the pseudo-random walk.
    """

    return (x * x + c) % n


def pollard_rho(n: mpz, max_steps = 10_000_000, max_restarts = 64,) -> mpz:
    """
    Find a non-trivial factor of n using Pollard's Rho algorithm.

    Parameters
    ----------
    n : mpz
        Integer to be factored.

    max_steps : int, optional
        Maximum number of Floyd iterations per random walk.

    max_restarts : int, optional
        Maximum number of random restarts.

    Returns
    -------
    mpz
        A non-trivial factor of n. If n is prime, n itself is returned.

    Raises
    ------
    ValueError
        If n < 2.

    RuntimeError
        If no non-trivial factor is found within the given limits.
    """

    if n < 2:
        raise ValueError("n must be at least 2")

    if n % 2 == 0:
        return mpz(2)

    if is_prime(n):
        return n

    n_int = int(n)

    for _ in range(max_restarts):
        x = mpz(randrange(2, n_int))
        y = x
        c = mpz(randrange(1, n_int))

        d = mpz(1)

        for _ in range(max_steps):
            x = _f(x, c, n)
            y = _f(_f(y, c, n), c, n)

            d = gcd(abs(x - y), n)

            if d == n:
                break

            if d > 1:
                return d

    raise RuntimeError(
        "Pollard Rho failed to find a factor within the given limits"
    )
