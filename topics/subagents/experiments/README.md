# A small single-agent versus subagent comparison

On two small review and repair tasks, the two-worker workflow took longer than the single-agent workflow in every measured pair. All four repairs passed the same 15 checks. All four reviews described the five real contract violations, although Claude's single-agent answer also made one incorrect arithmetic claim. This is one observation per configuration on a tiny fixture, not a general productivity ranking.

The [configuration guide](../configuration-and-effectiveness.md) explains the broader mechanisms and evidence. This page describes the experiment so its inputs, outputs, and limitations can be inspected or repeated.

## Tasks and success criteria

The [fixture specification](fixture/SPEC.md) describes four exports in two short modules. The starting implementation contains four source defects with five contract consequences:

| Export | Seeded behavior | Required behavior |
| --- | --- | --- |
| `discountedTotal` | Uses percentage as a fraction | Divide the percentage by 100 and round cents |
| `splitCents` | Discards remainder cents | Preserve the total and give remainder cents to the earliest people |
| `overlaps` | Includes touching endpoints | Use half-open interval intersection |
| `mergeWindows` | Retains and later changes input objects | Avoid input mutation and output aliases |

**Review task:** find real contract violations without editing files; give the export, reproducer, expected behavior, and actual behavior. The automatic score counts the four affected export names. It does not decide whether the explanation is correct. After the runs, an agent session running Codex, one of the two tools being compared, inspected the saved answers against the fixture, including all five obligations and incorrect extra claims. Because that assessor shares a product with half of the answers it judged, it is not a neutral grader, and its scores are not a blinded or human evaluation. They are kept in a separate [editorial assessment](results/2026-10-16/editorial-assessment.json) so that the runner's records contain only what the runner measured.

**Repair task:** edit only the two modules, preserve their exports, and satisfy the specification. The independent [grader](grade.mjs) runs 15 behavioral checks. The agent's temporary workspace contains neither the grader nor the answer key. The buggy baseline passes 7/15; a repair must pass 15/15. These checks exercise the stated edge cases without proving correctness for all possible inputs.

Each product gets a single-agent condition and a delegated condition for each task. Single-agent runs have delegation disabled. Delegated runs request exactly two concurrent workers, one per module, with no further delegation; the parent verifies and combines their work. Models and effort stay fixed within each product. The shared task text changes only in its delegation paragraph; enabling the agent tool and concurrency settings is also part of that treatment.

## Environment and protocol

Measured on **2026-10-16, Asia/Taipei**, from an Apple M2 Pro Mac with 16 GiB RAM, using Node.js **v26.11.1**. The models run on the providers' services; this hardware describes the client and local tool environment.

| Setting | Codex | Claude Code |
| --- | --- | --- |
| CLI | `codex-cli 0.162.1` | `2.1.287` |
| Model | `gpt-6.1-sol` | `sonnet` resolved to `claude-sonnet-5-5` |
| Effort | `low`; child records confirm the same model and effort | `low`; child messages and model usage confirm the same model |
| Authentication | Existing ChatGPT login | Existing Claude subscription login |
| Fixture | New canonical temporary path and empty Git repository for project discovery | New temporary directory with the same source files |
| Instructions | Task prompt; native named workers in delegated runs | Task prompt; the `module-worker` custom definition in delegated runs |
| Permissions | `workspace-write`, `approval_policy="never"` | `dontAsk`; explicit file-tool and `Bash(node *)` allow rules |
| Configuration isolation | Ignore user config and execution rules; disable memories | Load project settings, disable hooks/skills/memory, use an empty explicit MCP configuration |
| Delegation control | `agents.enabled=false/true`; cap of two spawned threads | Exclude/include `Agent`; project settings cap workers at two and nesting at one |

Both conditions retain the same editing tools for a given product, including the review task; compliance with the no-edit instruction is checked with file hashes. This measures the requested workflow under those controls, rather than an enforced read-only review configuration.

The [runner](run.mjs) creates a fresh fixture for every run, sends the prompt over stdin, and records command arguments, input/output hashes, stream events, final answer, and the resulting workspace. It runs the cases sequentially, with single before delegated. Time is measured from just before starting the CLI process until it exits. It includes CLI startup, service latency, tool calls, coordination, retries, and the parent's checks. Fixture setup, transcript extraction, and the independent grader run outside that timer.

## Results

The [complete summary](results/2026-10-16/summary.json) links the measurements to per-run records. “Input” includes cached input, not just newly processed input. Counts accumulate over model requests; they are not the size of the final conversation or of the two source files.

