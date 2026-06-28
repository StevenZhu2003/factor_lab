from random import choices

from gmpy2 import mpz

from factorlab.factor import factor

PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97,
]


def test_random_products() -> None:
    """Random products of small primes should factor correctly."""

    for _ in range(100):

        primes = choices(PRIMES, k=5)

        n = mpz(1)

        for p in primes:
            n *= p

        assert factor(n) == sorted(map(mpz, primes))
