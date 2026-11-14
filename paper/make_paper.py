"""Builds paper/symmetric_prime_pairs.pdf: the write-up of this project, with the results
and the figure computed fresh from symmetric_prime_pairs.py.

Run from the repository root:  python paper/make_paper.py
Needs: reportlab, matplotlib.
"""
import os
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.platypus import (Image, KeepTogether, Paragraph, Preformatted,  # noqa: E402
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from symmetric_prime_pairs import symmetric_prime_pair  # noqa: E402

OUT = Path(__file__).with_name("symmetric_prime_pairs.pdf")
FIG = Path(__file__).with_name("distance.png")
LIMIT = 100_000


def fmt(v):
    """12345 -> '12 345' (thin-space thousands, as in ISO 80000)."""
    return f"{v:,}".replace(",", " ")

# --- fonts with the mathematical characters we need (−, ≤, √, ≈, ·) ----------------------
TTF = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
for name, file in (("Serif", "DejaVuSerif.ttf"), ("Serif-B", "DejaVuSerif-Bold.ttf"),
                   ("Serif-I", "DejaVuSerif-Italic.ttf"), ("Serif-BI", "DejaVuSerif-BoldItalic.ttf"),
                   ("Mono", "DejaVuSansMono.ttf")):
    pdfmetrics.registerFont(TTFont(name, str(TTF / file)))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I",
                              boldItalic="Serif-BI")

body = ParagraphStyle("body", fontName="Serif", fontSize=9.8, leading=14.2, alignment=TA_JUSTIFY,
                      spaceAfter=5)
title = ParagraphStyle("title", parent=body, fontName="Serif-B", fontSize=15, leading=20,
                       alignment=TA_CENTER, spaceAfter=6)
author = ParagraphStyle("author", parent=body, alignment=TA_CENTER, fontSize=10, spaceAfter=14)
h1 = ParagraphStyle("h1", parent=body, fontName="Serif-B", fontSize=11.5, leading=15,
                    spaceBefore=10, spaceAfter=4, alignment=0)
h2 = ParagraphStyle("h2", parent=h1, fontSize=10.2, spaceBefore=6)
abstract = ParagraphStyle("abstract", parent=body, leftIndent=12 * mm, rightIndent=12 * mm,
                          fontSize=9.2, leading=13)
eq = ParagraphStyle("eq", parent=body, alignment=TA_CENTER, fontName="Serif-I", spaceBefore=2,
                    spaceAfter=8)
caption = ParagraphStyle("caption", parent=body, fontSize=8.6, leading=12, alignment=TA_CENTER)
code = ParagraphStyle("code", fontName="Mono", fontSize=7.9, leading=10.4, leftIndent=6 * mm,
                      backColor=colors.HexColor("#f4f4f4"), borderPadding=(5, 6, 5, 6),
                      spaceBefore=4, spaceAfter=10)
ref = ParagraphStyle("ref", parent=body, fontSize=8.8, leading=12.4, leftIndent=6 * mm,
                     firstLineIndent=-6 * mm, alignment=0)


def P(t, s=body):
    return Paragraph(t, s)


