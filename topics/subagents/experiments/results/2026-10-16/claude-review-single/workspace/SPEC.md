# Small billing and scheduling library

The modules use JavaScript ES modules. Inputs satisfy the contracts below;
input validation is outside this exercise.

- `money.mjs`, `discountedTotal(cents, percent)`: return the nearest integer
  number of cents after a discount expressed as a percentage from 0 through 100.
  Use JavaScript `Math.round` for half cents.
- `money.mjs`, `splitCents(total, people)`: split a nonnegative integer total
  among a positive integer number of people. Return exactly `people` integers
  whose sum is `total`. Give any remainder to the earliest people, one cent each.
- `windows.mjs`, `overlaps(a, b)`: intervals have numeric `start < end` and are
  half open: start is included, end is excluded. Return whether they intersect.
  Touching endpoints do not overlap.
- `windows.mjs`, `mergeWindows(windows)`: return sorted, merged intervals;
  touching intervals may be merged. Do not mutate the input array or its
  objects. Returned objects must not alias input objects. Empty input returns
  an empty array.

Preserve exports and the contracts. Do not change this specification.
