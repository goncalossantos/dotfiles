# Agentic configuration

Portable agent guidance, skills, and research. This is the first part of the dotfiles
repository; editor, shell, and machine configuration can be added separately later.

## Layout

```text
AGENTS.md                              Main repository guidance
agentic/
  SETUP.md                             Installation and client verification
  CHEZMOI.md                           Optional chezmoi deployment recipe
  instructions/AGENTS.md               Portable personal preferences
  scripts/setup.py                     Dry-run-first symlink installer
  tests/                               Isolated installer and chezmoi tests
  chezmoi/                             Optional seven-link deployment source
  skills/
    i-have-adhd/SKILL.md                Pinned upstream skill (MIT)
    visual-explainer/SKILL.md           Local HTML-first teaching skill
  research/
    adhd-skill.md                       Source, caveats, and adoption notes
    simple-english.md                  ASD-STE100 reference and local policy
    explainer-video-services.md        MCP options, prices, and limitations
    client-setup.md                    Pi, Claude Code, and Codex sources
    chezmoi.md                         Git comparison and actual test results
  examples/
    explainer-workflow.html            Small visual explanation of the approach
```

## Use

1. Read the root `AGENTS.md` for the baseline rules.
2. Read a skill's `SKILL.md` when the task needs it.
3. Use `examples/explainer-workflow.html` as a small output example.

To install user-level preferences and skills, follow [SETUP.md](SETUP.md).
The Python installer previews changes by default and refuses to overwrite existing
configuration. [CHEZMOI.md](CHEZMOI.md) provides a tested alternative, not an extra
required layer. Choose one deployment method.

Skills are **not automatically registered** just because this repo was cloned.
Do not copy this repo's root guidance into unrelated projects: the installer uses
`instructions/AGENTS.md`, which contains portable personal preferences instead.
Client-specific activation and persistent mode behavior may differ.

## Design decisions

- Plain English and attention-friendly organization are baseline guidance.
- The full upstream ADHD skill remains optional and unchanged for easy updates.
- Visual explanations use progressive depth: understand first, inspect details next.
- HTML works without a subscription. Paid video is an optional downstream format.
- No providers, credentials, global links, or paid jobs are configured yet.

## Next iterations

- Run the documented manual discovery checks in the clients you actually use.
- Try the visual skill on a real topic and tune its depth and visual style.
- If video is useful, test one short storyboard with an explicit spending cap.
