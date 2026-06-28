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


def pollard_rho_floyd(n: mpz, max_steps = 10_000_000, max_restarts = 64,) -> mpz:
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

def pollard_rho(n: mpz, max_steps: int = 10_000_000, max_restarts: int = 64, batch_size: int = 64,) -> mpz:
    """
    Find a non-trivial factor of n using Brent's Pollard Rho algorithm.

    Parameters
    ----------
    n : mpz
        Integer to be factored.

    max_steps : int, optional
        Maximum number of polynomial evaluations per random walk.

    max_restarts : int, optional
        Maximum number of random restarts.

    batch_size : int, optional
        Number of differences accumulated before computing a GCD.

    Returns
    -------
    mpz
        A non-trivial factor of n. If n is prime, n itself is returned.

    Raises
    ------
    ValueError
        If n < 2 or batch_size < 1.

    RuntimeError
        If no non-trivial factor is found within the given limits.
    """

    if n < 2:
        raise ValueError("n must be at least 2")

    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    if n % 2 == 0:
        return mpz(2)

    if is_prime(n):
        return n

    n_int = int(n)

    for _ in range(max_restarts):
        y = mpz(randrange(2, n_int))
        c = mpz(randrange(1, n_int))

        g = mpz(1)
        r = 1
        q = mpz(1)
        steps = 0

        while g == 1 and steps < max_steps:
            x = y

            for _ in range(r):
                y = _f(y, c, n)
                steps += 1

                if steps >= max_steps:
                    break

            k = 0

            while k < r and g == 1 and steps < max_steps:
                ys = y
                block_size = min(batch_size, r - k)

                for _ in range(block_size):
                    y = _f(y, c, n)
                    q = (q * abs(x - y)) % n
                    steps += 1

                    if steps >= max_steps:
                        break

                g = gcd(q, n)
                k += block_size

            r <<= 1

        if g == n:
            g = mpz(1)

            while g == 1 and steps < max_steps:
                ys = _f(ys, c, n)
                g = gcd(abs(x - ys), n)
                steps += 1

        if 1 < g < n:
            return g

    raise RuntimeError(
        "Brent Pollard Rho failed to find a factor within the given limits"
    )
