import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gradeImplementation, gradeReview } from './grade.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const directory = resolve(process.argv[2] ?? join(here, 'results', '2026-10-16'));
const summary = JSON.parse(await readFile(join(directory, 'summary.json'), 'utf8'));
assert.equal(summary.runs.length, 8);
assert.equal(new Set(summary.runs.map(r => r.id)).size, 8);
const expected = Object.fromEntries(await Promise.all(['SPEC.md', 'money.mjs', 'windows.mjs'].map(async name => [
  name, createHash('sha256').update(await readFile(join(here, 'fixture', name))).digest('hex'),
])));
for (const row of summary.runs) {
  const folder = join(directory, row.id);
  const record = JSON.parse(await readFile(join(folder, 'record.json'), 'utf8'));
  assert.deepEqual(record, row, `${row.id}: summary differs from record`);
  assert.deepEqual(record.initialHashes, expected, `${row.id}: input mismatch`);
  assert.equal(record.exitCode, 0);
  assert.equal(record.timedOut, false);
  assert.equal(record.delegationValid, true);
  const answer = await readFile(join(folder, 'answer.txt'), 'utf8');
  assert.equal(answer, record.final + '\n');
  for (const name of Object.keys(expected)) {
    const actual = createHash('sha256').update(await readFile(join(folder, 'workspace', name))).digest('hex');
    assert.equal(actual, record.finalHashes[name], `${row.id}: saved ${name} differs`);
  }
  assert.equal(record.initialHashes['SPEC.md'], record.finalHashes['SPEC.md']);
  const review = row.id.includes('-review-');
  if (review) {
    assert.deepEqual(record.initialHashes, record.finalHashes);
    assert.deepEqual(record.assessment, gradeReview(answer));
    assert.equal(record.assessment.covered, 4);
    assert.equal(record.editorialAssessment.correctContractViolations, 5);
  } else {
    assert.deepEqual(await gradeImplementation(join(folder, 'workspace')), record.assessment);
    assert.equal(record.assessment.passed, 15);
  }
  const delegated = row.id.endsWith('-delegated');
  if (row.id.startsWith('codex')) {
    const { ledger } = record;
    assert.equal(ledger.spawns.length, delegated ? 2 : 0);
    assert.equal(ledger.workers.length, delegated ? 2 : 0);
    assert(ledger.spawns.every(s => s.succeeded));
    assert(ledger.workers.every(w => w.complete && w.nestedSpawns === 0 && w.model === record.model && w.effort === 'low'));
    if (delegated) assert(Date.parse(ledger.spawns.at(-1).timestamp) < Math.min(...ledger.workerResults.map(r => Date.parse(r.timestamp))), 'Workers did not overlap');
    const unique = new Map(ledger.requests.map(r => [r.responseId, r]));
    assert.equal(unique.size, ledger.requests.length, 'Duplicate response usage');
    const sum = Object.fromEntries(Object.keys(ledger.aggregateUsage).map(key => [key,
      [...unique.values()].reduce((total, request) => total + request.usage[key], 0),
    ]));
    assert.deepEqual(sum, ledger.aggregateUsage);
    for (const [key, value] of Object.entries(record.usage)) assert.equal(value, ledger.rootUsage[key]);
  } else {
    const events = (await readFile(join(folder, 'events.jsonl'), 'utf8')).trim().split('\n').map(JSON.parse);
    const result = events.findLast(e => e.type === 'result');
    assert.deepEqual(record.modelUsage, result.modelUsage);
    assert.equal(record.reportedCostUsd, result.total_cost_usd);
    const calls = events.flatMap(e => (e.message?.content ?? []).filter(c => c.type === 'tool_use' && c.name === 'Agent'));
    assert.equal(calls.length, delegated ? 2 : 0);
    const results = events.flatMap(e => (e.message?.content ?? []).filter(c => c.type === 'tool_result' && calls.some(call => call.id === c.tool_use_id)));
    assert.equal(results.length, calls.length);
    assert(results.every(r => !r.is_error));
    assert.deepEqual(record.permissionDenials, result.permission_denials);
    assert.deepEqual(Object.keys(record.modelUsage), [record.model]);
    assert(record.workerModels.every(model => model === record.model));
  }
  console.log(`${row.id}: inputs, output, grading, delegation, and usage verified`);
}
const excluded = JSON.parse(await readFile(join(directory, 'excluded-setup.json'), 'utf8'));
assert.equal(excluded.length, 6);
const source = await import('./fixture/money.mjs');
assert.equal(source.discountedTotal(1000, 100), -99000);
console.log('8 measured runs and 6 disclosed setup runs verified; review arithmetic counterexample reproduced.');
