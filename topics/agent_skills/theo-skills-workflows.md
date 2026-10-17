# From repository rules to focused skills: Theo’s workflow in practice

| Field | Value |
| --- | --- |
| Researched | 2026-10-17 |
| Configuration walkthrough | [My AGENTS.md & SKILLS.md Breakdown (Don’t copy them)](https://www.youtube.com/watch?v=e1snsuY4lTI), Theo — t3.gg, 2026-08-11; 51:15 |
| Skill review | [So I tried Matt’s skills…](https://www.youtube.com/watch?v=0oXOOlqVu5M), Theo — t3.gg, 2026-08-19; 38:21 |
| Question | Which ideas from these workflows are useful to adapt, and what evidence would justify keeping them? |
| Companion | [Evidence behind the earlier “delete CLAUDE.md” video](repository-instructions-evidence.md), including the original and revised studies. |

The useful idea across these videos is to **turn recurring problems into narrowly applicable guidance, then check whether the guidance changes the result**. The August examples extend the February discussion toward communication, shared terminology, and reviewable work. The public files make these mechanisms inspectable; they do not establish a measured productivity improvement for every reader.

The walkthrough distinguishes personal global preferences from repository instructions and task-specific skills. The later review samples Matt Pocock’s collection and Cursor’s pstack. Both emphasize adapting a selection to actual work. Theo keeps a personal configuration library that is synced across several machines. It is not published in the walkthrough, so its complete contents and reported effects cannot be independently audited here. [Configuration discussion](https://www.youtube.com/watch?v=e1snsuY4lTI&t=270), [skill review](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=194)

## How the three videos fit together

| Video | Main question | Evidence available |
| --- | --- | --- |
| February: deleting instruction files | Does loading repository guidance improve coding-task outcomes? | A discussion of a benchmark, plus a live example. The [companion report](repository-instructions-evidence.md) checks the paper and later revisions. |
| August 11: configuration walkthrough | How should personal preferences and project-specific expectations be expressed? | An author walkthrough, Theo’s review of past agent sessions, and a public repository example. |
| August 19: trying external skills | Which reusable workflows fit an existing way of working? | Source inspection, demonstrations, and personal judgments. |

These address different outcomes. A test-suite score can measure whether a patch passes a benchmark. It will not necessarily reward an explanation that takes less effort to understand, a better requirements interview, or a clearer PR. Those outcomes need their own criteria. The context-file study explicitly leaves broader quality questions open, while SkillsBench evaluates curated task procedures under executable verifiers. [Context-file limitations](https://arxiv.org/html/2602.11988v3#S5), [SkillsBench evaluation](https://arxiv.org/html/2602.12670v4#S4)

## Put each kind of knowledge where it applies

Global preferences affect many projects, so each entry should make sense across those projects. Repository instructions can describe local meaning and constraints. A skill supplies a procedure for a particular class of work. Tests and tools provide feedback about what actually happened.

| Location | Useful contents | Example and reason |
| --- | --- | --- |
| Personal global guidance | Stable communication preferences and working agreements. | How to explain a result or distinguish a question from an edit request. A project-specific directory map does not belong here. |
| Repository instructions | Domain terms, product invariants, unusual commands, and operational facts. | T3 Code distinguishes the maintainer’s live runtime state from disposable development state and lists the clients a feature may affect. |
| A skill and its references | A task-specific sequence, examples, scripts, and completion criteria. | A debugging procedure can require an executable reproduction before accepting a fix. |
| Tooling and verification | Observable success and failure. | A command that exercises the reported bug provides feedback beyond a plausible explanation. |

The public T3 Code snapshot is a useful concrete example. Its glossary distinguishes the person controlling an agent from the agent itself, and defines terms such as environment, project, and thread. Its feature checklist includes alternate entry points, web/desktop/mobile clients, provider adapters, wire contracts, and reverse operations such as undoing a state change. These entries express the intended behavior of changes. [T3 Code instructions, August 11 snapshot](https://github.com/pingdotgg/t3code/blob/560d4a4560ddb5f42c8f8e0e35fa7827c0e46f80/AGENTS.md)

That file also contains preferences about process and verification. Those are rules for that project. Their presence is evidence of the maintainers’ intended workflow, not proof that another repository should adopt the same commands, test policy, or approval boundaries.

## Descriptions route work; instructions carry the procedure

A skill’s description helps the agent decide whether to load it. The portable specification asks for a description of what the skill does and when to use it. A good description therefore identifies both the capability and the applicable task. A list of broad trigger words can make the agent select the skill for unrelated work. [Agent Skills specification](https://agentskills.io/specification)

For an illustrative migration-review skill, this description is too broad because ordinary query work also matches it:

```yaml
description: Help with databases, queries, schemas, and backend work.
```

A narrower description names the job and the boundary of its use:

```yaml
description: Review a database migration and its rollout. Use when adding, changing, or reviewing a migration, not for ordinary query work.
```

The description does not need to contain the review checklist. That belongs in the skill body, with specialized references loaded only when relevant. Matt’s `writing-for-agents` calls this kind of routing reference a context pointer; it also separates the cost of loaded guidance from the effort required for a person to remember which workflow to invoke. Those are useful design concepts, rather than independently established numerical laws about model attention. [Writing for agents](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/productivity/writing-for-agents/SKILL.md)

Invocation controls need a separate check. Product behavior below was verified on 2026-10-17:

| Product | Documented control | Practical implication |
| --- | --- | --- |
| Claude Code | `disable-model-invocation: true` in `SKILL.md` prevents automatic invocation; the user can still invoke the skill. | A manual workflow need not become the agent’s default response to a broad prompt. [Claude Code skills](https://code.claude.com/docs/en/skills) |
| Codex | `policy.allow_implicit_invocation: false` in `agents/openai.yaml` prevents implicit invocation while keeping explicit `$skill` use. | Use the documented Codex control instead of assuming a Claude-specific field transfers. [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) |

At the pstack revision inspected here, `unslop`, `arena`, `blast-radius`, and `show-me-your-work` all declare `disable-model-invocation: true`, so an untouched installation should run them only when the user calls them by name. A demonstration in which one of them appears to start on its own does not show how a fresh installation behaves: Theo’s configuration, the product, and the skill version may all differ from what is pinned here. [Pinned pstack files](https://github.com/cursor/plugins/tree/ac4e25a0064cd600afdd605208bad72748cb019a/pstack/skills)

## Candidate workflows, organized by the problem they address

The following are candidates to evaluate. A source file establishes what its author asks an agent to do; it does not establish the size of any resulting improvement.

| Repeated problem | Candidate | Mechanism to inspect | Cost or limitation to test |
| --- | --- | --- | --- |
| Requirements remain ambiguous. | Matt’s [`grill-with-docs`](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/engineering/grill-with-docs/SKILL.md) | Combines a structured interview with domain modeling and decision records. | Many rounds of questions can add unnecessary work to a well-specified task. |
| Explanations are difficult to read. | pstack’s [`unslop`](https://github.com/cursor/plugins/blob/ac4e25a0064cd600afdd605208bad72748cb019a/pstack/skills/unslop/SKILL.md) | Rewrites vague, mannered, or inflated prose while preserving meaning. | A style pass must preserve uncertainty and technical details. Check for lost facts, not only smoother sentences. |
| One answer needs clarification. | Matt’s [`wait-what`](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/productivity/wait-what/SKILL.md), pstack’s [`bro`](https://github.com/cursor/plugins/blob/ac4e25a0064cd600afdd605208bad72748cb019a/pstack/skills/bro/SKILL.md) | Re-explains the preceding message in plainer language. | Repairing an answer does not prevent the next confusing answer. Shared vocabulary may address the recurring cause. |
| Debugging produces plausible fixes without a reproduction. | Matt’s [`diagnosing-bugs`](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/engineering/diagnosing-bugs/SKILL.md) | Builds an executable feedback loop, reproduces and minimizes the failure, tests hypotheses, then verifies the fix. | Its gated process may be excessive for a simple, already-reproduced error. |
| A small change breaks another path. | pstack’s [`blast-radius`](https://github.com/cursor/plugins/blob/ac4e25a0064cd600afdd605208bad72748cb019a/pstack/skills/blast-radius/SKILL.md) | Follows effects beyond direct callers and asks for executable evidence of the key safety assumption. | A convincing write-up still needs the claimed evidence. Broad changes can require substantial investigation. |
| An unattended run is hard to review. | pstack’s [`show-me-your-work`](https://github.com/cursor/plugins/blob/ac4e25a0064cd600afdd605208bad72748cb019a/pstack/skills/show-me-your-work/SKILL.md) | Records decisions, reasons, evidence pointers, and outcomes in a TSV log. | Logging and review add work. The log records observable decisions; it does not reveal an authoritative internal reasoning trace. |
| A human must complete external setup steps. | Matt’s [`wizard`](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/engineering/wizard/SKILL.md) | Generates a staged script around an existing template, with explicit human actions and captured values. | Depends on the template and current service instructions. Its stages need review before execution. |
| The first design may choose the wrong structure. | pstack’s [`arena`](https://github.com/cursor/plugins/blob/ac4e25a0064cd600afdd605208bad72748cb019a/pstack/skills/arena/SKILL.md) | Produces independent candidates, judges them against a rubric, selects a base, integrates useful alternatives, and verifies the result. | Candidate runs, judging, integration, and final verification all add cost. Agreement between models does not establish correctness. |

Some skills organize a larger workflow. Matt’s architecture-review skill depends on shared design vocabulary, produces candidate refactors, and asks which one to explore before moving into a requirements interview. The repository also offers planning, ticketing, implementation, and review components. It is reasonable to adopt a useful component without committing every task to the entire sequence. [Architecture review](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/engineering/improve-codebase-architecture/SKILL.md), [collection reference](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/README.md)

Teaching is another distinct activity. Matt’s `teach` maintains a learning workspace with a mission, resources, lessons, and learning records. It assumes an ongoing learning relationship. It would impose a different process from a one-off explanation, so its applicability should be explicit. [Teaching skill](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/productivity/teach/SKILL.md)

## A small skill can have a large dependency chain

The August snapshot’s `grill-with-docs` body is only a request to invoke `grilling` and `domain-modeling`. The former runs rounds of questions whose prerequisites have been settled; the latter checks and records terminology and offers architectural decision records when the trade-off warrants one. Copying only the wrapper loses that behavior. [Wrapper](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/engineering/grill-with-docs/SKILL.md), [interview](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/productivity/grilling/SKILL.md), [domain modeling](https://github.com/mattpocock/skills/blob/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/engineering/domain-modeling/SKILL.md)

Dependencies can also include supporting files and product-specific tools. `wizard` refers to a script template. `show-me-your-work` includes a log template and helper, then references other skills for review. `arena` expects Cursor configuration and agent-tool behavior. A short Markdown file is therefore not a complete estimate of installation effort, runtime behavior, or inference cost.

Before trying a candidate, read the invoked skills and referenced files, identify external services and write operations, and verify that the target product can perform the named operations. A text-only prompt pasted into a chat can test its wording. It cannot test installed discovery, missing assets, metadata handling, or authorization behavior.

For a customized copy, record the upstream repository, commit, imported files, and local changes. For a managed bundle, check what updates automatically. The repository’s [storage and distribution guide](storage-and-distribution.md) and [shared skill-repository walkthrough](backup-and-restore.md) cover those maintenance choices.

## Review the outcome each workflow claims to improve

A clearer answer is useful, but readability and factual correctness are separate outcomes. In the skill-review video, the writing comparison crosses different application contexts; it does not isolate a single file under a controlled experiment. Personal history audits also reflect the tasks assigned to each model. A model used for harder work can receive more corrections without being worse at comparable tasks. These observations are useful for forming local hypotheses. [Writing demonstration](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=563), [history audit](https://www.youtube.com/watch?v=e1snsuY4lTI&t=1140)

The practical evaluation should match the claimed benefit:

| Claimed benefit | Useful observation |
| --- | --- |
| Clearer explanations | Can a reader correctly explain the result and its limitations with fewer follow-up questions? |
| Better requirements | Do recorded decisions cover the disagreements that would otherwise cause rework? |
| Better debugging | Does the original symptom reproduce before the fix and stop reproducing afterward? |
| Better integration review | Are real cross-component failures found, with evidence that a reviewer can rerun? |
| Better multi-candidate design | Does the final artifact beat the single-run baseline under a rubric chosen before seeing the candidates, after accounting for cost? |

The companion report’s [evaluation plan](repository-instructions-evidence.md#a-small-evaluation-for-a-real-repository) supplies a starting method: freeze conditions, compare the same tasks, repeat attempts, and retain separate measures of quality, review effort, time, and usage. Benchmark gains from curated SkillsBench packages do not establish that these particular collections improve every workload. [SkillsBench limitations](https://arxiv.org/html/2602.12670v4#S6.SS1)

## Worked example: archive means something specific

Consider a hypothetical project with web and mobile clients. A developer asks for an archive action. The team means hiding a project from the active list while preserving its records and allowing restoration. An agent could implement hiding correctly but omit restoration or update only one client.

A focused workflow would establish the meaning first, record “archive” and “restore” in a glossary, and add a repository instruction that changes to this lifecycle must account for both clients and both operations. A debugging or integration-review skill would then inspect the actual paths and verify that restoration exposes the preserved records. A writing skill could explain the result using the same terms.

The outcome to measure is concrete: both clients can archive and restore the same project, its records remain intact, and the explanation accurately states the behavior. A longer design document or a more fluent explanation alone would not satisfy that criterion. The example shows how shared language, scoped instructions, task procedures, and executable feedback can complement one another; it is not a measured result.

For this research repository, an additional general writing skill would overlap with the existing explanatory-writing guidance. A useful trial would compare against that existing baseline and inspect specific remaining failures before adding another layer.

## Appendix: all chapters in the configuration walkthrough

These tables retain the chapter order and timestamps supplied by YouTube. Topic labels are paraphrased. They are navigation aids; individual caption passages may span a different boundary. The walkthrough ends at 51:15.

| Listed start | Topic | Research connection |
| --- | --- | --- |
| [00:00](https://www.youtube.com/watch?v=e1snsuY4lTI&t=0) | Recent workflow changes | Personal observations; context in [how the videos fit together](#how-the-three-videos-fit-together). |
| [01:29](https://www.youtube.com/watch?v=e1snsuY4lTI&t=89) | WorkOS advertisement | [Sponsor documentation](https://workos.com/docs). |
| [02:54](https://www.youtube.com/watch?v=e1snsuY4lTI&t=174) | Machine configuration library | Distribution and scope; see [where each kind of knowledge applies](#put-each-kind-of-knowledge-where-it-applies). |
| [05:40](https://www.youtube.com/watch?v=e1snsuY4lTI&t=340) | Personal defaults | Global guidance in [where each kind of knowledge applies](#put-each-kind-of-knowledge-where-it-applies). |
| [08:14](https://www.youtube.com/watch?v=e1snsuY4lTI&t=494) | Communication preferences | Criteria for clearer explanations in [outcome review](#review-the-outcome-each-workflow-claims-to-improve). |
| [08:55](https://www.youtube.com/watch?v=e1snsuY4lTI&t=535) | Process choices | When a workflow applies; see [descriptions and invocation](#descriptions-route-work-instructions-carry-the-procedure). |
| [10:06](https://www.youtube.com/watch?v=e1snsuY4lTI&t=606) | PR preparation and monitoring | Task procedures as skills; see [where each kind of knowledge applies](#put-each-kind-of-knowledge-where-it-applies). |
| [14:16](https://www.youtube.com/watch?v=e1snsuY4lTI&t=856) | Reviewable descriptions | Reader comprehension as an outcome; see [outcome review](#review-the-outcome-each-workflow-claims-to-improve). |
| [16:20](https://www.youtube.com/watch?v=e1snsuY4lTI&t=980) | Model observations | Why task mix limits model comparisons; see [outcome review](#review-the-outcome-each-workflow-claims-to-improve). |
| [17:09](https://www.youtube.com/watch?v=e1snsuY4lTI&t=1029) | Past-run inspection | History audits as local hypotheses; see [outcome review](#review-the-outcome-each-workflow-claims-to-improve). |
| [21:24](https://www.youtube.com/watch?v=e1snsuY4lTI&t=1284) | Shared terminology | Glossaries in the [archive example](#worked-example-archive-means-something-specific) and [dependency chain](#a-small-skill-can-have-a-large-dependency-chain). |
| [22:41](https://www.youtube.com/watch?v=e1snsuY4lTI&t=1361) | Convex advertisement | [Sponsor documentation](https://docs.convex.dev/). |
| [24:14](https://www.youtube.com/watch?v=e1snsuY4lTI&t=1454) | Project-specific guidance | Public T3 Code snapshot in [where each kind of knowledge applies](#put-each-kind-of-knowledge-where-it-applies). |
| [31:18](https://www.youtube.com/watch?v=e1snsuY4lTI&t=1878) | Changes across clients | Cross-client coverage in the [archive example](#worked-example-archive-means-something-specific). |
| [34:26](https://www.youtube.com/watch?v=e1snsuY4lTI&t=2066) | Short task prompts | Reusable repository context; see [where each kind of knowledge applies](#put-each-kind-of-knowledge-where-it-applies). |
| [38:47](https://www.youtube.com/watch?v=e1snsuY4lTI&t=2327) | Host provisioning | Private workflow dependency; see the note below. |
| [41:00](https://www.youtube.com/watch?v=e1snsuY4lTI&t=2460) | File sharing and HTML | Human-readable artifacts; see the note below. |
| [45:55](https://www.youtube.com/watch?v=e1snsuY4lTI&t=2755) | Editing skills | Routing and references in [descriptions and invocation](#descriptions-route-work-instructions-carry-the-procedure). |
| [47:18](https://www.youtube.com/watch?v=e1snsuY4lTI&t=2838) | Distributing revisions | Recording upstream versions; see [dependency chain](#a-small-skill-can-have-a-large-dependency-chain). |

The private upload, HTML, and provisioning services are examples of the author’s setup, not reproducible packages supplied by this report. The WorkOS and Convex segments are advertising, not effectiveness evidence.

## Appendix: all chapters in the external-skill review

The review ends at 38:21. pstack’s writing standards and verification principles are directly inspectable in the pinned collection: [technical writing](https://github.com/cursor/plugins/blob/ac4e25a0064cd600afdd605208bad72748cb019a/pstack/skills/technical-writing/SKILL.md), [prove it works](https://github.com/cursor/plugins/blob/ac4e25a0064cd600afdd605208bad72748cb019a/pstack/skills/principle-prove-it-works/SKILL.md).

| Listed start | Topic | Research connection |
| --- | --- | --- |
| [00:00](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=0) | Collection overview | Pinned versions listed in [Sources](#sources). |
| [01:58](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=118) | Depot advertisement | [Sponsor documentation](https://depot.dev/docs). |
| [03:14](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=194) | Adapting workflows | Fit before adoption; see [candidate workflows](#candidate-workflows-organized-by-the-problem-they-address). |
| [04:16](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=256) | Selecting candidates | Candidates organized by repeated problem in [candidate workflows](#candidate-workflows-organized-by-the-problem-they-address). |
| [05:12](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=312) | Prose cleanup | `unslop` in [candidate workflows](#candidate-workflows-organized-by-the-problem-they-address). |
| [09:23](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=563) | Explanation comparison | Demonstration limits in [outcome review](#review-the-outcome-each-workflow-claims-to-improve). |
| [12:17](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=737) | Matt’s collection | Workflow components in [candidate workflows](#candidate-workflows-organized-by-the-problem-they-address). |
| [13:23](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=803) | Requirements interview | Wrapper dependencies in [dependency chain](#a-small-skill-can-have-a-large-dependency-chain). |
| [17:02](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=1022) | Engineering procedures | Debugging, architecture, and teaching in [candidate workflows](#candidate-workflows-organized-by-the-problem-they-address). |
| [21:47](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=1307) | Integrating selected skills | Maintenance of customized copies; see [dependency chain](#a-small-skill-can-have-a-large-dependency-chain). |
| [27:17](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=1637) | Agent-facing writing | Context pointers in [descriptions and invocation](#descriptions-route-work-instructions-carry-the-procedure). |
| [31:16](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=1876) | Candidate comparison and proof | `arena` and `blast-radius` in [candidate workflows](#candidate-workflows-organized-by-the-problem-they-address). |
| [34:03](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=2043) | Recording decisions | `show-me-your-work` in [candidate workflows](#candidate-workflows-organized-by-the-problem-they-address). |
| [36:04](https://www.youtube.com/watch?v=0oXOOlqVu5M&t=2164) | Choosing what to retain | Evaluation on actual tasks; see [outcome review](#review-the-outcome-each-workflow-claims-to-improve). |

## Sources

- [Theo — configuration walkthrough](https://www.youtube.com/watch?v=e1snsuY4lTI) and [external-skill review](https://www.youtube.com/watch?v=0oXOOlqVu5M): official metadata, description, chapters, and original-English automatic captions.
- [T3 Code repository instructions](https://github.com/pingdotgg/t3code/blob/560d4a4560ddb5f42c8f8e0e35fa7827c0e46f80/AGENTS.md), pinned to `560d4a4`, a snapshot dated 2026-08-11. This is a public comparison point, not a claim that every line exactly matches filming.
- [Matt Pocock’s collection](https://github.com/mattpocock/skills/tree/885e2ca4d842d139e9aef4e48d366c63cb1b8013), pinned to `885e2ca`, dated 2026-08-19. The linked skill files above use that snapshot. File names and conventions can change in later revisions.
- [Cursor pstack](https://github.com/cursor/plugins/tree/ac4e25a0064cd600afdd605208bad72748cb019a/pstack), pinned to `ac4e25a`, dated 2026-10-16 UTC, inspected on 2026-10-17. Its current invocation flags and model/tool assumptions are not attributed to the August video.
- [Agent Skills specification](https://agentskills.io/specification), [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills), and [Claude Code skill documentation](https://code.claude.com/docs/en/skills): packaging and product-specific invocation behavior.
- [Evaluating AGENTS.md, v3](https://arxiv.org/html/2602.11988v3) and [SkillsBench, v4](https://arxiv.org/html/2602.12670v4): research context, discussed in depth in the [companion report](repository-instructions-evidence.md).
- [WorkOS](https://workos.com/docs), [Convex](https://docs.convex.dev/), and [Depot](https://depot.dev/docs): sponsor documentation; advertising performance claims are not used as research findings.

## Method and limitations

Both complete automatic-caption transcripts were reviewed, together with the videos’ metadata and chapter inventories. Captions can misrecognize names; skill names and mechanisms above were checked against public files. The chapter tables preserve YouTube’s supplied boundaries rather than treating them as precise timecodes for every spoken claim.

Source inspection was selective around the workflows discussed here, not an audit of every skill in either collection. Public files are pinned; Theo’s private configuration library and the underlying history-audit corpus were unavailable. The two X posts linked in the skill-review description were not retrievable and are not used to establish provenance or effectiveness. Model rankings, AI-detector demonstrations, and subjective style preferences do not substitute for controlled comparisons.

The suggested checks and worked example are analysis, not measured outcomes. No skills were installed, no personal histories were inspected, and no agent-effectiveness comparison was run for this report. The portable skill file is named `SKILL.md`, despite `SKILLS.md` appearing in the walkthrough’s title.
