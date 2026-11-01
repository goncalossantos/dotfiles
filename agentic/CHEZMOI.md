# Optional chezmoi recipe

This is a small, tested alternative to `scripts/setup.py`. Do not use it alongside
another tool managing the same paths. Read [SETUP.md](SETUP.md) first for scope,
client discovery, custom profiles, and security precautions.

## Scope

The **only chezmoi source directory is `agentic/chezmoi/`**, not the repository root.
It declares seven symlinks: three personal instruction files, two shared Pi/Codex
skills, and two Claude Code skills. It does not install Helix, the repo README,
secrets, agents, packages, or provider settings. No hooks or network templates run.

Do **not** run `chezmoi init --apply goncalossantos` against this repository as-is.
Its root is a general dotfiles repository, not a home-directory deployment tree.
Use the explicit source below. A future full migration could use `.chezmoiroot`,
but this prototype deliberately does not change how the whole repo is interpreted.

## Prepare

Install chezmoi through your OS package manager after reviewing the package. For
example, on Nix use `nix shell nixpkgs#chezmoi` for an ephemeral shell. This is not
an installer for chezmoi itself and does not execute a remote install script.

The recipe was tested with **chezmoi 2.70.3 on Linux/NixOS**. Other platforms and
versions should be checked with the isolated test before applying to a real home.

Set the absolute checkout path in your current shell:

```sh
DOTFILES="$(pwd -P)"
# Run the above from the root of your checkout.
```

Create a **separate local profile**, for example
`$HOME/.config/chezmoi/agentic.toml`, containing:

```toml
[data]
dotfilesRoot = "/absolute/path/to/your/dotfiles"
```

Use the actual absolute path, not `$HOME` or `~` inside the TOML string. Do not
replace an existing chezmoi config. Do not commit this machine-local profile.
The symlink templates use this one value so the checkout can live anywhere.

The prototype uses default client locations under the destination home. If you
use custom client directories or want only some clients, prefer the Python
installer or customize/review the recipe first. Ambient client environment
variables do not change these seven template destinations.

## Preview

In that shell, define a helper so every command uses the correct source and profile:

```sh
cm() {
  chezmoi --config "$HOME/.config/chezmoi/agentic.toml" \
    --source "$DOTFILES/agentic/chezmoi" \
    --destination "$HOME" --no-pager "$@"
}
cm managed
cm diff
cm apply --dry-run
```

Review all destinations, existing files, and `AGENTS.override.md` files yourself.
Unlike our Python installer, this recipe does not add an extra conflict-preflight
policy. **chezmoi is designed to reconcile managed destinations**, including changes
to existing files after review. It is not an unconditional “never overwrite” tool.
Its drift prompts are useful but are not a substitute for backups and `diff`.
Never add `--force` to a real apply merely to bypass a conflict.

## Apply and verify

Only after explicit approval:

```sh
cm apply
cm diff
cm verify
```

An empty diff and successful verify mean the managed filesystem entries match.
They do not prove the clients have loaded the files. Use the per-client checks in
[SETUP.md](SETUP.md), then restart or reload those clients as needed.

This recipe uses symlinks for skills so edits remain in the canonical checkout.
chezmoi normally also supports managed regular files and templates. This prototype
does **not** demonstrate secret integration, machine-specific client settings, or
package installation.

## Updates and removal

Update the checkout with ordinary reviewed Git operations. Instruction and skill
content changes become visible through the existing links; destination changes
require another `cm diff` and approved `cm apply`.

For this exact unchanged recipe, the Python installer's `--remove` mode can remove
these same links safely, because it checks the link source before deletion:

```sh
python3 "$DOTFILES/agentic/scripts/setup.py" --remove
# Review the seven paths, then repeat with --apply.
```

This is a **one-time removal/migration aid**, not a second active deployment tool.
Stop using this chezmoi profile after removal or it will recreate the links on the
next apply. Keep any unrelated chezmoi setup intact. Do not use `chezmoi purge`
or `destroy` as a blanket uninstall command.

## Repeat the isolated test

From the repository root:

```sh
python3 -m unittest discover -s agentic/tests -v
```

If chezmoi is not on `PATH`, select an existing binary explicitly:

```sh
CHEZMOI_BIN=/absolute/path/to/chezmoi \
  python3 -m unittest discover -s agentic/tests -v
```

The test uses a temporary home, config, cache, data, and state directories. It checks
that preview changes no destination files, seven valid symlinks are installed,
unmanaged content survives, repeated apply has no diff, `verify` passes, and drift
is visible. A forced **dry run only** avoids a TTY prompt in the drift test; the
test never uses force for a real drift overwrite.
