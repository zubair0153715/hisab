# Hisab (حساب) — free AI math tutor

**Photo ya type karo, steps seekho.** Free, unlimited, no paywall on steps.

An original clean-room build. Not affiliated with Photomath/Google or
Gauth/ByteDance. Built as one of the daily gap-builds:
[gap report](../market-gaps/daily/2026-10-22-hisab.md)
(Photomath's + Gauth's public gaps).

## Why it exists (the gaps it fills)

Photomath Plus ($9.99/mo) gates "detailed steps" — the actual product —
behind a subscription (1-star ComplaintsBoard reviews call this out by name);
Gauth's free tier is 3 questions/day with paid credits that expire monthly.
Both misread handwriting, go wrong on harder problems ("explanations skip
logical jumps"), and explain in English only.

Hisab answers all three:

1. **Steps are always free — and computed, never hallucinated.** A SymPy
   exact-CAS engine solves the problem; every displayed step is *derived*
   from that computation (linear isolation steps, discriminant + quadratic
   formula with substituted values, named calculus rules). Unlimited, no
   paywall, no expiring credits. (Honest caveat: AI photo-reading and AI
   explanations run on the owner's free Gemini quota — typed solving via
   SymPy always works, key or no key.)
2. **Verified correctness by construction.** Answers come from SymPy; the
   test suite asserts exact results on algebra + calculus cases. The page
   names the engine instead of hiding behind a black box.
3. **Urdu + English teaching.** Explanations in proper Urdu or English, plus
   a follow-up "why?" chat grounded in the computed steps (it quotes the
   steps and says plainly when something isn't there).

## Input formats

- Typed: `2x^2+5x-3=0`, `d/dx x^3+2x`, `∫ 3x^2 dx`, `lim x->0 sin(x)/x`,
  `(x^2-1)/(x-1)` (+ simplify/factor/expand/differentiate/integrate modes)
- Photo: any clear photo of a printed problem (AI vision extracts it)

## Privacy

The server stores nothing and trains on nothing. Photos are processed
in-memory for the vision call and discarded.

## Layout

- `hisab/solver.py` — SymPy exact engine: parse, classify, solve with
  derived pedagogical steps (22-test verified suite)
- `hisab/gemini.py` — photo reading (vision), explanations, grounded chat
  (Gemini free tier; key read at call time only, never stored)
- `hisab/routes.py` — FastAPI router (`/hisab`, `/api/read-photo`,
  `/api/solve`, `/api/chat`, `/api/ai-status`)
- `hisab/pages.py` — single-page UI (MathJax rendering, EN/UR toggle)
- `tests/verify.py` — engine verification vs hand-computed references

## Run the tests

```
python3 tests/verify.py
```
