# awesome-ai-coding-agents

> Honest comparison of AI coding assistants in September 2026. What each one does well, what it does badly, which to pick for your situation. No sponsored placements, no affiliate links, no paid rankings.

Maintained by [Brethof AI](https://brethof.ai). Companion to [awesome-llms-txt](https://github.com/BrethofAI/awesome-llms-txt) — this list goes deeper on one category.

---

## Quick decision tree

Pick by what matters to you. (Top to bottom — first match wins.)

- **Want the strongest all-around AI coding companion right now (September 2026)?** → **[Claude Desktop](#claude-desktop)**
- **Want the same Claude power but in your terminal / CI?** → **[Claude Code](#claude-code)**
- **Already pay for ChatGPT and want a terminal agent?** → **[OpenAI Codex CLI](#codex-cli)**
- **Want a capable terminal agent with a free tier?** → **[Gemini CLI](#gemini-cli)**
- **Want it free + open source?** → **[OpenCode](#opencode)** / **[Cline](#cline)** / **[Kilo Code](#kilo-code)** / **[Aider](#aider)**
- **Need to run 100% locally with your own LLM?** → **[OpenCode](#opencode)** / **[Cline](#cline)** / **[Qwen Code](#qwen-code)** / **[Aider](#aider)**
- **Already pay for GitHub and want zero setup?** → **[GitHub Copilot](#github-copilot)**
- **Want a polished IDE replacement (closed-source)?** → **[Cursor](#cursor)** / **[Devin Desktop (formerly Windsurf)](#devin-desktop)**
- **Enterprise with a massive monorepo and code-search needs?** → **[Sourcegraph Cody (Enterprise only)](#sourcegraph-cody)**
- **Heavy AWS stack, moving off Amazon Q Developer, or want a spec before code?** → **[Kiro (successor to Amazon Q Developer)](#kiro)**
- **Standardised on Qwen models?** → **[Qwen Code](#qwen-code)**

---

## Head-to-head comparison (September 2026)

| Dimension | Aider | Claude Code | Claude Desktop | Cline | Continue (discontinued) | Cursor | Devin Desktop (formerly Windsurf) | Gemini CLI | GitHub Copilot | Kilo Code | Kiro (successor to Amazon Q Developer) | OpenAI Codex CLI | OpenCode | Qwen Code | Sourcegraph Cody (Enterprise only) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Pricing tiers (no prices — see each vendor)** | Free (open source; you pay your model provider) | Claude Pro and above (not in Free), or API-key billing | Free, Pro, Max (5x / 20x), Team, Enterprise | Open Source (free, BYOK), Enterprise | Discontinued (code stays free under Apache 2.0) | Hobby (free), Individual (Pro / Pro+ / Ultra), Teams, Enterprise | Free, Pro, Max, Teams, Enterprise | Free tier (personal Google account); Gemini API key, Vertex AI or Code Assist licence | Free, Pro, Pro+, Max, Business, Enterprise (Pro access for verified students, faculty, OSS maintainers) | Free & Open Source, Teams, Enterprise | Free, Pro, Pro+, Pro Max, Power, Enterprise (Amazon Q Developer: no new signups since 2026-05-15) | Included in ChatGPT Free, Go, Plus, Pro, Business, Edu, Enterprise; or API-key billing | Free (open source); optional OpenCode Zen curated models | Free (open source); you pay your model provider | Enterprise only (Cody Free / Pro ended 2025-07-23) |
| **Open source** | Apache 2.0 ✅ | Closed (Anthropic) | Closed (Anthropic) | Apache 2.0 ✅ | Apache 2.0 — read-only, unmaintained | Closed (VS Code fork) | Closed (Cognition; VS Code-based) | Apache 2.0 ✅ | Closed (Microsoft) | MIT ✅ | Closed (AWS) | Apache 2.0 ✅ | MIT ✅ | Apache 2.0 ✅ | Closed; last public client source archived 2025-08-01 |
| **Bring your own model** | Yes — any LLM via LiteLLM | Claude models only — Anthropic, Amazon Bedrock, Google Cloud, Microsoft Foundry, or an LLM gateway | No (Claude models only) | Yes — OpenAI, Anthropic, Google and others (BYOK) | Yes (final release) | Chat only — OpenAI, Anthropic, Google, Azure, Bedrock keys; Tab stays on Cursor models | Some BYOK options alongside Cognition's SWE models | Gemini models (Google account, Gemini API, Vertex AI) | Model picker on paid plans; BYOK for any compatible provider in VS Code | Yes — BYOK, or 500+ models via Kilo | Multi-provider menu (Anthropic, OpenAI, open-weight); BYOK not documented | Yes — custom model providers in config.toml | Yes — 75+ providers | Yes — OpenAI, Anthropic, Gemini and Qwen APIs; any third-party provider | Unverified |
| **Local LLM support** | Yes (Ollama, llama.cpp, vLLM, LM Studio) | No | No | Yes — Ollama, LM Studio | Yes (final release; unmaintained) | Not documented | Not documented | Not documented | Yes in VS Code — BYOK via the Ollama extension, works offline without a Copilot plan | Yes — Ollama, LM Studio | Not documented | Yes — `--oss` with Ollama or LM Studio | Yes — Ollama, LM Studio, llama.cpp | Yes — Ollama, vLLM | Unverified |
| **Multi-file edits / refactor** | Good — git-aware, edits in commits | Excellent — agentic, plans + executes across many files | Excellent — agent mode + filesystem MCP, edits via accepted diffs | Agentic | Good (final release) | Strong (Agent mode) | Strong (Devin Local agent, replaced Cascade) | Agentic | Good (Agent mode in VS Code; Copilot CLI) | Agentic | Spec-driven: requirements → design → tasks, then the agent implements | Agentic, sandboxed | Agentic (`build` agent; read-only `plan` agent) | Agentic (subagents, agent teams) | Good with codebase search backing |
| **Codebase awareness** | Repo-map (deterministic, no embeddings) | Reads files on demand, very strong with hooks | Filesystem MCP — reads on demand, can index via custom MCP | Unverified | Indexed embeddings + custom retrievers (final release) | Indexed embeddings | RAG-based indexing + Fast Context retrieval | 1M-token context window | Indexed for paid users | Unverified | Steering files + specs | AGENTS.md project instructions | Unverified | LSP integration, auto-memory | Best-in-class — Sourcegraph code graph |
| **Visual / image input** | Yes — images and web pages for vision-capable models | Yes — drag-and-drop or paste (Ctrl+V) | Yes — drag in screenshots, PDFs, images for visual debugging | Unverified | Limited | Yes — paste image into chat | Unverified | Yes — images, PDFs, sketches | Limited | Unverified | Unverified | Yes — `--image` | Yes — drag image into the terminal | Unverified | No |
| **IDE coverage** | Terminal CLI (works alongside any editor) | Terminal CLI; VS Code + JetBrains; desktop app; browser | Editor-agnostic — works alongside any IDE via filesystem MCP; includes Claude Code | VS Code, Cursor, Windsurf, VSCodium, Antigravity, JetBrains; CLI; desktop app | VS Code, JetBrains, CLI (final release) | Standalone IDE (VS Code fork); Cursor CLI | Standalone IDE (VS Code-based); legacy Windsurf plugins in maintenance mode | Terminal CLI; VS Code companion; JetBrains + Zed via ACP | VS Code, Visual Studio, JetBrains, Neovim, Xcode; Copilot CLI | VS Code, JetBrains, CLI, cloud | Kiro IDE, Kiro CLI, web, iOS; ACP editors | Terminal CLI; VS Code / Cursor / Windsurf extension; Xcode + JetBrains integrations; desktop app | Terminal TUI; desktop app (beta); IDE integration | Terminal CLI; VS Code (beta), Zed, JetBrains; desktop app | VS Code, JetBrains, Visual Studio, web |
| **Privacy posture** | You pick the API; can be 100% local with Ollama | Account-dependent: Free / Pro / Max under Consumer Terms (training if the setting is on); Team / Enterprise / API under Commercial Terms (no training, 30-day retention) | Account-dependent: Free / Pro / Max under Consumer Terms (training if the setting is on); Team / Enterprise / API under Commercial Terms (no training) | BYOK — code goes to the provider you choose; can be fully local | 100% local possible (final release) | Telemetry on; Privacy Mode opts out of training | Unverified | Google cloud; terms depend on sign-in method (Code Assist individuals, Gemini API, Vertex AI) | Microsoft cloud; enterprise gates; local BYOK possible in VS Code | BYOK or Kilo-routed models; can be fully local | Unverified | OpenAI cloud (ChatGPT or API terms), or fully local with `--oss` | You pick the provider; can be fully local | You pick the provider; can be fully local | Unverified |
| **Best use case** | Open-source / local-first / git discipline (note: development has slowed) | Power users, big refactors, terminal-first workflows, CI integration | Architecture / planning sessions, visual debugging, MCP-extended workflows alongside any editor | Open-source agent inside your existing editor | Migrating off it, or forking the Apache-2.0 code | Polished IDE replacement, broad audience | Cursor alternative, especially alongside Devin cloud agents | Free terminal agent; very large context | Already on GitHub, want zero friction | One open-source agent across VS Code, JetBrains and terminal | AWS shops, spec-first teams, Amazon Q Developer migrations | ChatGPT subscribers; open-source terminal agent with a sandbox | Vendor-neutral open-source terminal agent; fully local setups | Qwen-model users; open-source agent with local models | Enterprises on Sourcegraph with massive monorepos |

---

<!-- LIST:START -->
## Tools

### Aider <a name="aider"></a>

_AI pair programming in your terminal — edits code across your git repo with commit-per-change discipline._

**Site:** [https://aider.chat](https://aider.chat) · **Repo:** [https://github.com/Aider-AI/aider](https://github.com/Aider-AI/aider) · **License:** open-source · **Deployment:** cli

Aider is an open-source CLI coding assistant that edits code in an
existing git repository under the developer's direction. It's known for
two core design choices: it operates on git (every change becomes a
discrete commit with an auto-generated message, making rollback trivial),
and it builds a "repo map" of the codebase so the model always has
context for where functions and types live across files.

It supports any LLM provider — Anthropic Claude, OpenAI GPT, local models
via Ollama or OpenAI-compatible servers, DeepSeek, xAI. Unlike IDE-coupled
assistants, Aider lives in the terminal and plays well with any editor
the developer already uses.

The `/architect` mode separates planning (using a reasoning model) from
editing (using a fast edit model) for complex changes. The benchmark
leaderboard Aider maintains is a widely-cited reference for LLM coding
performance. Images (screenshots, mockups) and web pages can be added to
the chat for vision-capable models.

Staleness note (checked 2026-09-29): the latest tagged release is v0.86.0
from 2025-08-09, and the last commit to the main branch is from
2026-05-22. Aider still works and its docs are online, but development has
slowed sharply — weigh that before standardising on it.

**Features:**
- Git-first workflow with automatic commits per change
- Repo-map context for large codebase awareness
- Any LLM provider (Claude, GPT, local, DeepSeek, xAI)
- Architect mode: reasoning model plans, edit model executes
- Image and web-page input for vision-capable models
- Voice input support
- In-chat commands for file management, linting, testing
- Language-agnostic (Python, JS, Rust, Go, Java, C++, … )

**Best for:**
- Pair programming in the terminal without IDE lock-in
- Refactoring across multi-file changes with git discipline
- Adding features to existing codebases with reviewable commits
- Running local LLMs as coding assistants
- Developers who prefer vim / emacs over IDE-integrated assistants

---

### Claude Code <a name="claude-code"></a>

_Anthropic's terminal-first agentic coding assistant with deep tool use and codebase awareness._

**Site:** [https://claude.com/claude-code](https://claude.com/claude-code) · **License:** commercial · **Deployment:** cli

Claude Code is Anthropic's official agentic coding tool, available in the
terminal, IDEs (VS Code, JetBrains), the Claude desktop app and the
browser. It runs against Claude models — via Anthropic directly or via
Amazon Bedrock, Google Cloud or Microsoft Foundry — and has first-class
tool use for reading
and editing files, running shell commands, searching codebases, browsing
the web, and orchestrating sub-agents. It ships with a hook system, slash
commands, MCP server support, and IDE integrations (VS Code, JetBrains).

Unlike chat-only coding assistants, Claude Code is agentic by design: it
plans, executes multi-step changes, reads its own output, and recovers
from errors. It's built around the Claude Agent SDK and exposes the same
primitives to developers who want to build custom agents.

Privacy depends on how you sign in. With a Free, Pro or Max account,
Claude Code falls under Anthropic's Consumer Terms: data is used to train
future models when the account's model-improvement setting is on (5-year
retention; 30 days if off). Under the Commercial Terms (Team, Enterprise,
API and cloud platforms), Anthropic does not train on Claude Code prompts
or code and retains them for 30 days by default. On Claude subscriptions,
Claude Code needs Pro or higher (it is not in the Free plan); it can also
be billed through an API key.

Images can be dragged in or pasted (Ctrl+V) into a session.

Anthropic publishes both `llms.txt` and `llms-full.txt` for the Claude
Code documentation at code.claude.com, making it one of the best-indexed
coding-agent references available to other AI assistants.

**Features:**
- Terminal CLI with native tool use (Bash, Read, Edit, Write, Grep)
- Hook system for shaping agent behavior per-project
- Slash commands and user-defined skills via SKILL.md
- MCP server support for connecting external tools and data
- IDE integrations for VS Code and JetBrains; also in the desktop app and browser
- Image input (drag-and-drop or paste)
- Background task support and session persistence
- Built on the Claude Agent SDK, exposed for custom agent builders

**Best for:**
- Refactoring and migration across large codebases
- Debugging and fixing issues with full shell + git access
- Writing new features with reviewed commits and CI awareness
- Onboarding to unfamiliar repos via guided exploration
- Building and testing in one loop without leaving the terminal

---

### Claude Desktop <a name="claude-desktop"></a>

_Anthropic's native desktop app — currently the strongest all-around AI coding companion via MCP, skills, and agent mode._

**Site:** [https://claude.com/download](https://claude.com/download) · **License:** commercial · **Deployment:** local

Claude Desktop is Anthropic's official native app for macOS, Windows,
and Linux. While not exclusively a coding tool, it's currently the
strongest all-around AI coding companion in 2026 thanks to the
combination of: MCP (Model Context Protocol) servers that give it
filesystem, git, GitHub, database, and shell access; a skills system
for packaging repeatable coding workflows; agent mode for autonomous
multi-step tasks; long-context conversations with local history; and
Anthropic's Claude Sonnet 4.x / Opus 4.x family running underneath.

Compared to **Claude Code** (Anthropic's terminal CLI agent): same
underlying models and tool-use primitives, different interface. Claude
Desktop is faster for visual work (drop in screenshots, read PDFs,
inspect designs), and the chat-first UX suits multi-turn coding
sessions where you're thinking through architecture rather than
typing-to-edit. Claude Code wins for terminal-native workflows and
CI integration; Claude Desktop wins for the "I want to talk through
a problem with full repo access" mode.

Compared to **Cursor / Windsurf**: those are IDE-bound. Claude Desktop
is editor-agnostic — works alongside any editor (VS Code, JetBrains,
Neovim) by reading/writing files via MCP. The UX trade-off is that
edits aren't inline; they happen in a chat-driven loop where Claude
proposes diffs you accept.

Plus: Claude Desktop is the place where MCP server experimentation
happens. New community MCP servers ship constantly (puppeteer, Stripe,
Slack, Postgres, Sentry, ...) — adding any of them gives Claude
Desktop a new capability without changing the app.

**Features:**
- Native apps for macOS, Windows, and Linux
- MCP (Model Context Protocol) integration — filesystem, git, GitHub, postgres, shell, browser, custom servers
- Skills system — package coding workflows as reusable invocations
- Agent mode for autonomous multi-step coding tasks
- Drop in screenshots / PDFs for visual debugging
- Long-context conversations with local persistence
- Multiple models (Sonnet, Opus, Haiku) selectable
- Editor-agnostic — pairs with any IDE you already use

**Best for:**
- Architecture / planning sessions where you talk through a design
- Multi-file refactors driven by chat with the agent reading the repo
- Visual debugging — drop in a screenshot of a broken UI
- Workflow automation via custom MCP servers and skills
- Power users who want Claude's full capabilities without committing to a CLI or new IDE
- Working alongside an existing editor (VS Code / JetBrains / Neovim) without replacing it

---

### Cline <a name="cline"></a>

_Apache-2.0 coding agent for VS Code-family editors and JetBrains, with a CLI and desktop app — bring your own keys or run local models._

**Site:** [https://cline.bot](https://cline.bot) · **Repo:** [https://github.com/cline/cline](https://github.com/cline/cline) · **License:** open-source · **Deployment:** local

Cline is "the open source coding agent in your IDE, terminal, & desktop",
licensed Apache 2.0. The extension installs into VS Code, Cursor,
Windsurf, VSCodium, Antigravity and JetBrains IDEs; there is also a CLI
(interactive or headless for CI/CD) and a desktop app (macOS, Windows).

The open-source version is free and runs on your own API keys ("OpenAI,
Anthropic, Google, and others") or on local models via Ollama and
LM Studio. An Enterprise tier adds team management, SSO, audit logs and
VPC deployment.

It supports MCP servers and plugins, and can scaffold new MCP tools on
request.

**Features:**
- Extension for VS Code, Cursor, Windsurf, VSCodium, Antigravity, JetBrains
- CLI (interactive or headless) and desktop app
- Bring your own API keys; local models via Ollama / LM Studio
- MCP servers and plugins
- Plans — Open Source (free) and Enterprise

**Best for:**
- Open-source agent inside an existing editor
- Teams that need BYOK with enterprise controls
- Local-model setups for code that can't leave the machine

---

### Continue (discontinued) <a name="continue-dev"></a>

_DISCONTINUED — Continue was acquired by Cursor in June 2026; the Apache-2.0 repo is now read-only and no longer maintained._

**Site:** [https://www.continue.dev](https://www.continue.dev) · **Repo:** [https://github.com/continuedev/continue](https://github.com/continuedev/continue) · **License:** open-source · **Deployment:** library

Continue was an open-source (Apache 2.0) coding agent for VS Code,
JetBrains and the terminal, best known for bring-your-own-model
configuration and first-class local LLM support (Ollama, LM Studio, vLLM).

It has been discontinued. continue.dev now reads "Continue was acquired by
Cursor", and the repository README states that it "is no longer actively
maintained and is read-only for all users". The team shipped a final
2.0.0 release of the VS Code extension, CLI and JetBrains plugin
(v2.0.0 / v2.1.0 tags, 2026-06-19). The source stays available under
Apache 2.0, so existing installs keep working and the code can be forked,
but there will be no fixes, new model support or security updates.

Kept on this list as a pointer for people searching for it. For an
actively maintained open-source, bring-your-own-model alternative, see
Cline, Kilo Code, OpenCode or Qwen Code.

Continue's `llms.txt` and `llms-full.txt` have returned 404 since at least
2026-07-24.

**Features:**
- Final release 2.0.0 (VS Code extension, CLI, JetBrains plugin), 2026-06-19
- Source remains Apache 2.0 on GitHub (read-only)
- No further maintenance

**Best for:**
- Existing users planning a migration
- Forks that want an Apache-2.0 IDE-agent codebase to build on

---

### Cursor <a name="cursor"></a>

_AI-first fork of VS Code with deep LLM integration, agent mode, and codebase-aware context._

**Site:** [https://cursor.com](https://cursor.com) · **License:** commercial · **Deployment:** local

Cursor is a commercial fork of VS Code that puts AI coding assistance at
the center of the editor rather than as an extension. It ships chat,
inline edits, multi-file rewrites, autocomplete, an agent mode for
autonomous task execution, and codebase-wide context retrieval out of the
box — all tuned against Claude and GPT models.

Cursor differentiates on UX polish: @-mentions to reference files and
symbols, diff-style inline edits, a native command palette for AI
actions, and proprietary context-selection heuristics tuned for the
provided models. Its agent mode (formerly "Composer") can execute
multi-step refactors across many files with user approval gates.

It's closed-source and subscription-based. Plans are Hobby (free, with
limited agent requests), Individual (Pro / Pro+ / Ultra), Teams and
Enterprise; paid plans include MCPs, skills, hooks and cloud agents. A
terminal agent, Cursor CLI (`agent`), ships alongside the editor. Bring-
your-own API keys (OpenAI, Anthropic, Google, Azure, AWS Bedrock) work for
chat models only — per Cursor's docs, Tab completion stays on Cursor's
built-in models.

Ownership changed in 2026: "Cursor has officially been acquired by SpaceX"
(Cursor blog, 2026-08-14), completing a process that began with a SpaceXAI
model-training partnership in April. The product keeps its name. Cursor
also acquired Continue in June 2026 (see that entry).

**Features:**
- VS Code fork with preserved extension compatibility
- Chat with @-file, @-symbol, @-web context references
- Inline edit with diff-preview before applying
- Agent mode for multi-step autonomous refactors
- Codebase-wide semantic search and retrieval
- Tab autocomplete tuned for each supported model
- Anthropic and OpenAI model support out of the box
- Cursor CLI (`agent`) for terminal use
- MCP support

**Best for:**
- Professional developers who want maximum AI integration
- Teams that want a consistent IDE across members with built-in AI
- Large refactors that benefit from multi-file agent coordination
- Developers migrating from pure VS Code who want more AI than extensions provide

---

### Devin Desktop (formerly Windsurf) <a name="devin-desktop"></a>

_Cognition's AI-native IDE — the product formerly called Windsurf (and before that, Codeium), now built around the Devin Local agent._

**Site:** [https://devin.ai/desktop](https://devin.ai/desktop) · **License:** commercial · **Deployment:** local

Devin Desktop is the product that used to be called Windsurf. Cognition
(the company behind the Devin cloud agent) acquired Windsurf's "IP,
product, trademark and brand" on 2025-07-14, after Google hired Windsurf's
CEO and licensed its technology. On 2026-06-02 Windsurf was renamed Devin
Desktop via an over-the-air update: same editor, settings and extensions,
and — per Cognition — the same plans. windsurf.com and codeium.com now
redirect to devin.ai/desktop.

The rename also replaced the agent. Cascade, Windsurf's original agent,
was succeeded by Devin Local, rewritten from scratch in Rust; the legacy
Cascade agent remained available until July 1. The editor now positions
itself as a command center for local and cloud agents (including Devin
itself) and speaks the Agent Client Protocol (ACP).

The old Codeium autocomplete extensions live on as "Windsurf plugins", but
Cognition's docs put the VS Code, Vim/Neovim, Visual Studio, Jupyter,
Chrome and Eclipse plugins in maintenance mode, and say of the JetBrains
plugin that "Cascade is being deprecated". This list no longer carries a
separate Codeium entry.

**Features:**
- VS Code-based IDE (backwards-compatible with Windsurf and VS Code extensions)
- Devin Local agent (replaced Cascade in June–July 2026)
- Agent Command Center for managing local and cloud agents
- MCP server integration
- RAG-based codebase indexing and Fast Context retrieval
- BYOK options alongside Cognition's own SWE models
- Plans — Free, Pro, Max, Teams, Enterprise

**Best for:**
- Developers who want a Cursor-style AI IDE from a different vendor
- Teams that also use Devin cloud agents and want one place to manage both
- Former Windsurf / Codeium users (the update carried settings forward)

---

### Gemini CLI <a name="gemini-cli"></a>

_Google's open-source (Apache 2.0) terminal agent for Gemini models, with a free tier for personal Google accounts._

**Site:** [https://www.geminicli.com](https://www.geminicli.com) · **Repo:** [https://github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) · **License:** open-source · **Deployment:** cli

Gemini CLI is "an open-source AI agent that brings the power of Gemini
directly into your terminal", licensed Apache 2.0. It runs Gemini 3
models with a 1M-token context window and can build from PDFs, images or
sketches using Gemini's multimodal input.

Signing in with a personal Google account gives a free tier (the README
lists request-per-minute and per-day allowances); alternatively it uses a
Gemini API key, Vertex AI, or a Gemini Code Assist licence. Which privacy
terms apply depends on that sign-in method — Google's docs point to
separate notices for Code Assist for individuals, the Gemini API and
Google Cloud.

It supports MCP servers and extensions. Editor integration is via the
Gemini CLI Companion extension for VS Code-compatible IDEs, and via the
Agent Client Protocol for JetBrains IDEs, Zed and other ACP editors.

**Features:**
- Terminal agent, Apache 2.0
- Free tier with a personal Google account; API key, Vertex AI or Code Assist licence also supported
- Gemini 3 models, 1M-token context
- Multimodal input (images, PDFs, sketches)
- MCP servers and extensions
- VS Code companion extension; ACP for JetBrains and Zed

**Best for:**
- Trying a capable terminal agent at no cost
- Google Cloud / Vertex AI shops
- Very large context tasks (whole-repo reading)

---

### GitHub Copilot <a name="github-copilot"></a>

_GitHub's native AI coding assistant with chat, autocomplete, and agent mode across major IDEs._

**Site:** [https://github.com/features/copilot](https://github.com/features/copilot) · **License:** commercial · **Deployment:** local

GitHub Copilot is the original and most widely deployed AI coding
assistant, integrated natively into VS Code, Visual Studio, JetBrains
IDEs, Neovim, Xcode, and GitHub itself. It offers inline code completion,
chat, a multi-file agent mode, pull-request summaries, and a terminal
agent, GitHub Copilot CLI (`copilot`), which ships with the GitHub MCP
server preconfigured and accepts additional MCP servers. The older
`gh copilot` extension was deprecated on 2025-10-25 in favour of Copilot
CLI.

Under the hood Copilot routes to multiple LLMs — GPT, Claude Sonnet,
Gemini — with model choice exposed to users on the paid tiers. In VS Code,
Bring Your Own Key (BYOK) connects any compatible model provider, including
local models via the Ollama extension; per the VS Code docs, "You can use a
local model completely offline", and BYOK models work without a Copilot
plan or GitHub sign-in (Business/Enterprise admins can disable BYOK). Its
reach within the GitHub platform (issues, PRs, code review, Actions)
makes it a practical default for teams already on GitHub.

For enterprise deployments, Copilot offers SOC 2 compliance, data
residency, code reference filtering, and the ability to restrict
external traffic — the most mature enterprise posture in the category.

**Features:**
- VS Code, Visual Studio, JetBrains, Neovim, Xcode integrations
- Inline autocomplete, chat, and multi-file agent mode
- Pull-request and code-review assistance on GitHub
- Multiple model backends (GPT, Claude, Gemini)
- GitHub Copilot CLI (`copilot`) — terminal agent with MCP support (replaced `gh copilot`)
- BYOK and offline local models in VS Code (Ollama extension)
- Enterprise tier with SOC 2, data residency, content filtering
- Plans — Free, Pro, Pro+, Max, Business, Enterprise (Copilot Pro access for verified students, faculty and OSS maintainers)

**Best for:**
- Professional development at organizations already on GitHub
- Teams needing enterprise compliance posture out of the box
- Users who want PR / issue / code-review AI integrated into Git workflow
- Cross-IDE consistency (one subscription, many editors)
- Students and OSS maintainers on the free tier

---

### Kilo Code <a name="kilo-code"></a>

_MIT-licensed coding agent for VS Code, JetBrains and the CLI with 500+ models, BYOK and local models._

**Site:** [https://kilo.ai](https://kilo.ai) · **Repo:** [https://github.com/Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode) · **License:** open-source · **Deployment:** local

Kilo Code is an MIT-licensed coding agent that "meets you everywhere you
work": VS Code, JetBrains, the CLI, and a cloud surface at app.kilo.ai.
The Kilo CLI is a fork of OpenCode.

Kilo's pricing page lists a free and open-source tier (VS Code, JetBrains
and CLI extensions), plus Teams and Enterprise. You can "Bring your own
Anthropic, OpenAI, Google, Azure, AWS Bedrock, or other provider keys" and
"Run local models with Ollama or LM Studio"; through a Kilo account there
are 500+ models with mid-task switching.

A Kilo Marketplace distributes agents, skills, MCP servers and plugins.

**Features:**
- VS Code and JetBrains extensions, CLI (OpenCode fork), cloud agents
- 500+ models; BYOK for major providers
- Local models via Ollama or LM Studio
- Marketplace for agents, skills, MCP servers, plugins
- Plans — Free & Open Source, Teams, Enterprise

**Best for:**
- One open-source agent across VS Code, JetBrains and terminal
- Teams that want BYOK and model choice with central billing
- Local-model workflows

---

### Kiro (successor to Amazon Q Developer) <a name="kiro"></a>

_AWS's spec-driven coding agent (IDE, CLI, web) — the replacement for Amazon Q Developer, whose IDE plugins reach end of support on 2027-04-30._

**Site:** [https://kiro.dev](https://kiro.dev) · **Repo:** [https://github.com/kirodotdev/Kiro](https://github.com/kirodotdev/Kiro) · **License:** commercial · **Deployment:** local

Kiro is AWS's AI coding agent, built around one agent harness shared by
the Kiro IDE, the Kiro CLI, a web surface, iOS, and any ACP-compatible
editor. Its distinguishing idea is spec-driven development: a feature is
planned as requirements, design and tasks before the agent implements it,
with steering files and event-driven hooks shaping the agent's behaviour.

Kiro is what AWS points Amazon Q Developer users to. Per AWS's end-of-support
announcement, new Q Developer Free Tier accounts and subscriptions were
blocked from 2026-05-15, and "Amazon Q Developer IDE plugins and paid
Subscriptions will reach end of support on April 30, 2027, giving customers
12 months to transition to Kiro." The Q Developer CLI has already become
Kiro CLI — Kiro's docs call it "the next update of the Q CLI", with
existing workflows, subscription and authentication carried over.

Models come from several providers (Anthropic, OpenAI and open-weight
families such as DeepSeek, GLM, MiniMax and Qwen). The docs we checked do
not describe bring-your-own-key or local-model support.

**Features:**
- Spec-driven development (requirements → design → tasks)
- Steering files and event-driven agent hooks
- MCP support
- Kiro IDE, Kiro CLI (successor to Amazon Q Developer CLI), web and iOS
- ACP support for other editors
- Multi-provider model menu (Anthropic, OpenAI, open-weight models)
- Plans — Free, Pro, Pro+, Pro Max, Power, Enterprise

**Best for:**
- Amazon Q Developer users migrating before the 2027-04-30 end of support
- Teams that want a written spec before the agent touches code
- AWS-centric organisations standardising on an AWS-supported agent

---

### OpenAI Codex CLI <a name="codex-cli"></a>

_OpenAI's open-source (Apache 2.0) coding agent that runs locally in your terminal, with IDE extensions and a desktop app on the same harness._

**Site:** [https://developers.openai.com/codex](https://developers.openai.com/codex) · **Repo:** [https://github.com/openai/codex](https://github.com/openai/codex) · **License:** open-source · **Deployment:** cli

Codex CLI is "a coding agent from OpenAI that runs locally on your
computer". The CLI is open source under Apache 2.0 and written in Rust;
the same agent is available as an IDE extension (VS Code, Cursor,
Windsurf, VS Code Insiders, with Xcode and JetBrains providing their own
integrations), a desktop app (`codex app`) and a cloud agent at
chatgpt.com/codex.

You can sign in with a ChatGPT account — OpenAI's pricing docs say Codex is
included in the Free, Go, Plus, Pro, Business, Edu and Enterprise plans —
or use an API key, which OpenAI recommends for CI and shared environments.
It is not locked to OpenAI's hosted models: with `--oss` it runs against a
local "open source" provider such as Ollama or LM Studio, and custom
model providers can be defined in `config.toml`.

It supports MCP servers, lifecycle hooks, skills, AGENTS.md project
instructions and a configurable sandbox, and accepts image attachments
(`--image`).

**Features:**
- Terminal agent (Rust), Apache 2.0
- Sign in with ChatGPT (Free through Enterprise plans) or an API key
- Local models via `--oss` (Ollama, LM Studio) and custom providers
- MCP servers, hooks, skills, AGENTS.md
- Image attachments (`--image`)
- IDE extension for VS Code-family editors; desktop app; cloud agent

**Best for:**
- ChatGPT subscribers who want a terminal agent included in their plan
- Open-source, auditable CLI agent with a sandbox
- Mixing hosted OpenAI models with local open-weight models

---

### OpenCode <a name="opencode"></a>

_MIT-licensed, provider-agnostic coding agent for the terminal (plus desktop app and IDE use) — 75+ model providers including local models._

**Site:** [https://opencode.ai](https://opencode.ai) · **Repo:** [https://github.com/anomalyco/opencode](https://github.com/anomalyco/opencode) · **License:** open-source · **Deployment:** cli

OpenCode describes itself as "the open source AI coding agent". It is
MIT-licensed (about 211k GitHub stars as of 2026-09-29); the
repository moved from `sst/opencode` to `anomalyco/opencode`.

It is provider-agnostic: the docs list support for "75+ LLM providers",
and local models through Ollama, LM Studio and llama.cpp. OpenCode Zen is
an optional curated list of models tested by the OpenCode team. It ships
two built-in agents — `build` (full access) and `plan` (read-only, asks
before running shell commands) — plus subagents.

Beyond the terminal UI there is a desktop app (beta, macOS / Windows /
Linux) and IDE integration. It supports MCP servers, and images can be
dragged into the terminal.

**Features:**
- Terminal agent, MIT licence
- 75+ providers; local models via Ollama, LM Studio, llama.cpp
- Built-in `build` and `plan` agents, subagents
- MCP servers
- Image input (drag and drop)
- Desktop app (beta) and IDE integration

**Best for:**
- Open-source, vendor-neutral terminal agent
- Running fully local with open-weight models
- Switching providers without switching tools

---

### Qwen Code <a name="qwen-code"></a>

_Alibaba's Apache-2.0 coding agent for terminal, editor and desktop — multi-protocol, with any third-party provider or local model._

**Site:** [https://qwenlm.github.io/qwen-code-docs/](https://qwenlm.github.io/qwen-code-docs/) · **Repo:** [https://github.com/QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) · **License:** open-source · **Deployment:** cli

Qwen Code is "the open-source AI coding agent for your terminal, editor,
desktop, browser, and chat", from Alibaba's Qwen team, licensed
Apache 2.0. It is developed alongside the Qwen models but is
multi-protocol: it
"Supports OpenAI, Anthropic, Gemini, and Qwen APIs. Any third-party
provider or local model (Ollama / vLLM)."

It ships subagents, agent teams, auto-memory, skills and MCP. Editor
integrations are a VS Code companion extension (beta), Zed and JetBrains;
there is also a desktop app, web UI, SDKs and chat integrations.

**Features:**
- Terminal agent, Apache 2.0
- OpenAI, Anthropic, Gemini and Qwen API protocols; local models via Ollama / vLLM
- Subagents, agent teams, auto-memory, skills
- MCP support
- VS Code (beta), Zed and JetBrains integrations; desktop app

**Best for:**
- Qwen-model users who want a first-party agent
- Open-source agent with local-model support
- Teams mixing Chinese and Western model providers

---

### Sourcegraph Cody (Enterprise only) <a name="sourcegraph-cody"></a>

_Sourcegraph's code-search-backed coding assistant — now sold only as part of Sourcegraph Enterprise; Cody Free and Pro were discontinued in July 2025._

**Site:** [https://sourcegraph.com/cody](https://sourcegraph.com/cody) · **License:** commercial · **Deployment:** local

Cody pairs an AI assistant with Sourcegraph's code search and code graph,
which is why it is aimed at very large codebases and monorepos. Its docs
describe it as "Supported on Sourcegraph Enterprise", available in VS Code,
JetBrains, Visual Studio and the web app.

Individual plans are gone: Sourcegraph stopped Cody Free and Cody Pro
signups on 2025-06-25 and cut off access on 2025-07-23, while stating that
"Cody Enterprise customers are not affected by these changes." The client
is no longer developed in the open: the public source now lives in
`sourcegraph/cody-public-snapshot`, archived since 2025-08-01.

---

<!-- LIST:END -->

## Contributing

Submit a PR with a YAML entry following the schema in `entries/`. Each entry needs verifiable receipts — pricing must link to the pricing page, feature claims must be testable. Generic marketing copy gets rejected.

## License

MIT.