# symmetric-prime-pairs

[![tests](https://github.com/Emirhan-1111/symmetric-prime-pairs/actions/workflows/tests.yml/badge.svg)](https://github.com/Emirhan-1111/symmetric-prime-pairs/actions/workflows/tests.yml)

Write an even number as the sum of two primes that lie **symmetrically around its half**:
for `2n`, find primes `L = n − d` and `R = n + d` with the smallest distance `d`.

```
$ python symmetric_prime_pairs.py 100
n (half of the input) = 50
Symmetric prime pair found: L = 47, R = 53 (d = 3)
Verification: L + R = 100 = 2 * 50
```

## Why it is interesting

Every even number greater than 2 is the sum of two primes — that is
[Goldbach's conjecture](https://en.wikipedia.org/wiki/Goldbach%27s_conjecture), unproven
since 1742 but checked by computer up to 4 · 10¹⁸. Searching from the middle outwards finds
the *most balanced* such pair, and the distance `d` stays surprisingly small even for very
large numbers:

| Even number | Pair | d |
|---|---|---|
| 4 | 2 + 2 | 0 |
| 100 | 47 + 53 | 3 |
| 1 000 | 491 + 509 | 9 |
| 10¹² | 499 999 999 769 + 500 000 000 231 | 231 |

## Use

```bash
python symmetric_prime_pairs.py          # asks for a number
python symmetric_prime_pairs.py 1000     # or pass it directly
```

```python
from symmetric_prime_pairs import symmetric_prime_pair
symmetric_prime_pair(1000)   # (491, 509)
```

Primality is tested by trial division up to √n, which is fast enough for numbers up to
about 10¹⁴. Tests (`pytest`) check the result for every even number up to 10 000.

## License

Apache License 2.0, see [LICENSE](LICENSE).
