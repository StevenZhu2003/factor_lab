"""
Primality testing algorithms.

Currently implemented:
- Miller-Rabin probabilistic primality test.
"""

from gmpy2 import mpz, powmod

from factorlab.utils import decompose


"""
Primality testing algorithms.

Currently implemented:
- Miller-Rabin probabilistic primality test.
"""

from gmpy2 import mpz, powmod

from factorlab.utils import decompose


SMALL_PRIMES: tuple[mpz, ...] = tuple(
    mpz(p)
    for p in (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47,
    )
)

MILLER_RABIN_BASES: tuple[mpz, ...] = tuple(
    mpz(p)
    for p in (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61,
    )
)


def is_prime(n: mpz) -> bool:
    """
    Determine whether an integer is prime using the Miller-Rabin primality test.

    Parameters
    ----------
    n : mpz
        Integer to be tested.

    Returns
    -------
    bool
        True if n is probably prime, False if n is definitely composite.
    """

    if n < 2:
        return False

    for p in SMALL_PRIMES:
        if n == p:
            return True
        if n % p == 0:
            return False

    s, d = decompose(n - 1)

    for a in MILLER_RABIN_BASES:
        if a >= n:
            continue

        x = powmod(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = powmod(x, 2, n)

            if x == n - 1:
                break
        else:
            return False

    return True