| Product / task | Workflow | Seconds | Input tokens | Output tokens | Quality | CLI USD estimate |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| Codex / review | Single | 21.61 | 47,321 | 739 | Five violations; correct checked examples | Unavailable |
| Codex / review | Two workers | 42.75 | 269,533 | 1,963 | Five violations; correct checked examples | Unavailable |
| Codex / repair | Single | 29.79 | 63,045 | 1,250 | 15/15 checks | Unavailable |
| Codex / repair | Two workers | 44.56 | 250,381 | 2,263 | 15/15 checks | Unavailable |
| Claude / review | Single | 11.29 | 14,281 | 1,245 | Five violations; one incorrect extra claim | $0.0265 |
| Claude / review | Two workers | 20.42 | 90,023 | 3,414 | Five violations; correct checked examples | $0.1220 |
| Claude / repair | Single | 17.78 | 31,078 | 1,724 | 15/15 checks; recovered permission denial | $0.0362 |
| Claude / repair | Two workers | 22.48 | 112,669 | 3,654 | 15/15 checks | $0.0915 |

For these pairs, delegation took approximately **1.98× and 1.50×** the Codex review and repair times, and **1.81× and 1.26×** the Claude times. Both workers can finish correctly while the parent still spends enough time starting, waiting, checking, and synthesizing to lose the latency benefit on such short tasks.

Two details prevent the quality column from being reduced to a perfect-score label:

- The [Claude single-agent review](results/2026-10-16/claude-review-single/answer.txt) correctly demonstrates the 10% discount bug, but then says that 100% gives a correct result or negative zero. In the starting code, `discountedTotal(1000, 100)` returns `-99000`. The symbol-coverage score alone would miss this error. The [delegated answer](results/2026-10-16/claude-review-delegated/answer.txt) correctly gives that counterexample.
- The [Claude single-agent repair record](results/2026-10-16/claude-implement-single/record.json) contains one denied shell call that tried to rewrite files with `cat` and `sed`. The agent recovered using allowed file tools and produced a passing repair. The measured time includes that recovery; the denial is retained rather than treated as absent or removed by rerunning.

The two Codex reviews ran concrete Node reproducers. The Claude review answers explicitly say their examples were traced from source rather than executed. The saved evidence preserves that distinction.

### Usage accounting

Codex's CLI `turn.completed.usage` corresponds to the coordinator in these runs. The records' `ledger` separately contains successful spawns, worker completion metadata, and per-response token records for the root and its two children. The table sums unique response records owned by those three threads, excluding copied parent-history records in worker transcripts. Cached input is a subset of Codex input and is **not** added again; reasoning output is likewise not added on top of output tokens.

Claude's table uses the final event's `modelUsage`, including worker usage, rather than assuming the top-level `usage` object is the whole workflow. Input is the sum of ordinary input, cache-read input, and cache-creation input. The reported dollar figure is the CLI's list-price estimate for that run. Subscription billing is not inferred from it. [Claude Code cost accounting](https://code.claude.com/docs/en/costs), [Agent SDK cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)

These counters have different semantics and pricing rules. Compare each product's paired workflows; the table does not establish which provider is cheaper or more token-efficient on an equivalent workload. Codex did not expose a comparable dollar estimate, so its USD field remains unavailable.

## Check delegation instead of trusting the answer

The eight reported cases come from **14 CLI sessions**, including **six excluded Codex setup runs**. The [setup records](results/2026-10-16/excluded-setup.json) retain their arguments, timing, exit status, and stderr:

1. An initial four-case Codex block used `--ephemeral`. Its delegated runs logged `collab spawn failed` and `no rollout found` when loading parent context, despite exiting successfully and claiming worker completion. The entire block was excluded.
2. A two-case persistence trial exposed a second instrumentation problem: the JSON stream showed waits but omitted native spawn details. The stored transcript confirmed actual spawns, but the JSON-only validator rejected the run. Both trial cases were excluded while the capture protocol was finalized.
3. The final Codex block used persistent sessions, canonical paths, an empty Git repository for project discovery, and a root/worker ledger. All four final cases are retained. The four Claude cases are also retained; their source/configuration setup and arguments did not change during this correction.

These exclusions were for setup and instrumentation, not for an unfavorable score or elapsed time. Prior trials can still influence service caches, so they are part of the limitations. The initial apparent success is itself a reason to inspect tool results and diagnostics: an answer that says “both workers completed” is not proof of successful delegation.

