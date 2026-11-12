# MatchLab

An exact finite inspector for classical strict complete two-sided stable matching. It shows both proposer-optimal outcomes, the whole stable family, every blocking-pair test, the stable lattice and an explicitly separate assignment-cost objective.

The original default profile has three stable assignments. Ignoring stability costs **3**. The cheapest stable assignment costs **13**, a premium of **10**. The unique cheapest stable assignment is neither proposer-optimal extreme. Another original profile has four stable assignments in a diamond, including incomparable outcomes.

## Choose a view

| Question | Evidence |
| --- | --- |
| What does either side's proposal process produce? | Both deferred-acceptance traces and proposer-optimal outcomes |
| Which assignments are stable? | Every bijection and every blocking-pair test |
| How are stable outcomes ordered? | All stable partners, lattice operations and covers |
| What does a separate supplied cost objective select? | Unconstrained/stable minima, cost ties and blocker-cap minima |

Stability and cost minimization are separate constraints. Costs do not follow
from preference ranks, and a cheapest assignment need not be stable. None of
these supplied-model results recommends an allocation for real people.

## Run locally

Python 3.10+, no runtime dependencies, no paid API or backend:

```sh
python -m venv .venv
. .venv/bin/activate
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

## Scope and limits

Balanced sides of size **1..5**, strict complete rankings, every pair acceptable, one partner per participant. No ties, unacceptable partners, unmatched people, capacities or learned preferences. The finite enumerator is factorial, not a scalable allocation engine. The deferred-acceptance implementation uses the lowest free proposer ID, not simultaneous rounds.

These are classical algorithms and theory, not new matching results. Developed profiles are teaching controls, not held-out performance data. This project does not establish fairness, strategic honesty for both sides, a social recommendation or suitability for real allocation. Allowing a blocker cap is an explicit relaxation to inspect, not a recommendation to tolerate departures.

## Reproduce checks

```sh
python -m unittest discover -s tests -v
node --test tests/test_engine.cjs
node --test tests/test_browser.cjs
python tools/check_assets.py
python tools/check_installed.py
```

Node 22+ and an installed `google-chrome` (or `CHROME_BIN`) are needed for actual browser tests. Browser tests use Chrome DevTools directly, not a mock DOM. The optional SciPy check builds binary assignment and stability constraints from the original input only, solves both objectives with HiGHS, and independently checks the returned assignment. Runtime code requires none of these test dependencies.

The native suite checks the complete finite evidence, relabeling and side-reversal
properties, and rejection of forged reports. The browser suite compares complete
Python/JavaScript reports, exercises the matching, proposal, lattice and cost-cap
views at three widths, and verifies downloaded reports with the native CLI. The
wheel check runs both entrypoints outside the source checkout. Counts in the test
output describe this finite suite, not a performance benchmark or universal proof.

Run the optional input-built integer reference in the active virtual environment:

```sh
python -m pip install scipy==1.15.3
python tools/check_milp.py
```

See [METHOD.md](METHOD.md) for definitions, independence limits and reference constraints, and [SOURCES.md](SOURCES.md) for classical theory and existing software. MIT licensed original implementation.
