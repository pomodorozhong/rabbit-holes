# Should you delete CLAUDE.md? Evidence behind Theo’s video

| Field | Value |
| --- | --- |
| Researched | 2026-10-17 |
| Video | [Delete your CLAUDE.md (and your AGENT.md too)](https://www.youtube.com/watch?v=GcNu6wrLTJc), Theo — t3.gg, published 2026-02-23; 29:15 |
| Question | When do repository instruction files and agent skills improve results enough to justify their cost? |
| Scope | The video’s claims, the original and revised studies, current product documentation, and an evaluation plan for a real repository. |

The evidence supports **keeping instructions that supply useful project knowledge or change a necessary decision, then evaluating their effect**. It gives much less support to generating a repository summary and assuming that loading it into every task improves performance. The strongest result in the revised context-file study is higher inference cost; its success-rate differences against having no instruction file are not statistically significant. A separate benchmark finds substantial gains from curated procedural skills. [Context-file study, v3](https://arxiv.org/html/2602.11988v3#S4), [SkillsBench, v4](https://arxiv.org/html/2602.12670v4#S5)

This makes the video a useful reason to audit accumulated guidance. It does not establish that every repository should delete its instructions. The standard filename discussed below is `AGENTS.md`; the video title uses the singular `AGENT.md`.

Theo’s later configuration walkthrough and review of Matt Pocock’s skills develop the practical side of that question. [From repository rules to focused skills](theo-skills-workflows.md) examines those two videos, pinned public examples, and the limits of their demonstrations.

## What the context-file study actually tested

An instruction file can contain several different kinds of information. A directory map describes what the agent could discover by searching. A project convention supplies a decision the code may not explain. A command such as “run the parser tests with this fixture loader” can prevent a specific failure. Loading all three into the same prompt does not make them equally valuable.

Gloaguen and colleagues evaluated four model–agent combinations: Claude Code with Sonnet 4.5, Codex with GPT-5.2, Codex with GPT-5.1 mini, and Qwen Code with Qwen3-30B-Coder. Each task and condition received one sampled attempt. These are the configurations tested in the paper, rather than a comparison of the products’ October 2026 defaults. [Experimental setup](https://arxiv.org/html/2602.11988v3#S4.SS1)

| Dataset | Tasks and repositories | Available comparisons |
| --- | --- | --- |
| SWE-bench Lite | 300 tasks from 11 popular Python repositories | No instruction file versus an agent-generated file. |
| AGENTbench in v1; renamed CTXbench in v3 | 138 tasks from 12 Python repositories with developer-committed instruction files | No file, an agent-generated file, and the repository’s existing developer-provided file. |

In the no-file condition, agents still had the repository, ordinary documentation, and their normal harness instructions. The generated files came from the agents’ recommended initialization workflows. Developer-provided files came from the repository state before the reference change. “Developer-provided” identifies their source; it does not prove that every sentence was written without AI assistance. Success meant that the produced patch passed the evaluation tests. The researchers also measured tool steps and inference cost. [Original study](https://arxiv.org/html/2602.11988v1#S4.SS1), [revised study](https://arxiv.org/html/2602.11988v3#S3)

The smaller-repository benchmark required additional construction work: agents helped refine task descriptions and generate regression tests, with reference patches used to validate the tests and humans reviewing the results. The tasks are grounded in historical repository changes, while their generated specifications and tests can still miss intended behavior. Passing these tests does not measure every aspect of maintainability, security, or a team’s preferred workflow. The authors explicitly leave several of those outcomes for future work. [Benchmark construction](https://arxiv.org/html/2602.11988v3#S3), [limitations](https://arxiv.org/html/2602.11988v3#S5)

## The revised result is more careful than the headline

The February paper’s introduction summarized developer-provided files as improving performance by about 4% and generated files as reducing it by about 3%. Those are the authors’ original headline percentages. Its detailed results already showed that generated files reduced success in five of eight model–dataset settings, rather than every setting. [Study v1](https://arxiv.org/html/2602.11988v1#S1)

The latest version available for this review, **v3 dated 2026-09-29**, adds an explicit statistical comparison. Its Table 3 reports:

| Success-rate comparison | Reported p-value | What the comparison supports |
| --- | --- | --- |
| Generated file versus no file, SWE-bench | 0.87 | No statistically significant success-rate difference. |
| Generated file versus no file, CTXbench | 0.37 | No statistically significant success-rate difference. |
| Developer-provided file versus no file, CTXbench | 0.21 | The small average improvement is not statistically significant. |
| Developer-provided versus generated file, CTXbench | 0.038 | Developer-provided files perform better in this comparison at the conventional 0.05 threshold. |

These are the paper’s pooled comparisons across configurations. A non-significant result does not prove that the two approaches are equivalent, and the significant developer-versus-generated comparison does not establish an improvement over the no-file baseline. [Revised Table 3 and results](https://arxiv.org/html/2602.11988v3#S4.SS2)

The cost result is clearer. Generated files increased average per-task inference cost by **20% on SWE-bench and 23% on CTXbench**, with statistically significant increases. Developer-provided files also increased average steps and cost. These figures measure the study’s inference spending; they are not a universal wall-clock slowdown or a prediction for a subscription bill. [Revised results and Table 2](https://arxiv.org/html/2602.11988v3#S4.SS2)

For a team deciding what to keep, this changes the question. The useful comparison is whether a particular instruction prevents enough mistakes or preserves enough required behavior to justify the additional work it causes.

## Why instructions can add work without improving the measured result

The trace analysis found that agents usually followed the instructions. They tested more, explored more files, and used named project tools more often. For example, mentioning `uv` was associated with about 1.6 uses per task, compared with fewer than 0.01 when it was absent. The weak accuracy result therefore cannot simply be explained by agents ignoring the file. Instructions changed what they did. [Behavioral analysis](https://arxiv.org/html/2602.11988v3#S4.SS3)

That extra activity may be appropriate. A test that catches a rare integration failure can matter even if this benchmark does not reward it. The study shows a cost and an absence of established success gains under its scoring; deciding that every additional check was wasted would require a broader quality evaluation.

The researchers also measured how quickly agents first touched a file modified by the reference patch. Repository overviews did not meaningfully improve that measure. In a separate experiment, they removed other documentation after generating the context files; generated files then became more helpful. This supports the explanation that much of the generated content duplicated information already available in the repository. It does not suggest that removing good documentation is a useful optimization. [Overview analysis](https://arxiv.org/html/2602.11988v3#S4.SS3), [documentation ablation](https://arxiv.org/html/2602.11988v3#A2)

**Shorter is not itself a demonstrated cure.** The revision found no clear relationship between instruction-file length and accuracy or cost. Removing individual categories such as overview, tooling, or testing did not establish an accuracy improvement either. A reasonable interpretation is to inspect what an instruction makes the agent do and when it applies, rather than enforce an arbitrary word limit. [Additional ablations](https://arxiv.org/html/2602.11988v3#A2)

## Other evidence limits a universal deletion rule

### A smaller Codex study found efficiency gains

Lulla and colleagues studied 124 small changes across 10 repositories using Codex with `gpt-5.2-codex`. With an existing root `AGENTS.md`, median completion time fell from 98.57 to 70.34 seconds, a **28.64% reduction**; median output tokens fell by **16.58%**. The changes were restricted to at most 100 added or deleted lines across at most five files. [Efficiency study, v2](https://arxiv.org/html/2601.20404v2#S3)

This is meaningful contrary evidence about efficiency, with a narrower quality check. The researchers manually inspected outputs for 50 tasks to rule out obvious empty or irrelevant work; they did not perform a comprehensive correctness evaluation. The results therefore cannot establish that files make agents both faster and equally correct. Different models, repository samples, task sizes, instruction contents, and outcomes prevent a direct numerical comparison with CTXbench. [Metrics and results](https://arxiv.org/html/2601.20404v2#S3.SS1.SSS8)

### SkillsBench tests procedures rather than repository summaries

A skill can package a procedure, examples, scripts, and reference material for a class of tasks. That can supply knowledge beyond a directory map. SkillsBench pairs tasks with curated skills and executable verifiers, then compares the same model and agent harness with and without those skills. The original paper was linked in the video’s description; the expanded revision is relevant to a current recommendation. [SkillsBench v1](https://arxiv.org/html/2602.12670v1), [v4](https://arxiv.org/html/2602.12670v4#S4)

| Version | Evaluation scope | Authors’ reported average gain from curated skills |
| --- | --- | --- |
| v1, 2026-02-13 | 84 evaluated tasks; seven model–harness configurations. The inventory contained 86 tasks, with two excluded. | +16.2 percentage points. |
| v4, 2026-06-14 | 87 tasks; 18 model–harness configurations in the main paired comparison. | 33.9% to 50.5% pass rate: +16.6 percentage points. |

These gains apply to curated task packages. They do not estimate the value of an arbitrary skill downloaded from a directory. The current revision also reports weaker self-generated-skill results, but treats them as diagnostic: failures mix content quality with discovery problems and interference between authoring and solving. That is insufficient to conclude that automatic skill creation can never work. [Current main results](https://arxiv.org/html/2602.12670v4#S5.SS1), [self-generated condition](https://arxiv.org/html/2602.12670v4#A4.SS6)

The report’s skill-count analysis groups different tasks by how many skills they have. It is useful evidence for keeping bundles focused, but it does not establish a universal maximum of three installed skills: task difficulty and content differ across the groups, and installed catalogs are different from the skills attached to one benchmark task. The paper also calls for stronger controls to distinguish the value of procedural structure from simply providing more relevant context. [Skill design factors](https://arxiv.org/html/2602.12670v4#A6), [limitations](https://arxiv.org/html/2602.12670v4#S6.SS1)

Taken together, the studies make the **content, task, and agent stack** the useful unit of evaluation. They give little reason to treat a Markdown filename as either inherently beneficial or inherently harmful.

## Current product behavior matters

Repository files, skill catalogs, loaded skills, and tool definitions enter context through different mechanisms. Product details below were checked on 2026-10-17.

| Mechanism | Documented behavior | Consequence for an audit |
| --- | --- | --- |
| Codex repository instructions | Codex builds a chain from global guidance and directories from the project root to its working directory, with overrides, fallback names, and a size limit. | Inspect the actual chain, not just the root file. [OpenAI documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Claude Code instructions | Claude describes these as context rather than enforced configuration. It recommends concise instructions and moving specialized workflows into skills or scoped rules. | Keep project facts accurate; use enforced controls for requirements that must hold regardless of model choice. [Claude Code memory guide](https://code.claude.com/docs/en/memory) |
| Skills | The format separates initially listed metadata from instructions and supporting resources loaded when needed. | A large installed collection and a large active prompt are related but different problems. [Progressive disclosure](https://agentskills.io/specification#progressive-disclosure) |
| MCP tools with tool search | Anthropic’s API can defer tool definitions until discovery. | Check what the client actually loads before assuming every connected server’s full schema is always present. [Tool search documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) |

The video’s instruction hierarchy is an explanatory simplification. An `AGENTS.md` filename does not inherently confer developer-message priority: OpenAI’s Codex prompting guide documents user-role wrappers for discovered files. Product-specific loading rules matter. [Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)

Likewise, repeated context does not necessarily incur full input processing on every request. Prompt caching can reuse a stable prefix and reduce input cost and latency. It does not remove instructions from the model’s context or prevent them from triggering unnecessary actions. [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)

Current OpenAI guidance also recommends reviewing old instructions, narrowing skill triggers, and reading supporting documents when the task needs them. That is provider guidance, rather than an independent reproduction of the studies. [Rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

## What to keep, move, or remove

The following is a practical synthesis of the evidence, rather than a configuration tested in this repository.

| Content found during an audit | Useful action | Reason |
| --- | --- | --- |
| A generated list of folders and dependencies already documented elsewhere | Remove duplication unless testing shows that the summary helps. | It adds another document that can drift from the code. |
| A non-obvious project convention or repeated mistake | Keep a concrete instruction, with the reason and relevant scope. | The agent may be unable to infer the intended decision from existing code. |
| A command that silently omits a required check | Improve the command or feedback path; document any remaining exception. | Executable feedback can expose failure at the point it occurs. |
| A long procedure needed for one kind of task | Put it in a clearly triggered skill or linked reference. | Routine work need not load the whole procedure. |
| An old workaround for a previous model or architecture | Re-evaluate it on representative tasks. | Its original benefit may have disappeared. |
| A rule about permissions, deployment, or real user data | Keep the facts and boundaries explicit; enforce essential limits outside prose where possible. | A benchmark’s patch tests do not cover every operational consequence. |

For example, imagine a project where a schema experiment is authorized only on a disposable database. “This app has no users” would give the agent a false fact if the application is live. A useful instruction would say: “Use the disposable database for schema experiments. Production compatibility is required for changes proposed for deployment.” This expresses the allowed scope directly. It addresses the video’s suggestion to describe a project as greenfield to encourage experimentation without relying on that misleading premise. [Video, closing discussion](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=1590)

For this research repository, writing conventions and evidence requirements are examples of intended outcomes that a generic coding benchmark does not measure. Their value should be assessed against actual research tasks. This report does not change the repository’s active instructions.

## A small evaluation for a real repository

An **ablation** removes one component while holding other conditions steady. A useful pilot would compare the current guidance with a trimmed candidate and, where appropriate in an isolated environment, a condition with optional repository guidance absent. Keep required access controls and task authorization fixed.

1. **Choose representative tasks and success criteria first.** Include a small fix, a cross-file change, an unfamiliar subsystem, and a task where a project-specific convention matters. Reserve some tasks to check the final candidate rather than tune it.
2. **Freeze the starting conditions.** Record the repository commit, exact model and agent version, reasoning settings, enabled tools and skills, all loaded instruction sources, and relevant cache behavior. Use fresh sessions and independent disposable copies.
3. **Repeat each task under each condition.** Randomize order to reduce effects from service load and caching. A few repetitions can reveal obvious failures; a small pilot cannot establish that two approaches are equivalent.
4. **Score the result and the process.** Check functional correctness, convention adherence, review effort, failed commands, tool steps, elapsed time, and available token or cost records. Distinguish cached input, uncached input, and output where reported.
5. **Inspect the traces before editing again.** Keep a rule that prevents a required failure. Move narrowly relevant guidance out of the default prompt. Remove rules that add work without a useful outcome, then check the candidate on the reserved tasks.

This is a proposed method. No comparison of instruction configurations was run for this report.

## Appendix: coverage of all eight video chapters

The rows follow YouTube’s official chapter order; topic descriptions are paraphrased. The final chapter ends at 29:15.

| Starts | Chapter topic | Research treatment |
| --- | --- | --- |
| [00:00](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=0) | Opening challenge to instruction files | Compare the original claim with the revised statistical analysis. |
| [01:45](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=105) | Daytona sponsorship | Advertising for [agent sandboxes](https://www.daytona.io/docs/); separate from the study evidence. |
| [03:47](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=227) | Auditing existing repository guidance | Assess duplication and conventions through the study’s content analysis. |
| [05:57](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=357) | Context and instruction priority | Check loading, message roles, and caching against product documentation. |
| [11:51](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=711) | Prompting and feedback choices | Evaluate applicable instructions alongside executable checks. |
| [14:14](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=854) | Experimental findings | Separate success rates, statistical uncertainty, and inference cost. |
| [18:09](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=1089) | Repository design and live timing example | Treat the demonstration as an observation requiring repeated evaluation. |
| [25:00](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=1500) | Iterating on rules and agent setup | Consider skills, tool loading, and truthful task boundaries. |

In the live example, Theo reports 71 seconds without the generated file and 89 seconds with it: about 25.4% longer in that pair. One pair does not isolate the file’s causal effect or establish comparable answer quality. Wall-clock time also differs from the paper’s inference-cost metric. [Demonstration](https://www.youtube.com/watch?v=GcNu6wrLTJc&t=1260)

The introduction also mentions repeating prompts. The corresponding research concerns non-reasoning model calls; it does not establish that duplicating every coding-agent request improves a whole development workflow. [Prompt Repetition Improves Non-Reasoning LLMs](https://arxiv.org/abs/2512.14982)

## Sources

- [Theo — video](https://www.youtube.com/watch?v=GcNu6wrLTJc): official metadata, chapters, description, and English automatic captions.
- [Evaluating AGENTS.md — v1, 2026-02-12](https://arxiv.org/html/2602.11988v1): the version available when the video was published.
- [Evaluating AGENTS.md — v3, 2026-09-29](https://arxiv.org/html/2602.11988v3): revised statistical analysis, behavioral analysis, and ablations; [version history](https://arxiv.org/abs/2602.11988), [evaluation code](https://github.com/eth-sri/agentbench).
- [SkillsBench — v1, 2026-02-13](https://arxiv.org/html/2602.12670v1): the original study linked in the video.
- [SkillsBench — v4, 2026-06-14](https://arxiv.org/html/2602.12670v4): expanded paired evaluation and diagnostic self-generated-skill condition; [version history](https://arxiv.org/abs/2602.12670), [benchmark repository](https://github.com/benchflow-ai/skillsbench).
- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents — v2, 2026-03-30](https://arxiv.org/html/2601.20404v2): the contrasting efficiency study.
- [OpenAI — Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide), [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching), and [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): product behavior and provider advice checked on the research date.
- [Anthropic — Claude Code memory](https://code.claude.com/docs/en/memory) and [tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool): instruction scope and deferred tool definitions.
- [Agent Skills specification](https://agentskills.io/specification): packaging and progressive disclosure.
- [Prompt Repetition Improves Non-Reasoning LLMs](https://arxiv.org/abs/2512.14982): the separate research topic mentioned in the introduction.
- [Daytona documentation](https://www.daytona.io/docs/): the sponsor’s sandbox product, not evidence for the instruction-file claim.
- [Hacker News discussion](https://news.ycombinator.com/item?id=47034087): community discussion linked in the description; not treated as an independent experiment.

## Method and limitations

The video’s official title, publication date, description, chapter boundaries, and original-English automatic captions were retrieved and the complete caption transcript was reviewed. Automatic captions can misrecognize model names, so model identities and experimental details above come from the papers. The live example’s timings are speaker-reported observations, not independently reproduced measurements.

Primary papers and official documentation support the factual analysis. Historical versions are pinned so that later revisions are not attributed to a February video. Studies use different tasks, harnesses, metrics, and instruction contents; their effect sizes should not be averaged together. The recommendations and evaluation plan are a synthesis of that evidence. No local agent benchmark, sandbox deployment, or comparison of this repository’s instruction files was performed.
