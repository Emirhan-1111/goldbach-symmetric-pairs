# goldbach-symmetric-pairs

[![tests](https://github.com/Emirhan-1111/goldbach-symmetric-pairs/actions/workflows/tests.yml/badge.svg)](https://github.com/Emirhan-1111/goldbach-symmetric-pairs/actions/workflows/tests.yml)

**Symmetric prime pairs and the expression of even numbers — an experimental approach to
Goldbach's conjecture.**

For an even number `2n`, find two primes `L` and `R` that lie symmetrically around `n`:

```
L = n − d,   R = n + d,   L + R = 2n
```

```
$ python symmetric_prime_pairs.py 28
n (half of the input) = 14
Symmetric prime pair found: L = 11, R = 17 (d = 3)
Verification: L + R = 28 = 2 * 14
```

📄 **Paper:** [Symmetric Prime Pairs and the Expression of Even Numbers (PDF)](paper/symmetric_prime_pairs.pdf) — method, results for every even number up to 100 000, discussion. Rebuilt with `python paper/make_paper.py`.

## Background

[Goldbach's conjecture](https://en.wikipedia.org/wiki/Goldbach%27s_conjecture) (1742) states
that every even integer greater than 2 is the sum of two primes. It has been checked by
computer up to 4 · 10¹⁸, but no proof is known. Writing the two primes as `n − d` and
`n + d` turns the question into one about symmetry: *is there always a pair of primes at the
same distance on both sides of n?* This is closely related to the study of twin primes,
prime gaps and [prime constellations](https://en.wikipedia.org/wiki/Prime_constellation).

This project is **experimental**: it finds such a pair for every number it is given and
thereby gives computational evidence for the conjecture. It is not a proof that a pair
exists for *every* even number.

## Method

1. **Start in the middle.** Halve the even number to get `n`.
2. **Candidates.** Test `L = n − d` and `R = n + d` for `d = 0, 1, 2, …`. Since every prime
   except 2 is odd, only `d` with `n − d` odd can work: `d` odd when `n` is even, `d` even
   when `n` is odd (`d = 0` covers `n` itself being prime, e.g. `10 = 5 + 5`).
3. **Expand symmetrically** until both candidates are prime. Because both sides move by the
   same amount, the sum stays `(n − d) + (n + d) = 2n` at every step.
4. **Verify** `L + R = 2n` and `n − L = R − n`.

Searching from the middle outwards returns the **most balanced** pair, the one with the
smallest `d`.

## Results

| Even number 2n | n | Pair | d |
|---|---|---|---|
| 4 | 2 | 2 + 2 | 0 |
| 10 | 5 | 5 + 5 | 0 |
| 28 | 14 | 11 + 17 | 3 |
| 100 | 50 | 47 + 53 | 3 |
| 1 000 | 500 | 491 + 509 | 9 |
| 10¹² | 5 · 10¹¹ | 499 999 999 769 + 500 000 000 231 | 231 |

For every even number from 4 to 100 000 a pair was found. The distance stays small: on
average `d ≈ 42`, at most `d = 621` (for 80 144) — tiny compared with `n`. The tests check
every even number up to 10 000.

## Use

```bash
python symmetric_prime_pairs.py          # asks for an even number
python symmetric_prime_pairs.py 1000     # or pass it directly
pytest                                   # run the tests
```

```python
from symmetric_prime_pairs import symmetric_prime_pair, is_prime
symmetric_prime_pair(1000)   # (491, 509)
```

Primality is tested by trial division with odd divisors up to √n — fast enough for numbers
up to about 10¹⁴.

### Note on the first version

The first version started with `d = 1` for even `n` and `d = 2` for odd `n`. That skips
`d = 0`, so it looped forever for 4 (= 2 + 2) and 6 (= 3 + 3), and for odd prime `n` it
returned a wider pair than necessary (10 → 3 + 7 instead of 5 + 5). The current version
starts at `d = 0` and stops at `L = 2`; for all other inputs the result is the same.

## License

Apache License 2.0, see [LICENSE](LICENSE).
