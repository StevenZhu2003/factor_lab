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
    raise NotImplementedError
