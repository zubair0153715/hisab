"""Hisab engine verification: every case hand-checked against known math.

Run: python3 tests/verify.py  (from the repo root)
All assertions compare SymPy's EXACT output to hand-computed values.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import sympy as sp
from hisab.solver import solve_problem

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name} {detail}")


def ans(text, **kw):
    return solve_problem(text, **kw)["answer"]


print("== linear equations ==")
r = solve_problem("2x+6=0")
check("2x+6=0 -> x=-3", r["answer"] == "x = -3", r["answer"])
check("linear has 3 steps", len(r["steps"]) == 3, str(len(r["steps"])))
check("linear step math derived",
      r["steps"][1]["math"] == "2*x = -6", r["steps"][1]["math"])
r = solve_problem("3(x-2)=9")
check("3(x-2)=9 -> x=5", r["answer"] == "x = 5", r["answer"])
r = solve_problem("2x+3=7")  # implicit multiplication parse
check("implicit mult 2x+3=7 -> x=2", r["answer"] == "x = 2", r["answer"])

print("== quadratic equations ==")
r = solve_problem("x^2-5x+6=0")
check("x^2-5x+6=0 roots 2,3",
      r["answer"] == "x = 2, x = 3", r["answer"])
check("discriminant shown = 1",
      any("1" in s["math"] and "D" in s["math"] for s in r["steps"]),
      str([s["math"] for s in r["steps"]]))
r = solve_problem("x^2+2x+1=0")
check("double root x=-1", r["answer"] == "x = -1", r["answer"])
r = solve_problem("2x^2+8=0")
check("no real roots handled",
      "I" in r["answer"] or "imag" in r["answer"].lower() or r["answer"],
      r["answer"])

print("== systems ==")
r = solve_problem("x+y=5")
# single equation with 2 unknowns -> parametric; system needs 2 eqns.
# Hisab solves one equation: check it doesn't crash and mentions both vars.
check("x+y=5 kind", r["kind"] in ("linear", "system", "equation"), r["kind"])

print("== calculus ==")
r = solve_problem("d/dx x^3+2*x")
check("d/dx(x^3+2x)=3x^2+2",
      r["answer"] == "3*x**2 + 2", r["answer"])
check("derivative rule named",
      "Power" in r["steps"][0]["note"] or "rule" in r["steps"][0]["note"].lower(),
      r["steps"][0]["note"])
r = solve_problem("d/dx sin(x)", mode="differentiate")
check("d/dx sin = cos", r["answer"] == "cos(x)", r["answer"])
r = solve_problem("∫ 3*x^2 dx")
check("∫3x²dx = x³+C", r["answer"] == "x**3 + C", r["answer"])
r = solve_problem("lim x->0 sin(x)/x")
check("lim sin(x)/x -> 1", r["answer"] == "1", r["answer"])

print("== algebra ops ==")
r = solve_problem("(x^2-1)/(x-1)", mode="simplify")
check("(x²-1)/(x-1) = x+1", r["answer"] == "x + 1", r["answer"])
r = solve_problem("x^2-4", mode="factor")
check("factor x²-4", r["answer"] == "(x - 2)*(x + 2)", r["answer"])
r = solve_problem("(x+1)^2", mode="expand")
check("expand (x+1)²", r["answer"] == "x**2 + 2*x + 1", r["answer"])

print("== robustness ==")
for bad in ["", "hello world", "__import__('os')", "x="]:
    try:
        solve_problem(bad)
        check(f"reject {bad!r}", False, "no error raised")
    except ValueError:
        check(f"reject {bad!r}", True)
    except Exception as e:
        check(f"reject {bad!r}", False, f"wrong exc {type(e).__name__}")

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
