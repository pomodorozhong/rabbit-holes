import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import { join } from 'node:path';

export const defects = ['discountedTotal', 'splitCents', 'overlaps', 'mergeWindows'];

export async function gradeImplementation(directory) {
  const money = await import(`${pathToFileURL(join(directory, 'money.mjs'))}?grade=${Date.now()}`);
  const windows = await import(`${pathToFileURL(join(directory, 'windows.mjs'))}?grade=${Date.now()}`);
  const checks = [];
  function check(name, operation) {
    try { operation(); checks.push({ name, passed: true }); }
    catch (error) { checks.push({ name, passed: false, error: error.message }); }
  }
  check('discount: 25 percent', () => assert.equal(money.discountedTotal(100, 25), 75));
  check('discount: zero percent', () => assert.equal(money.discountedTotal(101, 0), 101));
  check('discount: full discount', () => assert.equal(money.discountedTotal(101, 100), 0));
  check('discount: rounding', () => assert.equal(money.discountedTotal(101, 50), 51));
  check('split: remainder', () => assert.deepEqual(money.splitCents(10, 3), [4, 3, 3]));
  check('split: fewer cents than people', () => assert.deepEqual(money.splitCents(2, 4), [1, 1, 0, 0]));
  check('split: zero', () => assert.deepEqual(money.splitCents(0, 3), [0, 0, 0]));
  check('split: divisibility', () => assert.deepEqual(money.splitCents(12, 3), [4, 4, 4]));
  check('overlap: touching', () => assert.equal(windows.overlaps({ start: 0, end: 1 }, { start: 1, end: 2 }), false));
  check('overlap: intersecting', () => assert.equal(windows.overlaps({ start: 0, end: 3 }, { start: 1, end: 2 }), true));
  check('overlap: disjoint', () => assert.equal(windows.overlaps({ start: 0, end: 1 }, { start: 2, end: 3 }), false));
  check('merge: empty', () => assert.deepEqual(windows.mergeWindows([]), []));
  check('merge: sorted union', () => assert.deepEqual(windows.mergeWindows([
    { start: 4, end: 5 }, { start: 1, end: 2 }, { start: 2, end: 4 },
  ]), [{ start: 1, end: 5 }]));
  check('merge: no input mutation', () => {
    const input = [{ start: 3, end: 5 }, { start: 1, end: 4 }];
    const before = structuredClone(input);
    windows.mergeWindows(input);
    assert.deepEqual(input, before);
  });
  check('merge: no output alias', () => {
    const input = [{ start: 1, end: 2 }];
    const output = windows.mergeWindows(input);
    output[0].end = 9;
    assert.equal(input[0].end, 2);
  });
  return { passed: checks.filter(c => c.passed).length, total: checks.length, checks };
}

export function gradeReview(text) {
  // This measures reported locations, not the semantic correctness of prose.
  const mentioned = defects.filter(symbol => new RegExp(`\\b${symbol}\\b`).test(text));
  return { mentioned, covered: mentioned.length, total: defects.length,
    limitation: 'Symbol coverage only; review the saved answer for correct claims, reproductions, and false positives.' };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv[2] === 'review') console.log(JSON.stringify(gradeReview(await readFile(process.argv[3], 'utf8')), null, 2));
  else console.log(JSON.stringify(await gradeImplementation(process.argv[2]), null, 2));
}
