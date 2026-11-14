"""Symmetric prime pairs: write an even number 2n as L + R with two primes L and R that lie
symmetrically around n, i.e. L = n - d and R = n + d.

This is Goldbach's conjecture (every even number greater than 2 is the sum of two primes),
searched from the middle outwards, so the pair found is the one with the smallest distance d.

    $ python symmetric_prime_pairs.py 100
    n (half of the input) = 50
    Symmetric prime pair found: L = 47, R = 53 (d = 3)
    Verification: L + R = 100 = 2 * 50
"""
import sys


def is_prime(num):
    """Determine whether a given number is prime.

    Parameters:
        num (int): The number to be tested for primality.

    Returns:
        bool: True if num is prime, False otherwise.
    """
    if num < 2:
        return False
    if num % 2 == 0:
        return num == 2
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True


def symmetric_prime_pair(even_number):
    """Return (L, R) with L + R = even_number, both prime, closest to even_number / 2.

    Raises ValueError for odd numbers and for numbers below 4."""
    if even_number % 2 != 0 or even_number < 4:
        raise ValueError("the number must be even and at least 4")
    n = even_number // 2
    d = 0
    while n - d >= 2:
        if is_prime(n - d) and is_prime(n + d):
            return n - d, n + d
        d += 1
    raise RuntimeError(f"no pair found for {even_number} - a counterexample to Goldbach!")


def ask_even_number():
    """Prompt until the user enters an even number of at least 4."""
    while True:
        try:
            value = int(input("Please enter an even number (at least 4): "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue
        if value % 2 == 0 and value >= 4:
            return value
        print("The number must be even and at least 4. Try again.")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    even_number = int(argv[0]) if argv else ask_even_number()
    n = even_number // 2
    L, R = symmetric_prime_pair(even_number)
    print(f"n (half of the input) = {n}")
    print(f"Symmetric prime pair found: L = {L}, R = {R} (d = {n - L})")
    print(f"Verification: L + R = {L + R} = 2 * {n}")


if __name__ == "__main__":
    main()
