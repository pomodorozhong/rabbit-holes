import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { cp, mkdir, mkdtemp, readFile, realpath, writeFile } from 'node:fs/promises';
import { tmpdir, homedir, platform, arch, release } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gradeImplementation, gradeReview } from './grade.mjs';
import { codexEvidence } from './codex-evidence.mjs';
import { publicEvents } from './public-events.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const option = (name, fallback) => args.includes(name) ? args[args.indexOf(name) + 1] : fallback;
const product = option('--product', 'all');
const task = option('--task', 'all');
const mode = option('--mode', 'all');
if (!['all', 'codex', 'claude'].includes(product) || !['all', 'review', 'implement'].includes(task) || !['all', 'single', 'delegated'].includes(mode)) {
  throw new Error('Use --product all|codex|claude, --task all|review|implement, --mode all|single|delegated.');
}
const codexModel = option('--codex-model', 'gpt-6.1-sol');
const claudeModel = option('--claude-model', 'sonnet');
const stamp = new Date().toISOString().replaceAll(/[:.]/g, '-');
const output = resolve(option('--out', join(here, 'local-results', stamp)));
const timeout = Number(option('--timeout-seconds', '240')) * 1000;
if (!Number.isFinite(timeout) || timeout <= 0) throw new Error('Timeout must be a positive number.');
const expand = (value, choices) => value === 'all' ? choices : [value];
const products = expand(product, ['codex', 'claude']);
const tasks = expand(task, ['review', 'implement']);
const modes = expand(mode, ['single', 'delegated']);

function promptFor(taskName, runMode, agentProduct) {
  const common = 'Work only in this disposable fixture directory. Read SPEC.md. Inputs satisfy its contracts. Do not use the network or read other projects. Do not change SPEC.md or configuration files. ';
  const instruction = taskName === 'review'
    ? 'Review money.mjs and windows.mjs for violations of SPEC.md. Do not edit any files. Return each real defect with file, exported symbol, a concrete reproducer, expected behavior, and actual behavior. Avoid style findings.'
    : 'Repair money.mjs and windows.mjs to satisfy SPEC.md. Preserve exports, make minimal changes, and verify the contracts. Edit only those two modules. Return a concise description of changes and checks.';
  const delegation = runMode === 'single'
    ? ' Complete all work yourself. Do not delegate or create subagents.'
    : ` Use exactly two ${agentProduct === 'codex' ? 'module_worker' : 'module-worker'} subagents concurrently: assign money.mjs to one and windows.mjs to the other. Give each the specification and its file ownership. Do not let workers spawn more agents. Wait for both, verify their results, and synthesize the final answer yourself.`;
  return common + instruction + delegation + '\n';
}

function commandFor(agentProduct, runMode, directory) {
  if (agentProduct === 'codex') return ['codex', [
    'exec', '--json', '--ignore-user-config', '--ignore-rules', '--strict-config',
    '--skip-git-repo-check', '--sandbox', 'workspace-write', '--model', codexModel,
    '-c', 'approval_policy="never"', '-c', 'model_reasoning_effort="low"',
    '-c', `agents.enabled=${runMode === 'delegated'}`,
    '-c', 'agents.max_concurrent_threads_per_session=2',
    '-c', 'features.memories=false',
    '-c', `projects.${JSON.stringify(directory)}.trust_level="trusted"`,
    '-C', directory, '-',
  ]];
  const tools = ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'];
  if (runMode === 'delegated') tools.push('Agent');
  return ['claude', [
    '--print', '--output-format', 'stream-json', '--verbose', '--forward-subagent-text',
    '--model', claudeModel, '--effort', 'low', '--no-session-persistence',
    '--setting-sources', 'project', '--disable-slash-commands', '--no-chrome',
    '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
    '--settings', '{"disableAllHooks":true,"autoMemoryEnabled":false}',
    '--permission-mode', 'dontAsk', '--permission-prompts', 'none',
    '--tools', tools.join(','),
    '--allowedTools', 'Read,Glob,Grep,Edit,Write,Bash(node *),Agent(module-worker)',
  ]];
}

