# Should this dotfiles repo use chezmoi?

Research and local test: **2026-11-01**.

## Recommendation

**Keep Git. Use the small installer for the current agent setup. Keep chezmoi as
a tested option for when this repo grows into machine-specific dotfiles.**

chezmoi is not a better Git or a replacement for GitHub. It adds **deployment**:
map source files into their home-directory locations, render templates, preview
differences, and apply the desired state. Git still versions and synchronizes the
source. For seven straightforward symlinks, the extra naming conventions and
local profile are optional complexity. For varied laptops and servers, they become
more useful.

## The mental model

Open [the visual walkthrough](../examples/git-and-chezmoi.html) for a diagram with
optional drill-down explanations.

```text
GitHub repository
       │ git clone / git pull
       ▼
Local source files
       │ chezmoi renders templates using local machine data
       ▼
Desired files, contents, permissions, and links
       │ chezmoi diff → review → chezmoi apply
       ▼
Actual files under the target user's home
```

Git answers **“Which revision do I have?”** chezmoi answers **“Which configuration
should exist here, and how does this machine differ from it?”**

Example: Git stores `dot_claude/symlink_CLAUDE.md.tmpl`. chezmoi interprets `dot_`
as a leading dot, `symlink_` as a link, and `.tmpl` as a template. It renders the
local checkout path and creates `~/.claude/CLAUDE.md` pointing to our portable
instruction file. These are source naming conventions, not filenames to copy by hand.

## Comparison

| Need | Git alone | Git + our installer | Git + chezmoi |
| --- | --- | --- | --- |
| History, branches, remote synchronization | Yes | Git | Git |
| Put files in client-specific directories | Manual | Seven scoped symlinks | Declarative source-to-home mapping |
| Preview installation changes | Git diff only sees tracked source changes | Printed link plan | Desired-state diff and dry run |
| Preserve existing user files | No deployment policy | Refuse conflicts before linking | Review diffs/prompts; can reconcile/replace managed targets |
| Different content per host or OS | Manual branches or scripting | Not implemented | Templates and local data |
| Permissions and encrypted/secret-backed files | Not a general deployment system | Not implemented | Supported features, **not tested here** |
| Runtime dependencies | Git | Git + Python 3.9+ | Git workflow + chezmoi binary |

A symlink has a trade-off: edits take effect in the source immediately, and moving
the checkout breaks it. chezmoi's normal regular-file mode can deploy standalone
files instead. Our prototype deliberately uses symlinks to keep these agent files
single-sourced; it is not a complete demonstration of chezmoi's capabilities.

## Test results

Tests use temporary homes only. No real personal agent configuration was installed.

**Python installer: nine tests passed.** Covered no-write dry run; seven-link
installation, idempotence, and removal; collision preflight; foreign/dangling link
protection; custom profile selection; ambient variable acknowledgement; override
file protection; checkout paths with spaces; and parent-path errors.

**Real chezmoi integration: one test passed**, using **v2.70.3 from nixpkgs** on
Linux/NixOS. The test exercised our actual `agentic/chezmoi/` source:

1. `diff` showed the seven proposed symlinks; `apply --dry-run` left the destination unchanged.
2. `apply` created seven valid links, including whole skills and the MIT license.
3. Unmanaged content remained unchanged; a second apply produced no diff and `verify` passed.
4. A changed managed link appeared as drift. A dry run left it unchanged.

**Useful finding:** after drift, chezmoi requested confirmation and failed in the
noninteractive test because no TTY was available. The test was adjusted to use
`--force` **only with `--dry-run`** for that assertion. This is not a recommendation
to force real applies. It confirms that unattended drift handling needs an explicit
policy instead of assuming everything is safe to overwrite.

The latest upstream release endpoint resolved to v2.74.0. Its Linux release archive
was downloaded to `/tmp` and matched its published SHA-256 checksum, but the binary
could not execute on this NixOS host because its dynamic loader was not compatible.
It was not installed globally. Testing used the Nix-provided v2.70.3 binary instead.
That is the tested version, not a claim that the latest release was validated.

**Not tested:** macOS/Windows behavior, live agent loading, secrets, encryption,
package installation, remote SSH bootstrap, or per-machine template branches.
No paid provider requests or credential changes were made.

To reproduce, run the commands in [the chezmoi guide](../CHEZMOI.md). A missing
chezmoi binary yields a skipped integration test, not a pass.

## When to adopt it more broadly

Use chezmoi when maintaining machine differences becomes real work: distinct work
and personal identities, OS-specific shell configuration, packages or templates,
selective deployment, or secret-manager-backed settings. At that point:

- Keep this Git repository as the canonical source.
- Agree on which paths chezmoi owns, and migrate those paths once.
- Add host/OS data only for actual differences. Avoid speculative templates.
- Preview every apply and keep credentials out of public source/history.
- Retire overlapping installer ownership instead of running two managers in parallel.

It is reasonable to adopt it now if you want to learn it, but it is not required
for Pi, Claude Code, or Codex to use these files.

## Sources

Official sources consulted:

- [chezmoi quick start](https://www.chezmoi.io/quick-start/) — source state, Git workflow,
  `diff`, `apply`, and new-machine setup.
- [Why use chezmoi?](https://www.chezmoi.io/why-use-chezmoi/) — multi-machine templates,
  secret integration, and alternatives to maintaining a custom deployment script.
- [Official releases](https://github.com/twpayne/chezmoi/releases) — release artifacts.
- Actual `chezmoi --help` and executable behavior — evidence for tested commands.

A guessed `/user-guide/concepts/` URL returned 404. No conclusions depend on it.
