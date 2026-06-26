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

def pollard_rho(n: mpz) -> mpz:
    """
    Find a non-trivial factor of an odd composite integer using
    Pollard's Rho algorithm.

    Pollard's Rho performs a pseudo-random walk over the integers
    modulo n using the polynomial

        f(x) = x² + c (mod n)

    Two walkers are advanced using Floyd's cycle-finding algorithm.
    Whenever

        gcd(|x - y|, n)

    becomes greater than one, a non-trivial factor has been found.

    Since the algorithm is probabilistic, a single run may fail.
    In that case the random walk is restarted with different initial
    parameters until a factor is discovered.

    Parameters
    ----------
    n : mpz
        Odd composite integer to be factored.

    Returns
    -------
    mpz
        A non-trivial factor of n.

    Raises
    ------
    ValueError
        If n < 2.

    Notes
    -----
    This implementation uses Floyd's tortoise-and-hare cycle
    detection algorithm.

    The expected running time is approximately

        O(n^(1/4))

    for integers having two similarly-sized prime factors.
    """

    if n < 2:
        raise ValueError("n must be at least 2")

    if n % 2 == 0:
        return mpz(2)

    if is_prime(n):
        return n

    while True:

        # Random starting point
        x = ...
        y = ...
        c = ...

        d = mpz(1)

        while d == 1:

            x = _f(x, c, n)
            y = _f(_f(y, c, n), c, n)

            d = gcd(abs(x - y), n)

        if d != n:
            return d
