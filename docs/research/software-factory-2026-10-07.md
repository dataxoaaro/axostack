# The software factory, and where axostack fits

Researched 2026-10-07. Quotes marked † were extracted by a page summarizer rather than read from raw text. Check their wording before quoting them elsewhere.

## Takeaway

"Software factory" has meant four things since 1968: a disciplined organization for producing families of similar systems (SDC, Hitachi, Toshiba, NEC, Fujitsu), a development environment configured for one type of application (Microsoft, 2004), a DevSecOps pipeline platform (DoD, 2019 onward), and in 2026 a system of AI agents that turns signals or specs into shipped software with humans as governors. Across all four, a factory standardizes the process, reuses deliberately, automates with tools, controls quality, measures output, and improves the process itself. axostack covers the front half of the line in depth: intake, specification, planning, build, verification, and review, plus the standards. It lacks the back half and the plant machinery: unattended triggers, release and production feedback, a loop for PR review comments, and throughput metrics.

## Cited findings

### History

- McIlroy proposed a software components subindustry and a "components factory" at the 1968 NATO conference: "'Mass production' of software means multiplicity of what manufacturing industry would call 'models,' or 'sizes' rather than multiplicity of replicates of each." https://mcilroy.cs.dartmouth.edu/components.txt (talk October 1968, printed 1969).
- Bemer (GE), as quoted by Cusumano: "[A] software factory should be a programming environment residing upon and controlled by a computer... A factory... has measures and controls for productivity and quality." Cusumano, MIT Sloan WP 3325-91, 1991-08-26. https://dspace.mit.edu/server/api/core/bitstreams/1ec5521e-5ffe-4b0f-865d-2f1f74626858/content
- Cusumano's defining practices (same paper): "permanent development groups dedicated to particular families of products", "process R&D groups that develop or refine standardized methods and tools", "planned rather than 'accidental' or ad hoc reuse", "some divisions of labor", "common training programs", and "disciplined procedures for project management as well as product quality control". Factories aimed at "scope economies achieved through managing multiple design or engineering projects systematically, rather than treating each project or job as unique."
- SDC's factory (Santa Monica, about 200 programmers) combined "an integrated set of tools... standardized procedures and management policies... and a matrix organization." It failed on a fixed-price police project where "the requirements kept on expanding", and "SDC reverted to its former job-shop structure." Tool portability was also a cause. Cusumano, MIT Sloan WP 3095-89, 1989-12-05. https://dspace.mit.edu/handle/1721.1/47992
- Hitachi founded its Software Works in 1969, "the first company in the world to apply the term factory... to an actual software facility." Toshiba Fuchu introduced its factory organization in 1977, with policies to standardize the process, "reuse existing designs and code", use "standardized and integrated tools", and "provide extensive training." NEC founded its Basic Software Development Division in 1974. Fujitsu established a Software Factory Department in 1979. Same source, WP 3095-89.

### Microsoft Software Factories

- "A Software Factory is a development environment configured to support the rapid development of a specific type of application." Greenfield, "The Case for Software Factories", MSDN, July 2004. https://learn.microsoft.com/en-us/previous-versions/aa480032(v=msdn.10)
- A software factory "contains three key ideas: a software factory schema, a software factory template and an extensible development environment." The schema "specifies which DSLs should be used." The template "provides the patterns, guidance, templates, frameworks, samples, custom tools." The authors: "the term software factory is controversial." Greenfield and Short, "Moving to Software Factories", 2004-06-17 (marked paid advertisement). https://www.softwarefactories.com/ScreenShots/MS-WP-04.pdf
- The shipped factories were retired: the Web Service Software Factory in November 2011, and the Smart Client Software Factory 2010 page says "no new releases... are planned" and points to Prism. https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff699491(v=pandp.10), https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff709809(v=pandp.10)

### Government and DevSecOps factories

- DoD definition: "A software assembly plant that contains multiple pipelines, which are equipped with a set of tools, process workflows, scripts, and environments, to produce a set of software deployable artifacts with minimal human intervention. It automates the activities in the develop, build, test, release, and deliver phases." DoD Enterprise DevSecOps Fundamentals v2.0, March 2021 (read from the Wayback copy). https://dodcio.defense.gov/Portals/0/Documents/Library/DoDEnterpriseDevSecOpsFundamentals.pdf
- The Defense Innovation Board recommended: "Stand up one or more software factories within each Service." "Software Is Never Done", 2019-05-03. https://media.defense.gov/2019/May/01/2002126689/-1/-1/0/SWAP%20COMPLETE%20REPORT.PDF
- DoD had established "29 software factories", including Platform One, Kessel Run, the Navy's Forge, and the Army Software Factory. GAO-23-105611, 2023-04-05. https://www.gao.gov/products/gao-23-105611

