# Sources and prior work

Read November 10, 2026. Classical algorithm/theory and existing software are credited separately from original implementation, synthetic teaching controls and evidence format. No source example is claimed as an original developed profile.

1. **David Gale and Lloyd Shapley, "College Admissions and the Stability of Marriage" (1962)**. Primary paper, hosted by the University of Washington. Blocking/stability definitions, deferred acceptance, existence and proposer optimality; complete paper inspected. Original paper uses historical gender labels; this implementation uses A/B.
   https://sites.math.washington.edu/~billey/classes/562.winter.2018/articles/Gale.Shapley.pdf
2. **Alvin Roth, "Deferred Acceptance Algorithms: History, Theory, Practice, and Open Questions" (2008; 2007 draft)**. Author-hosted scholarly survey. Proposer-optimal stable outcomes, opposite interests across sides, stable-family structure and strategic caveats. These classical results motivate the evidence, not novel project claims.
   https://stanford.edu/~alroth/papers/GaleandShapley.revised.IJGT.pdf
3. **IIT Bombay CS6002, Lecture 5, "Structures of Stable Matchings"**. University-hosted lecture notes, date not established. Sections on proposer optimality, opposite-side stable order, coordinatewise better/worse stable matchings and lattice theorem inspected. Used as an explicit proof-level exposition of the lattice operations, not as original research attribution.
   https://www.cse.iitb.ac.in/~swaprava/courses/cs6002/scribed/lec05.pdf
4. **Alvin Roth, Uriel Rothblum and John Vande Vate, "Stable matchings, optimal assignments, and linear programming" (1993)**. Author-hosted primary paper. Abstract/introduction inspected for prior stable-matching/assignment LP work only. The project's binary no-blocking constraint is derived directly in METHOD.md; no uninspected LP theorem or source equation is claimed as reproduced.
   https://web.stanford.edu/~alroth/papers/1993_MOR_StableMatchingsOptimal.pdf
5. **PyCSP3, StableMarriage model documentation**. Official constraint-programming model documentation, date not established. Complete preferences and blocking-pair constraints; independent existing formulation and code context. Runtime code does not use this library.
   https://www.pycsp.org/documentation/models/CSP/StableMarriage/
6. **Henry Wilde, Vincent Knight and Jonathan Gillard, "Matching: A Python library for solving matching games" (2020)**. Journal of Open Source Software, 5(48), 2169, published April 17, 2020. Existing matching software, not a project dependency or a baseline we claim to outperform. JOSS publisher page inspected; documentation URL fetch failed and is not used as evidence of specific API behavior.
   https://joss.theoj.org/papers/10.21105/joss.02169
7. **SciPy, scipy.optimize.milp documentation**. Official API documentation. Binary/integer integrality, linear constraints/bounds, solver status, objective and tolerance reporting for the optional input-built HiGHS reference. Runtime code has no SciPy dependency.
   https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
8. **matchingproblems on PyPI**. Existing matching-problem software describes integer/linear programming and brute-force testing across matching settings. Prior software context only; not a tested dependency or performance baseline.
   https://pypi.org/project/matchingproblems/

## What is original here

Original Python and JavaScript implementations, independently structured exhaustive evidence replay, strict report/schema handling, original finite developed profiles, input-built reference checks, CLI/package checks, browser inspector, DOM/SVG/download checks and portfolio explanation. These engineering contributions do not make Gale-Shapley, the stable lattice, blocking-pair constraints or matching games new.
