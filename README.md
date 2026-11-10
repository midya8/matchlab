# MatchLab

**Stable is a constraint. Not a cost minimum.**

An exact finite inspector for classical strict complete two-sided stable matching. It shows both proposer-optimal outcomes, the whole stable family, every blocking-pair test, the stable lattice and an explicitly separate assignment-cost objective.

The original default profile has three stable assignments. Ignoring stability costs **3**. The cheapest stable assignment costs **13**, a premium of **10**. The unique cheapest stable assignment is neither proposer-optimal extreme. Another original profile has four stable assignments in a diamond, including incomparable outcomes.

## Run locally

Python 3.10+, no runtime dependencies, no paid API or backend:

```sh
python -m pip install .
python -m matchlab demo > report.json
python -m matchlab verify report.json
matchlab run examples/incomparable_diamond.json
python -m http.server --directory docs 8000
```

Open localhost:8000 for the browser inspector. Every input and computation stays in the browser. The independent native checker replays downloaded reports without importing the generator.

## What the evidence contains

- All `n!` bijections, their inverses, every assigned-pair cost, ordinal rank summaries and all `n²` strict blocking-pair tests per assignment.
- Both deferred-acceptance outcomes and every proposal state: current receiver holdings, next preference cursors, free proposers, displacements and partial A-to-B assignment.
- Every stable assignment and each participant's attainable stable partners, ordered by its own preferences.
- Every ordered stable-pair lattice operation and every cover. The generator selects coordinatewise A-better/A-worse partners. The native checker independently searches bounds over the whole stable family.
- All unconstrained/stable cost minima, the stability premium, all tied nondominated cost/blocker-count assignments, and exact minima under every integer blocker-count cap.
- A strict, integer-only JSON schema; complete field/type/order/completeness replay; an installed CLI; responsive evidence tables, assignment/blocker SVGs and a stable-lattice diagram.

IDs and ranks are zero-based. Signed supplied costs are independent of preference ranks. Rank sums and worst rank are descriptive indices, not cardinal utilities, a welfare objective or an implied tie-breaker.

## Scope and honesty

Balanced sides of size **1..5**, strict complete rankings, every pair acceptable, one partner per participant. No ties, unacceptable partners, unmatched people, capacities or learned preferences. The finite enumerator is factorial, not a scalable allocation engine. The deferred-acceptance implementation uses the lowest free proposer ID, not simultaneous rounds.

These are classical algorithms and theory, not new matching results. Developed profiles are teaching controls, not held-out performance data. This project does not establish fairness, strategic honesty for both sides, a social recommendation or suitability for real allocation. Allowing a blocker cap is an explicit relaxation to inspect, not a recommendation to tolerate departures.

## Reproduce checks

```sh
python -m unittest discover -s tests -v
node --test tests/test_engine.cjs
node --test tests/test_browser.cjs
python tools/check_installed.py
python -m pip install scipy==1.15.3
python tools/check_milp.py
```

Node 22+ and an installed `google-chrome` (or `CHROME_BIN`) are needed for actual browser tests. Browser tests use Chrome DevTools directly, not a mock DOM. The optional SciPy check builds binary assignment and stability constraints from the original input only, solves both objectives with HiGHS, and independently checks the returned assignment. Runtime code requires none of these test dependencies.

On 76 profiles (16 developed controls plus 12 seeded profiles at each size 1..5): 2,219 assignments, 49,295 pair witnesses, 113 stable assignments, 217 ordered lattice operations and 715 proposal states. The 20-test native suite rejects 1,372 primitive forgeries; two Node tests compare full Python/JavaScript reports and strict input validation. The optional input-built reference makes 152 integer solves, 1,774 constraint rows and zero absolute cost error with a stated 1e-8 tolerance. Installed-wheel checks cover six module origins, 16 controls, two entrypoints and 32 forged-report CLI rejections.

Actual Chrome checks 48 responsive views at 1440/768/390px, 1,149 selected assignments, 23,793 pair rows, 453 proposal states, 243 lattice-operation selections, 450 blocker-cap selections, invalid-input clearing and 16 downloads independently verified by the native CLI. These counts describe this finite test suite, not universal proof or a performance benchmark.

See [METHOD.md](METHOD.md) for definitions, independence limits and reference constraints, and [SOURCES.md](SOURCES.md) for classical theory and existing software. MIT licensed original implementation.
