# Client configuration research

Observed **2026-11-01**. Scope: local Pi, Claude Code, and Codex CLIs. Configuration
formats evolve; verify the installed client version before applying to a new host.
The automated tests exercise deployment, not authenticated agent sessions.

## Sources and decisions

### Pi

Reviewed the installed **Pi 1.4.0** README and complete `docs/configuration.md`,
`docs/skills.md`, `docs/settings.md`, and `docs/packages.md` references. The package
is `@earendil-works/pi-coding-agent`; its documented upstream is
[earendil-works/pi](https://github.com/earendil-works/pi).

- [Configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md)
- [Skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)
- [Packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md)

Local docs establish `~/.pi/agent` as the default agent directory, configurable with
`PI_CODING_AGENT_DIR`. User instructions include `AGENTS.md`; an
`AGENTS.override.md` in the same directory takes precedence. Pi discovers personal
skills in `~/.agents/skills/` as well as its native skills directory. Explicit skill
invocation uses `/skill:<name>`. Use `/reload` after changes.

**Decision:** link user instructions into the agent directory and use the shared
Agent Skills directory. No edits to `settings.json`, auth, extensions, trust policy,
or model configuration are needed. A Pi package is a valid future distribution
option, but would not by itself configure Claude Code and Codex.

**Version caveat:** older Pi releases may have different paths or discovery rules.
The installed docs are evidence for this version, not a blanket guarantee for all
forks. Public links above are follow-up locations; the installed docs were the
primary Pi reference in this iteration.

### Claude Code

Fetched and reviewed relevant sections of the official documentation:

- [Memory / CLAUDE.md](https://code.claude.com/docs/en/memory)
- [Skills](https://code.claude.com/docs/en/skills)

The docs identify `~/.claude/CLAUDE.md` as personal instructions and
`~/.claude/skills/<name>/SKILL.md` as personal skills. They explicitly support
symlinked skill directories. Project equivalents use `CLAUDE.md` and
`.claude/skills/`. Current docs describe `/memory` and `/skills` inspection and
`/<skill-name>` invocation; availability can vary with installed versions.

**Decision:** use the native personal paths without modifying settings. Custom
config roots must be explicitly selected by the installer and matched by the
client's launch environment. No plugins or marketplace registration are required.

**Boundary:** local terminal configuration is not a reliable way to configure
Cowork or hosted/cloud sessions. The docs call out different discovery rules and
restrictions on symlinked user memory in Cowork.

### Codex

Fetched and reviewed relevant sections of official documentation:

- [Agent skills](https://developers.openai.com/codex/skills)
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)

Global instructions live in `$CODEX_HOME`, defaulting to `~/.codex`.
`AGENTS.override.md` takes precedence over `AGENTS.md`. Project instructions are
layered from the project root toward the working directory. Current docs list
`$HOME/.agents/skills` for personal skills and `.agents/skills` for repository
skills, and explicitly support symlinked skill folders.

**Decision:** use `~/.codex/AGENTS.md` and shared `~/.agents/skills`. Do not assume
that changing `CODEX_HOME` relocates the documented shared skill directory. Leave
`config.toml`, login, approvals, and sandbox policy untouched.

## What the tests establish

The Python tests validate dry-run behavior, repeat installation, selected clients,
explicit profile directories, refusal to replace user content or foreign links,
override-file preflight, arbitrary checkout locations, source references, and safe
removal. The chezmoi integration test validates the declared deployment tree in a
temporary home. See [test results](chezmoi.md#test-results).

No Codex CLI was available on the test machine. Pi and Claude executables were
present, but no live or authenticated model session was launched for validation.
The tools must still be reloaded and checked in their real deployment environment.
