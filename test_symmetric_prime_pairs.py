import pytest

from symmetric_prime_pairs import is_prime, symmetric_prime_pair


def test_is_prime():
    assert [n for n in range(30) if is_prime(n)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


@pytest.mark.parametrize("even,pair", [(4, (2, 2)), (6, (3, 3)), (8, (3, 5)), (10, (5, 5)),
                                       (100, (47, 53)), (1000, (491, 509))])
def test_known_pairs(even, pair):
    assert symmetric_prime_pair(even) == pair


def test_every_even_number_up_to_10000():
    for even in range(4, 10001, 2):
        L, R = symmetric_prime_pair(even)
        assert L + R == even and is_prime(L) and is_prime(R) and L <= R


@pytest.mark.parametrize("bad", [2, 0, -4, 7])
def test_rejects_invalid_input(bad):
    with pytest.raises(ValueError):
        symmetric_prime_pair(bad)
