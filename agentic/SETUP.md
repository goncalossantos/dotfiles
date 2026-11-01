# Set up Pi, Claude Code, and Codex

Use this guide when the repo is cloned into any permanent directory on a laptop,
server, or container. The installer is for **Linux and macOS**, with Python 3.9+
and symlink support. It does not install the agent applications or log in to them.
Run it as the account that will run the agents, not with `sudo`.

“PyClaud” was interpreted as **Pi, Claude Code, and Codex**. These instructions
are for their local CLI clients, not Claude Cowork or hosted/cloud sessions.

## Choose one installation method

- **Recommended now:** the small Python installer below. It creates reviewed
  symlinks, refuses conflicts, and requires no new dotfiles manager.
- **Optional:** the tested [chezmoi recipe](CHEZMOI.md). Use it instead of
  the installer if you want chezmoi to manage deployment.

Do not use two deployment tools to manage the same paths independently. Both
methods deliberately install the same content and leave the old Helix config alone.

## Prerequisites and application installation

Install Git and Python 3.9+ using the target system's package manager. Install only
the clients you intend to use, following their current official instructions:

- [Pi installation](https://github.com/earendil-works/pi#getting-started)
- [Claude Code setup](https://code.claude.com/docs/en/setup)
- [Codex CLI installation](https://developers.openai.com/codex/cli)

For Pi, use the documented Node.js version if you choose the npm route. For all
clients, authenticate separately as the target user. Do not copy another machine's
auth files into this public repo. The setup script intentionally does not install
applications, execute downloaded install scripts, select models, or change billing.

## 1. Put the checkout in a permanent location

Once the new `main` branch is published:

```sh
git clone --branch main https://github.com/goncalossantos/dotfiles.git "$HOME/src/dotfiles"
cd "$HOME/src/dotfiles"
```

Any other permanent path is fine, including paths with spaces. The installer finds
its source using its own location, not the current working directory. Do not use
an ephemeral `/tmp` checkout for a real installation: links depend on the checkout
remaining in place and readable by the target user.

**Branch:** the agent setup is published on `main`. Clone that branch explicitly:
the repository's default branch may still be `develop`, which does not contain
this setup.

Review the source before applying:

```sh
git status --short
python3 agentic/scripts/setup.py --help
python3 -m unittest discover -s agentic/tests -v
```

The chezmoi test reports a skip if chezmoi is unavailable; that is not a chezmoi pass.

## 2. Preview and install

For all three clients:

```sh
python3 agentic/scripts/setup.py
# Review the printed source and destination paths, then:
python3 agentic/scripts/setup.py --apply
```

For only one client, or a subset:

```sh
python3 agentic/scripts/setup.py --client claude
python3 agentic/scripts/setup.py --client claude --apply

python3 agentic/scripts/setup.py --client pi --client codex
# Repeat that command with --apply after reviewing it.
```

The default is a **dry run**. It creates no directories or links. All ordinary
path conflicts are checked before any links are created. Existing files,
directories, and foreign or dangling symlinks are never silently replaced. Matching
links are kept, so repeating the same installation is safe. This is not a fully
transactional installer: a later OS error such as a permissions failure can leave
some links installed. Fix the error and rerun, or use the removal command below.

If there is a conflict, read and back up the existing file, then merge preferences
manually. Do not delete an unfamiliar file just to make installation pass. An
existing `AGENTS.override.md` also stops installation until you review it, because
it can take priority over the new instructions.

## What is installed

| Consumer | Personal instructions | Skills |
| --- | --- | --- |
| Pi | `~/.pi/agent/AGENTS.md` | `~/.agents/skills/<name>/` |
| Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/skills/<name>/` |
| Codex | `~/.codex/AGENTS.md` | `~/.agents/skills/<name>/` |

Every instruction link points at `agentic/instructions/AGENTS.md`. This is a
portable preference file, **not** the repo-specific root `AGENTS.md`.
Every skill link points at a whole skill directory under `agentic/skills/`, so
supporting files and the upstream license stay available.

Pi and Codex both support the shared `~/.agents/skills` location. We install one
shared copy rather than giving Pi duplicate skill names. Consequently, installing
skills for either client also makes them discoverable by the other client if it
is installed. Client selection controls which instruction files are linked, not
exclusive visibility of shared skills. Removing shared skills affects both.

For linked skills, resolve the skill directory's real path before resolving
relative research references. The canonical files remain in this checkout.

## 3. Reload and verify in each client

These are manual client checks. Automated tests validate the filesystem, not an
LLM's obedience, provider authentication, or every installed client version.

### Pi

1. Start Pi as the target user, or run `/reload` in the existing session.
2. Inspect startup diagnostics for skill errors or duplicate names.
3. Run `/skill:visual-explainer Explain a cache hit and a cache miss`.
4. To opt into the stronger ADHD response mode, run `/skill:i-have-adhd`.

Pi's terminal does not itself imply an embedded HTML viewer. A host such as T3
Code may provide one. The skill prefers embedded HTML only when that capability
exists, otherwise it delivers a standalone file.

### Claude Code

1. Start a new terminal Claude Code session.
2. Use `/memory` to inspect loaded instructions and `/skills` to inspect skills.
3. Run `/visual-explainer Explain a cache hit and a cache miss`.
4. Use `/i-have-adhd` only when you want that mode.

This is the local CLI setup. Claude Cowork and cloud sessions do not necessarily
read these files. Do not assume a local symlink configures a hosted service.

### Codex

1. Start a new Codex session as the target user.
2. Use its skill picker (`/skills` in clients that expose it) or explicitly name
   `$visual-explainer` in your prompt.
3. Ask it to identify its active personal instructions and the skill file path.
4. Run an explanation task and confirm that HTML delivery matches host capabilities.

Codex checks `AGENTS.override.md` before `AGENTS.md`. Project instructions may
also change behavior. A successfully created link is not proof that the client
loaded or followed it.

## Custom homes and profile directories

To preview a separate target home without touching your account:

```sh
python3 agentic/scripts/setup.py --home /path/to/target-home
```

To use custom client directories, pass them explicitly:

```sh
python3 agentic/scripts/setup.py --client pi --pi-dir /path/to/pi-agent
python3 agentic/scripts/setup.py --client claude --claude-dir /path/to/claude-config
python3 agentic/scripts/setup.py --client codex --codex-dir /path/to/codex-home
```

Repeat with `--apply` only after review. The script refuses an ambient
`PI_CODING_AGENT_DIR`, `CLAUDE_CONFIG_DIR`, or `CODEX_HOME` for a selected client
unless you pass its matching directory option. This prevents accidental changes
to a harness-managed profile. Passing an option does not export an environment
variable for the client: launch that client with its matching environment too.

`--codex-dir` changes instructions, **not** the documented `~/.agents/skills`
location. Shared skills always use the target `--home`. Run the real clients with
that same home; `--home` on this script does not change their process environment.

For multi-user servers, each user should run setup separately against a trusted,
readable checkout. Do not point another user's agent at a checkout they should not
trust or cannot read. Authentication and API keys stay in each client's own stores,
never in this repo. The installer makes no network requests.

## Project-only use without global links

If you do not want user-level setup, leave the installer unused. In a project you
own, you can link the skill directories into `.agents/skills/` for Pi and Codex,
and `.claude/skills/` for Claude Code. Use `.pi/skills/` for older Pi releases that
do not support shared Agent Skills locations. Link whole directories, not only
`SKILL.md`.

Merge writing preferences into that project's existing `AGENTS.md` (Pi/Codex) or
`CLAUDE.md` (Claude Code); do not replace its instructions with this repo's root
file. Review project trust prompts. Uncommitted absolute links are machine-local;
do not commit them as a supposedly portable setup for other contributors.

## Updates, moving the checkout, and removal

Links follow edits immediately; reload or restart clients to pick them up. In a
clean checkout on `main`, use `git pull --ff-only` to retrieve reviewed updates.
If the pull fails, resolve it rather than resetting away local work. Inspect changes
before restarting agents, because changes to skills change agent instructions.

To remove the Python install, use the **same checkout, client selection, home, and
custom-directory options** as installation:

```sh
python3 agentic/scripts/setup.py --remove
# Review, then:
python3 agentic/scripts/setup.py --remove --apply
```

Only links pointing to the expected sources in this checkout are removed. The
script keeps directories and refuses unrelated paths. It does not uninstall
applications or delete authentication. Removing installed instructions cannot erase
content already loaded in an active session; restart the client.

Before moving or deleting the checkout, remove links while it is still at the old
path. Move it, then rerun setup from the new path. A new checkout intentionally
refuses links to an old checkout rather than claiming ownership of them.

## For an agent doing setup

1. Read this guide and the source; identify the target user and selected clients.
2. Check custom profile variables, existing instructions, overrides, and trust policy.
3. Run the dry run and show conflicts or planned destinations. Obtain approval to apply.
4. Apply only the selected setup method. Never overwrite user files or configure secrets.
5. Report filesystem checks separately from live-client checks, with any skipped tests.

See [client-source research](research/client-setup.md) and
[chezmoi evaluation](research/chezmoi.md) for evidence and limitations.
