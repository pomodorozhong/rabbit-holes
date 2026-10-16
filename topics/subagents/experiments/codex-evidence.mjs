import { createReadStream } from 'node:fs';
import { readFile, readdir, stat } from 'node:fs/promises';
import { createInterface } from 'node:readline';
import { homedir } from 'node:os';
import { join } from 'node:path';

async function firstLine(path) {
  const lines = createInterface({ input: createReadStream(path), crlfDelay: Infinity });
  for await (const line of lines) { lines.close(); return JSON.parse(line); }
}

function usageFor(events, threadId) {
  const responses = new Map(events.filter(e => e.type === 'token_usage_record' && e.payload.thread_id === threadId).map(e => [e.payload.response_id, e.payload.usage]));
  if (!responses.size) return null;
  const keys = Object.keys(responses.values().next().value);
  return Object.fromEntries(keys.map(key => [key, [...responses.values()].reduce((total, usage) => total + usage[key], 0)]));
}

function requestsFor(events, threadId) {
  return events.filter(e => e.type === 'token_usage_record' && e.payload.thread_id === threadId).map(e => ({
    timestamp: e.timestamp, threadId, responseId: e.payload.response_id, usage: e.payload.usage,
  }));
}

// Inspect only this run's root transcript and children whose metadata names it.
// Do not export base instructions, encrypted messages, or unrelated sessions.
export async function codexEvidence(stdout, startedAt) {
  const emitted = stdout.trim().split('\n').flatMap(line => { try { return [JSON.parse(line)]; } catch { return []; } });
  const rootId = emitted.find(e => e.type === 'thread.started')?.thread_id;
  if (!rootId) return { error: 'No thread ID in CLI output', spawns: [], workers: [] };
  const sessions = join(process.env.CODEX_HOME || join(homedir(), '.codex'), 'sessions');
  const candidates = [];
  for (const offset of [-1, 0, 1]) {
    const date = new Date(startedAt + offset * 86400000);
    const folder = join(sessions, String(date.getFullYear()), String(date.getMonth() + 1).padStart(2, '0'), String(date.getDate()).padStart(2, '0'));
    for (const file of await readdir(folder).catch(() => [])) {
      if (!file.endsWith('.jsonl')) continue;
      const path = join(folder, file);
      if ((await stat(path)).mtimeMs >= startedAt - 1000) candidates.push(path);
    }
  }
  const rootFile = candidates.find(path => path.endsWith(`${rootId}.jsonl`));
  if (!rootFile) return { rootId, error: 'Root rollout unavailable; do not count delegation as verified', spawns: [], workers: [] };
  const root = (await readFile(rootFile, 'utf8')).trim().split('\n').map(JSON.parse);
  const outputs = new Map(root.filter(e => e.type === 'response_item' && e.payload.type === 'function_call_output').map(e => [e.payload.call_id, e.payload.output]));
  const spawns = root.filter(e => e.type === 'response_item' && e.payload.type === 'function_call' && e.payload.name === 'spawn_agent').map(e => {
    const parameters = JSON.parse(e.payload.arguments);
    const result = outputs.get(e.payload.call_id);
    let returned; try { returned = JSON.parse(result); } catch { returned = { error: result }; }
    return { timestamp: e.timestamp, name: 'spawn_agent', taskName: parameters.task_name,
      forkTurns: parameters.fork_turns ?? 'default', model: parameters.model ?? 'inherited',
      reasoningEffort: parameters.reasoning_effort ?? 'inherited', result: returned,
      succeeded: Boolean(returned?.task_name || returned?.agent_id) && !returned?.error };
  });
  const workerResults = root.filter(e => e.type === 'response_item' && e.payload.type === 'agent_message').map(e => ({
    timestamp: e.timestamp, author: e.payload.author, recipient: e.payload.recipient,
    content: e.payload.content,
  }));
  const workers = [];
  const requests = requestsFor(root, rootId);
  for (const path of candidates) {
    if (path === rootFile) continue;
    const meta = (await firstLine(path))?.payload;
    if (meta?.parent_thread_id !== rootId && meta?.source?.subagent?.thread_spawn?.parent_thread_id !== rootId) continue;
    const events = (await readFile(path, 'utf8')).trim().split('\n').map(JSON.parse);
    const context = events.find(e => e.type === 'turn_context')?.payload;
    const usage = usageFor(events, meta.id);
    requests.push(...requestsFor(events, meta.id));
    const roles = [...new Set(events.filter(e => e.type === 'response_item' && e.payload.type === 'message').map(e => e.payload.role))];
    workers.push({ id: meta.id, agentPath: meta.agent_path,
      agentRole: meta.source?.subagent?.thread_spawn?.agent_role ?? null,
      forkedFromId: meta.forked_from_id, historyMode: meta.history_mode,
      historyStartOrdinal: meta.subagent_history_start_ordinal,
      model: context?.model, effort: context?.effort, instructionRolesPresent: roles,
      nestedSpawns: events.filter(e => e.ordinal >= meta.subagent_history_start_ordinal && e.type === 'response_item' && e.payload.type === 'function_call' && e.payload.name === 'spawn_agent').length,
      usage, complete: events.some(e => e.type === 'event_msg' && e.payload.type === 'task_complete') });
  }
  const rootUsage = usageFor(root, rootId);
  const aggregateUsage = rootUsage && workers.every(w => w.usage) ? Object.fromEntries(
    Object.keys(rootUsage).map(key => [key, [rootUsage, ...workers.map(w => w.usage)].reduce((total, usage) => total + usage[key], 0)]),
  ) : null;
  return { rootId, spawns, workerResults, workers, requests, rootUsage, aggregateUsage };
}
