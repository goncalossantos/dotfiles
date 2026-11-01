# Agentic configuration

Portable agent guidance, skills, and research. This is the first part of the dotfiles
repository; editor, shell, and machine configuration can be added separately later.

## Layout

```text
AGENTS.md                              Main repository guidance
agentic/
  skills/
    i-have-adhd/SKILL.md                Pinned upstream skill (MIT)
    visual-explainer/SKILL.md           Local HTML-first teaching skill
  research/
    adhd-skill.md                       Source, caveats, and adoption notes
    simple-english.md                  ASD-STE100 reference and local policy
    explainer-video-services.md        MCP options, prices, and limitations
  examples/
    explainer-workflow.html            Small visual explanation of the approach
```

## Use

1. Read the root `AGENTS.md` for the baseline rules.
2. Read a skill's `SKILL.md` when the task needs it.
3. Use `examples/explainer-workflow.html` as a small output example.

This folder is source material, not an installer. Skills stored here are **not
automatically registered** with every agent. Copy or link a skill directory into
your chosen client's supported skill location after checking that client's docs.
Do not copy this repo's root guidance into unrelated projects without review.
Client-specific activation and persistent mode behavior may differ.

## Design decisions

- Plain English and attention-friendly organization are baseline guidance.
- The full upstream ADHD skill remains optional and unchanged for easy updates.
- Visual explanations use progressive depth: understand first, inspect details next.
- HTML works without a subscription. Paid video is an optional downstream format.
- No providers, credentials, global links, or paid jobs are configured yet.

## Next iterations

- Pick the first client to integrate and decide between copying and symlinking.
- Try the visual skill on a real topic and tune its depth and visual style.
- If video is useful, test one short storyboard with an explicit spending cap.