function run(command, commandArgs, cwd, input) {
  return new Promise(resolveRun => {
    const start = performance.now();
    const child = spawn(command, commandArgs, { cwd, stdio: ['pipe', 'pipe', 'pipe'], detached: true });
    let stdout = '', stderr = '', timedOut = false;
    const timer = setTimeout(() => { timedOut = true; process.kill(-child.pid, 'SIGTERM'); }, timeout);
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.stderr.on('data', chunk => { stderr += chunk; });
    child.on('error', error => { stderr += error.message; });
    child.on('close', code => {
      clearTimeout(timer);
      resolveRun({ code, timedOut, seconds: (performance.now() - start) / 1000, stdout, stderr });
    });
    child.stdin.on('error', () => {});
    child.stdin.end(input);
  });
}

function parse(agentProduct, stdout) {
  const events = stdout.split('\n').filter(Boolean).flatMap(line => { try { return [JSON.parse(line)]; } catch { return []; } });
  if (agentProduct === 'codex') {
    const completed = events.filter(e => e.type === 'item.completed').map(e => e.item);
    const calls = completed.filter(i => /collab|subagent|spawn|agent/i.test(i.type ?? '') && i.type !== 'agent_message');
    return {
      final: completed.filter(i => i.type === 'agent_message').at(-1)?.text ?? '',
      usage: events.filter(e => e.type === 'turn.completed').at(-1)?.usage ?? null,
      usageScope: 'Coordinator CLI turn.completed usage; ledger separately sums response records owned by the root and its workers',
      model: codexModel, coordination: calls,
      resultStatus: events.some(e => e.type === 'turn.completed') ? 'completed' : 'incomplete',
    };
  }
  const result = events.findLast(e => e.type === 'result');
  const coordination = events.flatMap(e => (e.message?.content ?? []).filter(c => c.type === 'tool_use' && ['Agent', 'Task', 'SendMessage', 'TaskOutput'].includes(c.name)));
  const workerCallIds = coordination.filter(c => ['Agent', 'Task'].includes(c.name)).map(c => c.id);
  const workerCompletions = events.flatMap(e => (e.message?.content ?? []).filter(c => c.type === 'tool_result' && workerCallIds.includes(c.tool_use_id))).map(c => ({ toolUseId: c.tool_use_id, isError: Boolean(c.is_error) }));
  const workerModels = [...new Set(events.filter(e => e.parent_tool_use_id && e.message?.role === 'assistant').map(e => e.message.model))];
  const init = events.find(e => e.type === 'system' && e.subtype === 'init');
  return {
    final: result?.result ?? '', usage: result?.usage ?? null,
    modelUsage: result?.modelUsage ?? null,
    reportedCostUsd: result?.total_cost_usd ?? null,
    usageScope: 'CLI result usage/modelUsage; reported USD is an API-equivalent estimate, not a subscription invoice',
    model: init?.model ?? null, coordination, workerCompletions, workerModels,
    permissionDenials: result?.permission_denials ?? [],
    resultStatus: result?.subtype ?? 'incomplete',
  };
}

