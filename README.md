# awesome-ai-coding-agents

> Honest comparison of AI coding assistants in April 2026. What each one does well, what it does badly, which to pick for your situation. No sponsored placements, no affiliate links, no paid rankings.

Maintained by [Brethof AI](https://brethof.com). Companion to [awesome-llms-txt](https://github.com/BrethofAI/awesome-llms-txt) — this list goes deeper on one category.

---

## Quick decision tree

Pick by what matters to you. (Top to bottom — first match wins.)

- **Want the strongest all-around AI coding companion right now (April 2026)?** → **[Claude Desktop](#claude-desktop)**
- **Want the same Claude power but in your terminal / CI?** → **[Claude Code](#claude-code)**
- **Want it free + open source?** → **[Aider](#aider)** / **[Continue](#continue-dev)**
- **Need to run 100% locally with your own LLM?** → **[Aider](#aider)** / **[Continue](#continue-dev)**
- **Already pay for GitHub and want zero setup?** → **[GitHub Copilot](#github-copilot)**
- **Want a polished IDE replacement (closed-source)?** → **[Cursor](#cursor)** / **[Windsurf](#windsurf)**
- **Working on a massive monorepo with code-search needs?** → **[Sourcegraph Cody](#sourcegraph-cody)**
- **Heavy AWS stack, lots of cloud-service code?** → **[Amazon Q Developer](#amazon-q-developer)**
- **Just want free autocomplete in your existing editor?** → **[Codeium](#codeium)**

---

## Head-to-head comparison (April 2026)

| Dimension | Aider | Amazon Q Developer | Claude Code | Claude Desktop | Codeium | Continue | Cursor | GitHub Copilot | Sourcegraph Cody | Windsurf |
|---|---|---|---|---|---|---|---|---|---|---|
| **Pricing** | FREE (BYOAPI key) | $19/seat/mo (FREE tier limited) | $20/mo Pro, $100/mo Max | $20/mo Pro, $100/mo Max (same plans as Claude Code) | FREE individual + paid teams tier | FREE (open source, BYOAPI) | $20/mo Pro, $40/mo Business | $10/mo individual, $19/seat business, FREE for OSS maintainers | $9-19/seat/mo | $15/mo Pro |
| **Open source** | Apache 2.0 ✅ | Closed (AWS) | Closed (Anthropic-owned, runs locally with API key) | Closed (Anthropic) | Closed (free tier available) | Apache 2.0 ✅ | Closed (VS Code fork) | Closed (Microsoft) | Apache 2.0 client; cloud backend closed | Closed (VS Code fork) |
| **Bring your own model** | Yes — any LLM via LiteLLM | No | No (Anthropic only) | No (Anthropic only) | No | Yes — full BYOM, local LLMs first-class | Yes (BYOAPI) | GPT, Claude, Gemini selectable on paid tiers | Yes on enterprise tier | Limited (Codeium models + some pass-through) |
| **Local LLM support** | Yes (Ollama, llama.cpp, vLLM, LM Studio) | No | No | No | No | First-class — Ollama, LM Studio, vLLM, custom endpoints | Hacky (via OpenAI-compatible base URL) | No | Limited (Ollama as model option) | No |
| **Multi-file edits / refactor** | Good — git-aware, edits in commits | Good (refactoring tools) | Excellent — agentic, plans + executes across many files | Excellent — agent mode + filesystem MCP, edits via accepted diffs | Limited (autocomplete-focused) | Good — explicit @ context, edit-in-place | Strong (Composer / Agent mode) | Good (Agent mode in VS Code) | Good with codebase search backing | Strong (Cascade) |
| **Codebase awareness** | Repo-map (deterministic, no embeddings) | AWS service catalog awareness | Reads files on demand, very strong with hooks | Filesystem MCP — reads on demand, can index via custom MCP | Indexed for paid teams | Indexed embeddings + custom retrievers | Indexed embeddings | Indexed for paid users | Best-in-class — Sourcegraph code graph | Real-time indexing |
| **Visual / image input** | No (text only) | Limited | Limited (Read tool can ingest images) | Yes — drag in screenshots, PDFs, images for visual debugging | No | Limited | Yes — paste image into chat | Limited | No | Yes |
| **IDE coverage** | Terminal CLI (works alongside any editor) | VS Code, JetBrains | Terminal CLI; VS Code + JetBrains plugins | Editor-agnostic — works alongside any IDE via filesystem MCP | 40+ editors (VS Code, JetBrains, Vim, Emacs, Sublime, ...) | VS Code, JetBrains | Standalone IDE (VS Code fork) | VS Code, Visual Studio, JetBrains, Neovim, Xcode | VS Code, JetBrains, web | Standalone IDE (VS Code fork) |
| **Privacy posture** | You pick the API; can be 100% local with Ollama | AWS retention by default; configurable | Anthropic API (sees your code) | Anthropic API (sees your code) | Free tier sees code; enterprise zero-retention | 100% local possible; cloud optional | Telemetry on; Privacy Mode opts out of training | Microsoft cloud; enterprise gates | Self-hosted available (enterprise) | Codeium SOC 2; enterprise zero-retention |
| **Best use case** | Open-source / local-first / git discipline / cost-sensitive | AWS-heavy stacks | Power users, big refactors, terminal-first workflows, CI integration | Architecture / planning sessions, visual debugging, MCP-extended workflows alongside any editor | Free autocomplete in your existing editor | BYOM / privacy-conscious / customizable / self-hosted | Polished IDE replacement, broad audience | Already on GitHub, want zero friction | Massive monorepos with deep code search needs | Cursor alternative if you prefer Codeium's ecosystem |

---

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
performance.

**Features:**
- Git-first workflow with automatic commits per change
- Repo-map context for large codebase awareness
- Any LLM provider (Claude, GPT, local, DeepSeek, xAI)
- {'Architect mode': 'reasoning model plans, edit model executes'}
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

### Amazon Q Developer <a name="amazon-q-developer"></a>

_AWS's AI coding assistant with deep integration into AWS services and enterprise compliance._

**Site:** [https://aws.amazon.com/q/developer/](https://aws.amazon.com/q/developer/) · **License:** commercial · **Deployment:** local

---

### Claude Code <a name="claude-code"></a>

_Anthropic's terminal-first agentic coding assistant with deep tool use and codebase awareness._

**Site:** [https://claude.com/claude-code](https://claude.com/claude-code) · **License:** commercial · **Deployment:** cli

Claude Code is Anthropic's official terminal-based coding agent. It runs
locally against the Claude API and has first-class tool use for reading
and editing files, running shell commands, searching codebases, browsing
the web, and orchestrating sub-agents. It ships with a hook system, slash
commands, MCP server support, and IDE integrations (VS Code, JetBrains).

Unlike chat-only coding assistants, Claude Code is agentic by design: it
plans, executes multi-step changes, reads its own output, and recovers
from errors. It's built around the Claude Agent SDK and exposes the same
primitives to developers who want to build custom agents.

Anthropic publishes both `llms.txt` and `llms-full.txt` for the Claude
Code documentation, making it one of the best-indexed coding-agent
references available to other AI assistants.

**Features:**
- Terminal CLI with native tool use (Bash, Read, Edit, Write, Grep)
- Hook system for shaping agent behavior per-project
- Slash commands and user-defined skills via SKILL.md
- MCP server support for connecting external tools and data
- IDE integrations for VS Code and JetBrains
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

### Codeium <a name="codeium"></a>

_Free AI autocomplete extension for 40+ editors — from the makers of Windsurf._

**Site:** [https://codeium.com](https://codeium.com) · **License:** freemium · **Deployment:** local

---

### Continue <a name="continue-dev"></a>

_Open-source AI coding assistant for VS Code and JetBrains — bring any model, any provider, customizable._

**Site:** [https://www.continue.dev](https://www.continue.dev) · **Repo:** [https://github.com/continuedev/continue](https://github.com/continuedev/continue) · **License:** open-source · **Deployment:** library

Continue is an open-source AI coding assistant that runs as a VS Code or
JetBrains extension. Unlike vendor-locked assistants, Continue is fully
configurable: users bring their own model (cloud or local), their own
provider (Anthropic, OpenAI, local via Ollama, vLLM, LM Studio, etc.),
and define custom slash commands, context providers, and tools via a
plain YAML config.

It supports chat, inline autocomplete, tab-complete, edit-in-place, agent
mode with tool use, codebase-aware retrieval, and team-shared configs. The
extension works online or fully offline against local inference servers,
making it a popular choice for organizations where code can't leave
developer machines.

Continue publishes `llms.txt` and `llms-full.txt` — a useful reference
while building coding assistants on top of local or hybrid models.

**Features:**
- VS Code and JetBrains extensions
- Bring-your-own-model (cloud or local)
- Chat, autocomplete, edit-in-place, agent mode
- Codebase retrieval and context providers
- Custom slash commands and tools via YAML config
- Team-shared configuration for consistent org-wide setups
- Fully offline capable with local model servers

**Best for:**
- IDE-integrated coding assistance without vendor lock-in
- Air-gapped development teams using local LLMs
- Organizations standardizing on a custom model + prompt setup
- Developers who want Cursor-like features in vanilla VS Code
- {'Hybrid setups': 'fast local completions, smart cloud chat'}

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

It's closed-source and subscription-based, with a free tier that has
meaningful limits. Commercial adoption among professional developers is
significant.

**Features:**
- VS Code fork with preserved extension compatibility
- Chat with @-file, @-symbol, @-web context references
- Inline edit with diff-preview before applying
- Agent mode for multi-step autonomous refactors
- Codebase-wide semantic search and retrieval
- Tab autocomplete tuned for each supported model
- Anthropic and OpenAI model support out of the box

**Best for:**
- Professional developers who want maximum AI integration
- Teams that want a consistent IDE across members with built-in AI
- Large refactors that benefit from multi-file agent coordination
- Developers migrating from pure VS Code who want more AI than extensions provide

---

### GitHub Copilot <a name="github-copilot"></a>

_GitHub's native AI coding assistant with chat, autocomplete, and agent mode across major IDEs._

**Site:** [https://github.com/features/copilot](https://github.com/features/copilot) · **License:** commercial · **Deployment:** local

GitHub Copilot is the original and most widely deployed AI coding
assistant, integrated natively into VS Code, Visual Studio, JetBrains
IDEs, Neovim, Xcode, and GitHub itself. It offers inline code completion,
chat, a multi-file agent mode, pull-request summaries, and command-line
assistance via `gh copilot`.

Under the hood Copilot routes to multiple LLMs — GPT, Claude Sonnet,
Gemini — with model choice exposed to users on the paid tiers. Its
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
- `gh copilot` CLI for command-line help
- Enterprise tier with SOC 2, data residency, content filtering
- Free tier available for open-source maintainers and students

**Best for:**
- Professional development at organizations already on GitHub
- Teams needing enterprise compliance posture out of the box
- Users who want PR / issue / code-review AI integrated into Git workflow
- Cross-IDE consistency (one subscription, many editors)
- Students and OSS maintainers on the free tier

---

### Sourcegraph Cody <a name="sourcegraph-cody"></a>

_AI coding assistant with enterprise-grade code search context across massive codebases._

**Site:** [https://sourcegraph.com/cody](https://sourcegraph.com/cody) · **License:** commercial · **Deployment:** local

---

### Windsurf <a name="windsurf"></a>

_AI-native IDE from Codeium with Cascade agent mode, deep indexing, and real-time code awareness._

**Site:** [https://windsurf.com](https://windsurf.com) · **License:** commercial · **Deployment:** local

Windsurf (formerly Codeium) is a commercial AI-native IDE and VS Code
fork competing directly with Cursor. Its flagship feature is Cascade —
an agent mode that combines chat, multi-file edits, and codebase
understanding into a single conversational interface that can execute
long-running tasks with user approval.

Windsurf emphasizes real-time awareness of the developer's actions (what
they just edited, what they're looking at) to feed context into agent
responses. Its indexing of large codebases is a recurring strength in
benchmarks against comparable AI IDEs.

Windsurf shares roots with the Codeium autocomplete extension, which
remains available as a standalone plugin for VS Code, JetBrains, Vim,
Emacs, and many more.

**Features:**
- VS Code-based IDE with Cascade agent mode
- Real-time context awareness of developer actions
- Multi-file edit planning and execution
- Deep codebase indexing (fast on large repos)
- Supervised agent with user-approval gates
- Standalone Codeium autocomplete for 40+ editors
- Team plans with shared context / custom instructions

**Best for:**
- Developers who want Cursor-style AI IDE with a different polish model
- Large-codebase work where indexing quality matters
- Teams standardizing on an AI-native IDE
- Users of Codeium autocomplete who want the full Cascade experience

---

## Contributing

Submit a PR with a YAML entry following the schema in `entries/`. Each entry needs verifiable receipts — pricing must link to the pricing page, feature claims must be testable. Generic marketing copy gets rejected.

## License

MIT.