# --- experiment ---------------------------------------------------------------------------
evens = list(range(4, LIMIT + 1, 2))
ds = [e // 2 - symmetric_prime_pair(e)[0] for e in evens]
d_max = max(ds)
e_max = evens[ds.index(d_max)]
d_mean = statistics.mean(ds)
n_zero = sum(d == 0 for d in ds)

fig, ax = plt.subplots(figsize=(6.2, 2.9), dpi=200)
ax.scatter(evens, ds, s=0.4, color="#1f4e79", alpha=0.45, linewidths=0)
ax.set_xlabel("even number 2n")
ax.set_ylabel("distance d")
ax.set_xlim(0, LIMIT)
ax.set_ylim(0, d_max * 1.08)
ax.scatter([e_max], [d_max], s=14, color="#c0392b", zorder=3)
ax.annotate(f"largest d = {d_max} at 2n = {fmt(e_max)}", (e_max, d_max), xytext=(-8, 0),
            textcoords="offset points", ha="right", va="center", fontsize=8)
ax.grid(alpha=0.25, lw=0.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(FIG)
plt.close(fig)

examples = [4, 10, 28, 100, 1_000, 10_000, 10**6, 10**12]
rows = [["Even number 2n", "n", "L", "R", "d"]]
for e in examples:
    L, R = symmetric_prime_pair(e)
    rows.append([fmt(e), fmt(e // 2), fmt(L), fmt(R), str(e // 2 - L)])

CODE = '''def is_prime(num):
    """Determine whether a given number is prime."""
    if num < 2:
        return False
    if num % 2 == 0:
        return num == 2
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True


def symmetric_prime_pair(even_number):
    """(L, R) with L + R = even_number, both prime, closest to even_number / 2."""
    if even_number % 2 != 0 or even_number < 4:
        raise ValueError("the number must be even and at least 4")
    n = even_number // 2
    d = 0
    while n - d >= 2:
        if is_prime(n - d) and is_prime(n + d):
            return n - d, n + d
        d += 1
    raise RuntimeError(f"no pair found for {even_number}")'''

# --- document -----------------------------------------------------------------------------
story = [
    P("Symmetric Prime Pairs and the Expression<br/>of Even Numbers: An Experimental Approach",
      title),
    P("Emirhan Turgut<br/><font size=8.5>March 2025, revised November 2026 · "
      "github.com/Emirhan-1111/goldbach-symmetric-pairs</font>", author),
    P("<b>Abstract.</b> We propose and examine experimentally an algorithm that, for a given "
      "integer <i>n</i>, finds two primes <i>L</i> and <i>R</i> located symmetrically around "
      "<i>n</i>, i.e. <i>L</i> = <i>n</i> − <i>d</i> and <i>R</i> = <i>n</i> + <i>d</i>. "
      "Starting at <i>d</i> = 0 and widening the distance step by step, the construction "
      "guarantees <i>L</i> + <i>R</i> = 2<i>n</i> for the pair it returns, and the pair is the "
      "most balanced one. For every even number from 4 to "
      f"{fmt(LIMIT)} such a pair was found, with a mean distance of "
      f"{d_mean:.1f} and a largest distance of {d_max}. These results are consistent with "
      "Goldbach's conjecture; they are computational evidence, not a proof. A Python "
      "implementation is included.", abstract),

    P("1. Introduction", h1),
    P("The representation of even numbers as sums of two primes has been a central theme in "
      "number theory ever since Goldbach's conjecture was proposed in 1742. The conjecture "
      "asserts that every even integer greater than two can be expressed as the sum of two "
      "primes. It has been verified by computer for all even numbers up to 4 · 10<super>18</super> "
      "[4], yet a formal proof remains elusive. Related questions about twin primes, prime "
      "gaps and prime constellations [1, 2] have given much insight into how primes are "
      "distributed."),
    P("Writing the two primes as <i>n</i> − <i>d</i> and <i>n</i> + <i>d</i> turns the question "
      "into one about symmetry: is there, for every <i>n</i> ≥ 2, a distance <i>d</i> such "
      "that both numbers at that distance from <i>n</i> are prime? In this study we introduce "
      "an algorithm that searches for such a pair and satisfies"),
    P("L + R = 2n.", eq),
    P("The approach demonstrates the special case of even numbers being expressible as the sum "
      "of two primes that are equidistant from <i>n</i>, and it lets us observe how far from "
      "<i>n</i> one has to go to find them."),

    P("2. Methodology", h1),
    P("2.1 Candidate selection", h2),
    P("Every prime other than 2 is odd, so for <i>n</i> − <i>d</i> and <i>n</i> + <i>d</i> to "
      "be prime they must in general be odd. This fixes the parity of <i>d</i>:"),
    P("• For <b>even</b> <i>n</i>, <i>d</i> must be odd; the first candidates are "
      "<i>L</i> = <i>n</i> − 1 and <i>R</i> = <i>n</i> + 1.<br/>"
      "• For <b>odd</b> <i>n</i>, <i>d</i> must be even; the first candidates are "
      "<i>L</i> = <i>R</i> = <i>n</i> (<i>d</i> = 0), which already succeeds when <i>n</i> "
      "itself is prime, e.g. 10 = 5 + 5."),
    P("The implementation simply tries <i>d</i> = 0, 1, 2, …; candidates of the wrong parity "
      "are rejected at once by the primality test, so the result is the same."),
    P("2.2 Iterative adjustment", h2),
    P("If one of the candidates is not prime, the distance is increased on both sides at once,"),
    P("L ← L − 2,   R ← R + 2   (within the admissible parity),", eq),
    P("until both <i>L</i> and <i>R</i> are prime. Because both sides move by the same amount, "
      "the difference from <i>n</i> stays equal on both sides, and when a pair is found"),
    P("L + R = (n − d) + (n + d) = 2n.", eq),
    P("2.3 Symmetry verification", h2),
    P("The algorithm verifies that the pair is symmetric by confirming"),
    P("(n − L) − (R − n) = 0,", eq),
    P("which guarantees that the two primes are equidistant from <i>n</i>. Since the search "
      "goes outwards from <i>n</i>, the pair returned is the one with the smallest distance "
      "<i>d</i>."),
    P("2.4 Termination", h2),
    P("The search stops when <i>L</i> would fall below 2. For the smallest cases the pair has "
      "<i>d</i> = 0: 4 = 2 + 2 and 6 = 3 + 3. Reaching <i>L</i> &lt; 2 without a pair would "
      "mean that 2<i>n</i> is not a sum of two primes at all, i.e. a counterexample to "
      "Goldbach's conjecture; the implementation raises an error in that case. It never "
      "occurred in our experiments."),

    P("3. Experimental results", h1),
    P("<b>Worked example.</b> Take the even number 28, so <i>n</i> = 14 (even). The first "
      "candidates are <i>L</i> = 13 and <i>R</i> = 15; 15 is composite, so the algorithm "
      "proceeds. The next candidates are <i>L</i> = 11 and <i>R</i> = 17. Both are prime, and"),
    P("11 + 17 = 28 = 2 × 14,   (14 − 11) − (17 − 14) = 0.", eq),
    P("<b>Selected values.</b> Table 1 shows the pairs found for a range of sizes. Even for "
      "2<i>n</i> = 10<super>12</super> the two primes lie only 231 away from the middle."),
]
tbl = Table(rows, hAlign="CENTER", colWidths=[33 * mm, 28 * mm, 34 * mm, 34 * mm, 12 * mm])
tbl.setStyle(TableStyle([
    ("FONT", (0, 0), (-1, -1), "Serif", 8.6), ("FONT", (0, 0), (-1, 0), "Serif-B", 8.6),
    ("ALIGN", (0, 0), (-1, -1), "RIGHT"), ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.black),
    ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
    ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.black),
    ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
story += [KeepTogether([tbl, Spacer(1, 3), P("Table 1. Most balanced prime pairs L + R = 2n.",
                                             caption)]), Spacer(1, 6)]
story += [
    P(f"<b>Every even number up to {fmt(LIMIT)}.</b> "
      f"The algorithm was run for all {fmt(len(evens))} even numbers from 4 to "
      f"{fmt(LIMIT)}. A pair was found in every case. The mean distance is "
      f"{d_mean:.1f}, the largest is {d_max} (for 2<i>n</i> = {fmt(e_max)}), and in {fmt(n_zero)} cases "
      "<i>n</i> itself is prime (<i>d</i> = 0). Figure 1 shows the distance for each even "
      "number: it grows only very slowly and stays tiny compared with <i>n</i>."),
    KeepTogether([Image(str(FIG), width=118 * mm, height=118 * mm * 2.9 / 6.2),
                  P(f"Figure 1. Distance d of the most balanced prime pair for every even number "
                    f"up to {fmt(LIMIT)}.", caption)]),

    P("4. Computational verification via Python", h1),
    P("The algorithm is implemented in Python; the complete program with input handling and "
      "tests is in the repository. The core is short:"),
    Preformatted(CODE, code),
    P("<b>Primality test.</b> <font name=Mono size=8.5>is_prime</font> rules out numbers "
      "below 2 and even numbers other than 2, then tries odd divisors up to √<i>n</i>: if "
      "<i>n</i> = <i>a</i> · <i>b</i> with <i>a</i> ≤ <i>b</i>, then <i>a</i> ≤ √<i>n</i>. "
      "This is fast enough for numbers up to about 10<super>14</super>."),
    P("<b>Search.</b> <font name=Mono size=8.5>symmetric_prime_pair</font> halves the input, "
      "widens the distance until both candidates are prime and returns the pair; "
      "<i>L</i> + <i>R</i> = 2<i>n</i> holds by construction. The test suite checks for every "
      "even number up to 10 000 that both numbers are prime and sum to the input."),

    P("5. Discussion", h1),
    P("The method is experimental. The algorithm finds a symmetric prime pair for every value "
      "tested, but this does not prove that every even number can be represented as the sum "
      "of two primes: no finite number of checks covers all even numbers. The results are "
      "computational evidence that supports the numerical observations related to Goldbach's "
      "conjecture."),
    P("The small distances are not a coincidence. A heuristic by Hardy and Littlewood [3] "
      "predicts that the number of ways to write 2<i>n</i> as a sum of two primes grows "
      "roughly like <i>n</i> / (ln <i>n</i>)<super>2</super>, so larger even numbers have more "
      "and more representations, and one of them is likely to lie close to the middle. The "
      "symmetric formulation makes this visible: Figure 1 is in effect a picture of how "
      "densely such pairs fill the neighbourhood of <i>n</i>."),
    P("<b>Note on the first version.</b> The first version of the algorithm started at "
      "<i>d</i> = 1 for even <i>n</i> and <i>d</i> = 2 for odd <i>n</i>. Skipping <i>d</i> = 0 "
      "made it miss 4 = 2 + 2 and 6 = 3 + 3 (it then searched without end) and, for odd "
      "prime <i>n</i>, return a wider pair than necessary (10 → 3 + 7 instead of 5 + 5). "
      "Starting at <i>d</i> = 0 and stopping at <i>L</i> = 2 removes both issues; for every "
      "other input the result is unchanged."),

    P("6. Conclusion", h1),
    P("We have introduced an experimental algorithm that, for a given integer <i>n</i>, finds "
      "the most balanced pair of primes <i>L</i> = <i>n</i> − <i>d</i>, <i>R</i> = <i>n</i> + "
      "<i>d</i>, so that <i>L</i> + <i>R</i> = 2<i>n</i>. For all even numbers up to "
      f"{fmt(LIMIT)} and for selected values up to 10<super>12</super> such "
      "a pair exists and lies close to <i>n</i>. The approach agrees with Goldbach's "
      "conjecture, but it remains an empirical observation rather than a formal proof. Future "
      "work may extend the experiments to larger ranges with a faster primality test "
      "(e.g. Miller–Rabin) and compare the observed distances with the Hardy–Littlewood "
      "prediction."),

    P("References", h1),
    P("[1] Twin prime. Wikipedia. https://en.wikipedia.org/wiki/Twin_prime", ref),
    P("[2] Prime constellation. Wikipedia. https://en.wikipedia.org/wiki/Prime_constellation", ref),
    P("[3] G. H. Hardy, J. E. Littlewood. Some problems of 'Partitio numerorum' III: On the "
      "expression of a number as a sum of primes. <i>Acta Mathematica</i> 44 (1923), 1–70.", ref),
    P("[4] T. Oliveira e Silva, S. Herzog, S. Pardi. Empirical verification of the even "
      "Goldbach conjecture and computation of prime gaps up to 4 · 10<super>18</super>. "
      "<i>Mathematics of Computation</i> 83 (2014), 2033–2060.", ref),
    P("[5] Goldbach's conjecture. Wikipedia. "
      "https://en.wikipedia.org/wiki/Goldbach%27s_conjecture", ref),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Serif", 8)
    canvas.drawCentredString(A4[0] / 2, 12 * mm, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=24 * mm, rightMargin=24 * mm,
                        topMargin=22 * mm, bottomMargin=22 * mm,
                        title="Symmetric Prime Pairs and the Expression of Even Numbers",
                        author="Emirhan Turgut", subject="An experimental approach to Goldbach's conjecture")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
os.remove(FIG)
print("written:", OUT.relative_to(ROOT), f"(d_mean {d_mean:.1f}, d_max {d_max} at {e_max})")