if (args.includes('--self-check')) {
  const baseline = await gradeImplementation(join(here, 'fixture'));
  if (baseline.passed !== 7 || baseline.total !== 15) throw new Error(`Unexpected fixture baseline: ${JSON.stringify(baseline)}`);
  console.log(JSON.stringify({ fixture: baseline, promptDifference: 'delegation paragraph only', networkCalls: 0 }, null, 2));
} else if (args.includes('--dry-run')) {
  console.log(JSON.stringify(products.flatMap(p => tasks.flatMap(t => modes.map(m => ({ product: p, task: t, mode: m, command: commandFor(p, m, '<FIXTURE>'), prompt: promptFor(t, m, p) })))), null, 2));
} else {
  await mkdir(output, { recursive: true });
  const versions = Object.fromEntries(products.map(p => {
    const version = spawnSync(p, ['--version'], { encoding: 'utf8' });
    if (version.status !== 0) throw new Error(`${p} --version failed: ${version.stderr || version.error}`);
    return [p, version.stdout.trim()];
  }));
  const hardware = platform() === 'darwin' ? spawnSync('sysctl', ['-n', 'machdep.cpu.brand_string', 'hw.memsize'], { encoding: 'utf8' }).stdout?.trim() : null;
  const summary = { startedAt: new Date().toISOString(), node: process.version, platform: platform(), arch: arch(), osRelease: release(), hardware, versions, codexModel, claudeModel, runs: [] };
  benchmark: for (const p of products) for (const t of tasks) for (const m of modes) {
    const id = `${p}-${t}-${m}`;
    const directory = await realpath(await mkdtemp(join(tmpdir(), 'subagents-210-')));
    await cp(join(here, 'fixture'), directory, { recursive: true });
    await cp(join(here, 'examples'), directory, { recursive: true });
    if (p === 'codex') {
      const init = spawnSync('git', ['init', '--quiet', directory], { encoding: 'utf8' });
      if (init.status !== 0) throw new Error(`Fixture git init failed: ${init.stderr}`);
    }
    const runOutput = join(output, id);
    await mkdir(runOutput, { recursive: true });
    const sanitize = value => value.replaceAll(directory, '<FIXTURE>').replaceAll(homedir(), '<HOME>');
    const prompt = promptFor(t, m, p);
    const [command, commandArgs] = commandFor(p, m, directory);
    const initial = Object.fromEntries(await Promise.all(['SPEC.md', 'money.mjs', 'windows.mjs'].map(async file => [file, createHash('sha256').update(await readFile(join(directory, file))).digest('hex')])));
    console.log(JSON.stringify({ status: 'started', id }));
    const startedAt = Date.now();
    const result = await run(command, commandArgs, directory, prompt);
    const parsed = parse(p, result.stdout);
    const ledger = p === 'codex' ? await codexEvidence(result.stdout, startedAt) : null;
    const assessment = t === 'review' ? gradeReview(parsed.final) : await gradeImplementation(directory).catch(error => ({ error: error.message, passed: 0, total: 15 }));
    const final = Object.fromEntries(await Promise.all(['SPEC.md', 'money.mjs', 'windows.mjs'].map(async file => [file, createHash('sha256').update(await readFile(join(directory, file))).digest('hex')])));
    const spawnErrors = /collab spawn failed|failed to load model context/i.test(result.stderr);
    const spawnCalls = p === 'codex' ? ledger.spawns : parsed.coordination.filter(c => ['Agent', 'Task'].includes(c.name));
    const delegationValid = m === 'single'
      ? spawnCalls.length === 0 && !ledger?.error
      : !spawnErrors && spawnCalls.length === 2 && (p === 'claude'
        ? parsed.workerCompletions.length === 2 && parsed.workerCompletions.every(w => !w.isError)
        : ledger.workers.length === 2 && ledger.spawns.every(s => s.succeeded) && ledger.workers.every(w => w.complete && w.nestedSpawns === 0));
    const record = { id, startedAt: new Date(startedAt).toISOString(), seconds: result.seconds, exitCode: result.code, timedOut: result.timedOut, command, args: commandArgs, initialHashes: initial, finalHashes: final, ...parsed, ledger, spawnErrors, delegationValid, assessment };
    await writeFile(join(runOutput, 'record.json'), sanitize(JSON.stringify(record, null, 2)) + '\n');
    await writeFile(join(runOutput, 'prompt.txt'), prompt);
    await writeFile(join(runOutput, 'events.jsonl'), sanitize(publicEvents(result.stdout)));
    await writeFile(join(runOutput, 'stderr.txt'), sanitize(result.stderr));
    await writeFile(join(runOutput, 'answer.txt'), sanitize(parsed.final) + '\n');
    await cp(directory, join(runOutput, 'workspace'), { recursive: true, filter: path => !path.split('/').includes('.git') });
    summary.runs.push(JSON.parse(sanitize(JSON.stringify(record))));
    await writeFile(join(output, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
    console.log(JSON.stringify({ status: 'finished', id, seconds: result.seconds, exitCode: result.code, resultStatus: parsed.resultStatus, coordination: parsed.coordination.length, assessment }));
    if (result.code !== 0 || result.timedOut || !parsed.final || !delegationValid) {
      process.exitCode = 1;
      console.log('Stopped after an unsuccessful run; inspect saved evidence before rerunning.');
      break benchmark;
    }
  }
  console.log(`Results: ${output}`);
}
