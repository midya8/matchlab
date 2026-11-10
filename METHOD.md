# Method and evidence contract

## Input

Exactly `version`, `n`, `a`, `b`, `cost`. `version` is integer 1; `n` is integer 1..5. Each side has `n` rows, each a permutation of IDs 0..n-1, best first. `cost` is an n-by-n matrix of integers -1000..1000. Booleans are not integers. Inputs are capped at 65,536 UTF-8 bytes; duplicate keys, floating/exponent tokens and nonfinite numbers are rejected. Native verification permits reports up to 8 MiB. Deep nesting is rejected without a CLI traceback. There are no network requests after the static controls load, no preferences stored elsewhere and no authentication.

A matching `m[a]=b` is a complete bijection. Its ID is its position in lexicographic permutation order. Its inverse gives B-to-A partners. Ranks are zero-based row positions. Pair `(a,b)` blocks exactly when A_a ranks b above m[a] **and** B_b ranks a above inverse[b]. Matched pairs therefore cannot block. Stability means the complete blocker set is empty.

## Two objectives must remain separate

The ordinal rankings determine stability and the stable order. They do not supply the cost matrix. Total supplied cost is sum_a cost[a][m[a]]. All tied cost minima are retained, stable or unconstrained. Stability premium is stable minimum minus unconstrained minimum and is nonnegative because the feasible stable set is a nonempty subset. Negative entries are allowed and do not represent a payment mechanism.

The cost/blocker frontier retains an assignment when no other assignment weakly improves both coordinates and strictly improves at least one. Equal-coordinate assignments are all kept. Every blocker-count cap 0..n(n-1) is inspected; this upper bound suffices because n matched pairs cannot block. Cap zero equals the stable optimum; the largest cap equals the unconstrained optimum. This is a descriptive constraint relaxation, not an intervention, welfare analysis, repair distance or changed-preferences model.

## Deferred acceptance

Start with every proposer free, no receiver holdings and all proposal cursors zero. At each step the lowest-ID free proposer tries the next receiver on its ranking. A receiver accepts when free or when it prefers the new proposer to its current holding; a displaced proposer becomes free. Otherwise the incoming proposer remains free. Each step records proposal ID, previous holding, acceptance, rejected proposer, holdings by receiver, next cursors, sorted free IDs and a partial A-to-B assignment. The partial assignment always uses A-to-B orientation, even when B proposes. It contains null for an unassigned A participant. Proposals are temporary holdings, not irreversible commitments.

Each proposer-receiver pair is tried at most once, so at most n² proposals occur. Under these balanced strict complete assumptions the process returns a perfect stable matching. Its proposer optimality is relative to that side's attainable partners across the stable family. Reversing the proposing side reaches the other extreme. These are the classical Gale-Shapley results [1,2], not an assignment-cost optimization or universal strategy-proofness claim. The deterministic serial schedule differs from simultaneous rounds; tests also shuffle free-proposer order and check the final outcome.

## Stable-family order and lattice

X is A-greater than Y when every A participant weakly prefers its partner in X. On stable assignments, B preferences reverse this order. Join selects the A-better of two partners for each A participant; meet selects the A-worse. The classical strict complete stable-lattice theorem ensures these mappings are stable bijections [2,3]. Every ordered operation is recorded, including identical operands. Covers are oriented A-better to A-worse, with no stable assignment strictly between endpoints. The SVG groups nodes by A-rank sum only for layout. Equal sums are not preference ties, and incomparable nodes need not have equal sums. An isolated one-node lattice has no covers.

The developed diamond control makes clear that the stable family need not be totally ordered. The default control instead makes clear that a supplied stable-cost optimum need not be either deferred-acceptance extreme.

## Independent checks and their limits

`engine.py` enumerates permutations, builds rank lookup arrays, runs cursor/holding deferred acceptance and computes coordinatewise lattice operations. `certificate.py` imports only shared schema validation, not the generator. It separately enumerates bijections, uses direct preference-list indexing for pair tests, tracks proposals through partner arrays and finds joins/meets by searching all upper/lower bounds over the stable family. It checks the exact recursive shape, types, values, ordering and completeness of the report. Dropping assignments, replacing optimum ties with one witness or mutating evidence is not accepted. The validator does not authenticate a source or prove user-supplied preferences true.

The JavaScript engine independently enumerates permutations and computes lattice operations by exhaustive bounds search. Complete browser/native report comparison catches cross-language differences; both implementations use the same specification and developed controls, so agreement cannot exclude a shared conceptual error. Native metamorphic checks cover agent relabeling, side reversal and positive affine cost changes. Other checks cover all 16 complete 2-by-2 ordinal profiles, proposer optimality from the complete family, opposite-side order, lattice associativity/commutativity/absorption, no repeat proposals, improving receiver holdings, cost ties, negative costs, schema/resource limits and arbitrary primitive report forgeries. Source import separation is also tested in a fresh process.

## Input-built integer reference

The optional SciPy/HiGHS reference builds n² binary variables x_ab, one row sum and column sum equal to 1. The unconstrained model minimizes the supplied matrix cost. The stable model adds, for every pair (a,b):

```
x_ab + sum_(b' strictly preferred to b by a) x_ab'
     + sum_(a' strictly preferred to a by b) x_a'b >= 1
```

This is justified directly: if the pair is matched, its variable satisfies the row. Otherwise at least one participant must have a strictly better assigned partner to prevent blocking. With complete strict rankings and row/column bijection constraints, this is equivalent to the no-blocking definition. The reference uses integer variables, not an unverified LP relaxation or a copied optimum. It does not read report witnesses, ranks, matchings, cost values or stable-family constraints to construct the model; it uses report scalar optimum costs only after solving to compare results. The returned integer solution is checked again from input preferences and costs, without a generator witness. Both objectives are solved, but this reference does not independently verify all lattice operations, every optimum tie or every cap. Those use exhaustive replay instead. Related stable matching/assignment LP literature is acknowledged [4]; no claim is made to reproduce a theorem or equation not inspected there.

On the stated test run SciPy 1.15.3 reports success on 152 solves over 76 profiles, zero absolute objective error, tolerance 1e-8. Dependency versions and exact counts are printed, not inferred. This is a finite reference agreement, not proof of universal correctness or a speed comparison.

## Browser and distribution

The browser inspector presents the original input, all assignments and pair tests, both full proposal ledgers, selected partial states, stable partners, all lattice operations/covers, all cost-cap summaries and the complete JSON. Input edits immediately clear stale evidence and disable export. Actual Chrome tests inspect every selected matching, proposal state, operation and cap on all controls at three widths, then use a real mouse event to download reports and call the native verifier. Tables intentionally scroll horizontally inside their own containers. Screenshots must be visually reviewed in addition to DOM assertions.

Installed-wheel verification creates a fresh virtual environment, installs without dependencies, imports outside the source tree, checks module origins and both entrypoints, exercises all controls and verifies forged-report rejection. A development checkout passing tests is not evidence of a working package by itself.

## Attribution and limits

Sources [1..7] are listed in SOURCES.md. Existing software already solves classical matching games; this project contributes a bounded, inspectable evidence interface and original implementation/controls, not a new algorithm, proof, market design method or performance result. All profiles are synthetic and developed. There are no real participants or inferred preferences. Strategy, fairness, welfare, capacities, ties, unacceptable partners, uncertainty and real allocation policy are outside this model.
