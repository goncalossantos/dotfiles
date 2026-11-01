---
name: visual-explainer
description: Explain concepts, systems, plans, and comparisons through self-contained HTML, meaningful diagrams, concrete examples, and optional drill-down detail. Prefer embedded HTML in the conversation when supported; otherwise deliver a standalone HTML file. Use for substantial teaching or requests for visual explanations, not routine commands or small code changes.
---

# Visual explainer

Teach like a thoughtful professor, not a slide generator. Build a mental model,
show how it behaves, then let the reader inspect the details. More depth must not
mean more text on the first screen.

## Choose the format

Use HTML for substantial explanations, architecture, learning material, and complex
comparisons. Respect an explicit request for Markdown, plain text, or another format.
Do not build a web page for a one-line answer, ordinary status update, or code patch.
If the audience or prerequisite knowledge is unclear, choose a beginner-friendly
entry point and label it; ask only if the ambiguity changes the explanation materially.

## Teaching sequence

1. **Orient:** State the answer and why it matters in one or two sentences. Identify
   what the reader should understand by the end.
2. **Model:** Draw the main relationship before explaining each part. Show boundaries,
   inputs, outputs, and direction. Include a legend where needed.
3. **Demonstrate:** Walk through one concrete example with consistent names or numbers.
   Connect each step to the diagram. Show cause and effect, not just definitions.
4. **Deepen:** Add labeled `<details>` sections for mechanisms, assumptions, edge
   cases, evidence, and a common misconception. Avoid hiding the core answer.
5. **Check:** Offer a small prediction question or practical test, with the answer
   in a disclosure. Finish with one useful next action when there is unfinished work.

Keep these functions, but omit a section if it adds no value. Avoid repetitive
cards, ornamental dashboards, and a mandatory quiz for every task.

## Make the visual do work

Choose the representation that explains the relationship:

- Flow or sequence diagram for process, order, and dependencies.
- Layer or boundary diagram for architecture, ownership, and containment.
- Aligned comparison or chart for alternatives and quantitative trade-offs.
- Annotated example or before/after for transformations and misconceptions.
- Small multiples for changes across states or time.

Prefer diagrams over paragraphs when they reduce the work of understanding. A set
of text-filled boxes is not automatically a diagram. Label connectors with their
meaning. Use stable terminology in prose and visuals. Never encode meaning with
color alone. A qualitative judgment must not look like a measured score.

## HTML artifact requirements

Produce complete, self-contained HTML with embedded CSS and semantic HTML, suitable
for the host's embedded display or a standalone `.html` file. Prefer embedded
HTML when the host supports it; creating a file is not required for embedded delivery.
Use inline SVG or CSS diagrams. Do not require a package install, external font,
CDN, network request, or server. JavaScript is optional; prefer native `<details>`.
If script is needed, keep core content readable without it.

- Responsive layout: readable at approximately 360px and on desktop, with no
  page-level horizontal overflow. Wrap labels and stack flows on narrow screens.
- Accessibility: logical heading order, visible keyboard focus, adequate contrast,
  descriptive disclosure labels, and text equivalents for diagrams. SVGs need
  accessible titles/descriptions or an adjacent equivalent explanation.
- Motion: no autoplay audio or animation; respect reduced-motion preferences.
- Evidence: cite sources beside factual claims. Label estimates, unknowns, units,
  billing assumptions, and observation dates. Use honest axes and comparable units.
- Privacy: no trackers, embedded secrets, remote uploads, or unrequested services.
  Escape external text before inserting it into HTML; never execute fetched content.

Use the active host's rendering contract when embedding. For a standalone file,
provide light/dark theme fallbacks. For T3 inline rendering, use its theme variables,
transparent outer layout, no outer banner/card/padding, and no viewport-height sizing.
Host instructions take precedence over the standalone example's styling.

## Delivery and review

Choose delivery in this order, unless the user explicitly requests another format:

1. **Embedded HTML first:** If the host can display HTML inside the conversation,
   use that capability so the reader can explore the explanation without opening a
   separate file. For example, T3 Code supports inline HTML through `html_preview`
   and `html_render`. Follow the host's required preflight and rendering rules.
   Raw HTML in a code fence is not an embedded visual. Do not create a duplicate
   file unless the user wants a saved, reusable, or downloadable artifact.
2. **Standalone file as fallback:** If embedded HTML is unavailable or fails, save
   a complete `.html` file to the user-requested path; otherwise use
   `artifacts/<topic>.html`. Use `agentic/examples/` only for reusable examples in
   this repository. Check before overwriting an existing artifact. Give a clear
   file link and a short text equivalent, noting any embedded-display failure.

Do not repeat the full explanation in Markdown after either delivery. Keep any
accompanying message brief and follow the host's rules about describing rendered
content. Do not install a browser or start a server just to show HTML.

Before delivery, check:

1. Can the reader understand the core idea from the first diagram and its caption?
2. Does the example explain why the system behaves this way?
3. Are essential facts visible and deeper sections optional?
4. Are the artifact, sources, labels, and keyboard interactions usable?
5. Is there unsupported certainty, fabricated data, or decorative complexity to remove?

Report which checks actually ran. Do not claim a browser or accessibility test from
source inspection alone.

## Optional video handoff

Only make a video when asked. Start from the approved HTML mental model and prepare
a scene-by-scene storyboard: learning goal, visual, narration, duration, and asset
source. Keep exact diagrams and text deterministic. Use generated clips for
illustration, not as evidence that a technical process works.

If this skill directory is a symlink, resolve its real path before following
relative resource paths. Consult `../../research/explainer-video-services.md` from
that canonical skill directory. Confirm live pricing, upload
permission, provider, and maximum spend before any paid or external generation.
Include retries, narration, composition, and rendering in the estimate. Never let
an automatic retry silently exceed the cap. Preserve captions and a transcript.