### Agentic software factories (2025-2026)

- Dan Shapiro's five levels: at Level 4, "You write a spec. You argue with it about the spec. You craft skills (for Claude Code...)". At Level 5, "It's a black box that turns specs into software", "dark" because "humans are neither needed nor welcome." 2026-01-23. https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/
- StrongDM: "Code must not be written by humans" and "Code must not be reviewed by humans."† A factory is "non-interactive development where specs + scenarios drive agents that write code, run harnesses, and converge without human review."† Scenarios are end-to-end user stories stored outside the codebase, scored as "satisfaction", and run against a Digital Twin Universe of cloned third-party services. Undated, retrieved 2026-10-07. https://factory.strongdm.ai, https://factory.strongdm.ai/techniques. The blog adds "validation replaces code review."† 2026-02-19. https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai
- Factory (factory.ai, now factory.com): "The software factory starts with signals from the outside world: bug reports, internal conversations, customer feedback, business requirements. These signals get triaged and turned into planned changes. These changes are built, tested, reviewed, secured, shipped, and monitored."† Engineers "will be responsible for building the factories that build the software."† 2026-06-15. https://factory.com/news/software-factory
- Factory docs name the stages Triage, Code-gen, Validate, Release, Document, and Monitor, and the metrics Tickets Triaged, PR Validations, PRs Merged, and Incidents Processed.† Undated, retrieved 2026-10-07. https://docs.factory.com/software-factory/overview. Its headless mode, Droid Exec, is "for CI/CD pipelines and automation scripts", with autonomy levels from read-only up to `--auto high` for "remote writes, deployments, database migrations".† https://docs.factory.com/cli/droid-exec/overview. Automations trigger on "Schedule, Slack, GitHub, or webhook."† 2026-09-30. https://factory.com/news/automations
- OpenAI's harness-engineering team reports "0 lines of manually-written code", "Humans steer. Agents execute.", about 1,500 PRs from three engineers, and agents that "pull review feedback, respond inline, push updates, and often squash and merge their own pull requests." The post does not use the word factory. https://openai.com/index/harness-engineering/ (dated 2026-02-11 from search snippets only).
- Steve Yegge: "A dark factory is any system in which coding agents are set up to work autonomously without humans watching... Observability is a choice in dark factory design." "Welcome to Gas City", 2026-04-24 (read via his RSS feed).
- Adjacent tools describe the same issue-to-PR line without the word factory: Claude Code GitHub Actions turns "issues into pull requests", responds to PR review comments, and runs on any event including cron, while advising "review Claude's changes before merging." https://code.claude.com/docs/en/github-actions (live 2026-10-07). GitHub Spec Kit's phases are Specify, Plan, Tasks, and Implement. 2025-09-02. https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/

### Common station model

Combining Factory's stages, the DoD pipeline phases, and Cusumano's practices gives nine stations and four cross-cutting functions:

1. Intake and triage of signals
2. Specification of intent
3. Planning and decomposition
4. Build
5. Verification and quality control
6. Review
7. Integration and release
8. Monitoring and production feedback
9. Process improvement (Cusumano's process R&D group)

Cross-cutting: standards and methods, tooling and orchestration, reuse and product lines, and metrics.

## Inferences

These are my conclusions, drawn from the findings above and from this repo.

| Station | What a factory does there | axostack skills (file:line) | Coverage |
|---|---|---|---|
| Intake and triage | Listens for bugs, feedback, and requests and turns them into work | `/to-linear-issue` (`skills/axo-mode/SKILL.md:30`), `/triage` (`:32`), `/research-idea` (`:19`) | Partial. A person starts every intake. Nothing listens to Slack, error trackers, or customer feedback. |
| Specification | Captures intent before any code | **grilling** and `/grill-with-docs` (`:18`), **domain-modeling** (`:48`), **plan** (`:20`) | Full. Deeper than most factories. No scenario set held outside the codebase, as StrongDM uses. |
| Planning and decomposition | Splits intent into units with dependencies | **plan** (`:20`), **to-tickets** (`:31`), `/wayfinder` (`:38`), **architect** | Full |
| Build | Workers produce the change | **implement** (`:34`), **tdd** (`:25`), `/implement-spec` (`:35`), `/idea-to-pr`, **swarm** and **arena** (`:39`) | Full inside a session |
| Verification and QC | Proves the change works | **tdd**, `/create-verification-skill` (`:43`), **blast-radius** (`:27`), **security-audit** (`:28`), **benchmark-checklist** (`:29`), **principle-prove-it-works** | Partial. Strong per change. No digital twins or scenario scoring. |
| Review | Independent check before merge | **code-review** and **no-comments** (`:47`), the independent reviews in `skills/idea-to-pr/SKILL.md:64` | Partial. Agent review is thorough. Incoming human or bot PR comments have no handler. |
| Integration and release | Merges, releases, deploys | Committing playbook (`skills/axo-mode/playbooks/committing.md:6`), **pr** (`skills/axo-mode/SKILL.md:46`), the integration branch in `skills/implement-spec/SKILL.md:39` | Partial. The line stops at a PR. No merge, release, or deploy station. |
| Monitoring and feedback | Watches production and feeds incidents back to intake | **why** reads observability for history only | None |
| Process improvement | Refines the methods and tools | `/reflect` (`skills/axo-mode/SKILL.md:42`), **principle-encode-lessons-in-structure**, `scripts/check-skill-refs.py` in CI (`.github/workflows/checks.yml:14`), the upstream audits in `docs/research/` | Partial. Runs when a person asks. Nothing is learned automatically across runs. |
| Standards and methods | One way of working for everyone | **axo-mode** principles and playbooks, **technical-writing**, **unslop** | Full |
| Tooling and orchestration | Runs the line without a person present | **show-me-your-work** (`:40`) for audit trails, the run record in `skills/implement-spec/SKILL.md:34` | None for unattended runs. Everything starts in an interactive session. |
| Reuse and product lines | Reuses designs and code across a product family | The skills library itself | Partial. Reuses process, not code. |
| Metrics | Measures throughput and quality | **benchmark-checklist** for performance numbers only | None |

**Where axostack sits.** It matches Shapiro's Level 4: you write a spec, argue with it, and craft skills. In Greenfield's terms it is a factory template, made of guidance, patterns, and tools, configured for a kind of work rather than a type of application. `/reflect` and the upstream audits play the role of Cusumano's process R&D group.

**Gaps, in order of impact:**

1. No unattended operation. Factory's Droid Exec and Claude Code GitHub Actions run on schedules, webhooks, and CI events. Every axostack skill needs a person to start a session.
2. The line ends at the PR. Nothing handles review comments, merges, releases, deploys, or monitors production and feeds incidents back to intake.
3. No metrics. Factories count tickets triaged, PRs merged, lead time, and escaped defects. axostack measures nothing about its own output, so `/reflect` works from anecdote.
4. No holdout validation. StrongDM keeps scenarios outside the codebase so agents cannot fit their tests to their code. axostack's tests are written by the same agent that writes the code.

**Deliberate departures from the dark factory:**

- A human approves every push (`skills/axo-mode/playbooks/committing.md:10`, `skills/axo-mode/SKILL.md:96`). StrongDM forbids human review. `/idea-to-pr` is the one exception, where the request itself authorizes the push (`skills/idea-to-pr/SKILL.md:19`).
- Specification is interactive. Grilling (`skills/axo-mode/SKILL.md:18`) and ticket approval (`skills/to-tickets/SKILL.md:55`) keep a person in the loop on intent. SDC's factory collapsed because "the requirements kept on expanding". Front-loading the argument about intent addresses that failure, and it fits StrongDM's "Shift Work" split between interactive and fully specified work.
- Review is bounded. `/implement-spec` runs one broad review and one fix pass (`skills/implement-spec/SKILL.md:52`) instead of OpenAI's open-ended agent-to-agent review loop.

## Gaps

- GAO-23-105462 does not exist at gao.gov. The GAO report on software factories is GAO-23-105611.
- Not read: DoD DevSecOps Reference Design v1.0 (2019) and Fundamentals v2.5 (2024), because the downloads failed. Bratman and Court (1975) is paywalled and cited only through Cusumano. Greenfield and Short's 2004 book is cited only through Wikipedia.
- The OpenAI post's date comes only from search snippets. Yegge's original "Welcome to Gas Town" post is reachable only through secondary sources.
- No first-party use of "software factory" was found from Anthropic, GitHub, or Cognition. The Cognition phrase appears only on a third-party event page.
- StrongDM's "holdout set" wording appears only in Simon Willison's write-up (2026-02-07). The Attractor and CXDB repositories were not read.
- The AI-tooling sources from January to May 2026 (Shapiro, OpenAI, Yegge, Cognition) are older than three months and were not rechecked.
