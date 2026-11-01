# The “I Have ADHD” skill

## Found

The likely match is [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd),
a skill for attention-friendly agent output. Its README describes action-first
answers, numbered steps, reduced tangents, and visible progress.

Observed on **2026-11-01**. The unchanged local copy is pinned to commit
`1ecea1993b7fce257ffbd686c070948b5e07eda6`:

- [Pinned SKILL.md](https://github.com/ayghri/i-have-adhd/blob/1ecea1993b7fce257ffbd686c070948b5e07eda6/skills/i-have-adhd/SKILL.md)
- [Pinned MIT license](https://github.com/ayghri/i-have-adhd/blob/1ecea1993b7fce257ffbd686c070948b5e07eda6/LICENSE)
- Local copy: `../skills/i-have-adhd/`, including the upstream copyright notice.

## Adoption choice

Keep the full upstream skill optional. Use its presentation ideas in the baseline
`AGENTS.md`, but do not assume that all of its wording is appropriate for everyone.
Its frontmatter disables automatic model invocation in clients that support that
field; explicit invocation and session persistence are client-dependent.

The source makes broad statements about memory and dopamine. Treat those as the
author's framing, not medical evidence or facts about an individual reader. The
local baseline avoids diagnosing the reader or repeating those claims.

Other caveats:

- Exact time estimates are useful only when supported. Do not fabricate them.
- A five-item presentation target must never suppress required detail.
- “No recap” must not prevent useful validation results or handoff information.
- Long explanations are compatible with attention-friendly output when core ideas
  are visible and optional depth uses progressive disclosure.

## Relationship to the visual skill

The two skills solve different problems. `i-have-adhd` shapes a response so it is
easy to act on. `visual-explainer` shapes a concept so it is easy to understand.
Use short, action-first chat around a deep HTML artifact instead of forcing the
whole explanation into a short response.

## Updating

Review upstream changes before replacing the local file. Fetch `SKILL.md` and
`LICENSE` from the same immutable commit, preserve attribution, and update the pin
and observation date here. Do not run an upstream installer as part of a source update.