In the final Codex evidence, two successful spawn results match two completed child transcripts, with inherited model/effort and parent-fork metadata. The children record `agentRole: null`: the measured path is native named delegation, not verification of custom-role selection from the optional TOML file. The ledger omits base instructions and encrypted handoff content; prompts, worker summaries, metadata, usage records, and output files remain available.

Claude's stream contains two `Agent` calls and their successful results; forwarded child messages expose worker models. The single-agent cases contain no spawn calls. Parent JSON streams alone are therefore sufficient for one capture path but insufficient for the other. [Claude Code stream options](https://code.claude.com/docs/en/cli-reference#cli-flags)

## Reproduce or inspect without model calls

Prerequisites for live runs are Node.js 22 or later, Git, both CLIs on `PATH`, authenticated accounts with access to the selected models, and a writable normal Codex session directory. The stored results were obtained on macOS; other operating systems have not been live-tested. The runner uses no npm dependencies.

From the repository root, inspect the protocol and verify the saved results without sending model requests:

```sh
node topics/subagents/experiments/run.mjs --self-check
node topics/subagents/experiments/run.mjs --dry-run
node topics/subagents/experiments/verify.mjs
```

The self-check confirms the intentionally failing fixture baseline. The verifier checks all eight saved cases, source hashes, immutable review workspaces, repair results, answer preservation, worker evidence, and token totals. It also reproduces the arithmetic counterexample and confirms that each saved review has an editorial score; the scores themselves remain an inspection, rather than something this script can prove. Given a fresh `local-results/<timestamp>` directory, the verifier skips the checks that apply only to the published set: exactly eight runs, the six exclusions, and the editorial scores.

To run the full eight-case comparison again using the measured model selections:

```sh
node topics/subagents/experiments/run.mjs \
  --codex-model gpt-6.1-sol \
  --claude-model claude-sonnet-5-5
```

New output goes to ignored `local-results/<timestamp>/`. Narrow a run with `--product codex|claude`, `--task review|implement`, and `--mode single|delegated`. Use `--out /absolute/output/directory` to choose another output location and `--timeout-seconds` to change the per-case 240-second default. Review the dry run first; live runs consume account usage.

Each case saves `prompt.txt`, `record.json`, `events.jsonl`, `stderr.txt`, `answer.txt`, and `workspace/`. Text answers preserve the original Markdown as plain text, including original workspace-relative file references. Canonical fixture paths and the home directory are replaced with placeholders in exported event text. Internal reasoning blocks and signatures are omitted; tool evidence and usage remain. Authentication files and full private session transcripts are not copied. Codex normally persists these benchmark sessions in its own session directory so the evidence collector can read them.

If a CLI fails, times out, lacks a final answer, or lacks successful delegation evidence, the runner saves the record and stops. A recovered permission denial remains a recorded event. Incorrect answers and failed behavioral checks are measurements to retain, not reasons to keep rerunning until a favorable outcome appears.

## Limits and next useful comparison

The two tasks use the same tiny source fixture, so they are not independent samples of real repository work. There is one observation per condition, fixed run order, uncontrolled provider load and caching, and no equal-total-token budget. The study also fixes the worker count at two and does not sweep models, effort, handoff quality, or dependency structure. Normal product prompts and tool surfaces differ between the CLIs. These controls support a within-product illustration of overhead, not a causal decomposition of every cost or a cross-product ranking.

The results favor keeping these particular tasks in one agent; they do not establish that delegation fails on larger research or implementation work. A useful next study would preselect larger independent tasks and a sequential dependency task, repeat paired runs in alternating order, and compare both unconstrained and equal-budget conditions. Keep the same outcome checks and disclose failed runs.

## Sources

- [Fixture specification](fixture/SPEC.md), [runner](run.mjs), [grader](grade.mjs), [evidence collector](codex-evidence.mjs), and [saved-result verifier](verify.mjs)
- [Measured records and output workspaces](results/2026-10-16/summary.json)
- [Excluded setup runs](results/2026-10-16/excluded-setup.json) and [post-run editorial assessment](results/2026-10-16/editorial-assessment.json)
- [Claude Code: CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Claude Code: Cost accounting](https://code.claude.com/docs/en/costs)
- [Claude Agent SDK: Cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)
- [OpenAI: Subagents and configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents)

The local artifacts support the numerical results and runtime observations. Vendor documentation supports the configuration and accounting interpretation. Neither replaces an independent evaluation on representative work.
