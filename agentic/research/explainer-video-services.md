# Explainer video services and MCP

Research snapshot: **2026-11-01**. USD, before tax where applicable. These are
published prices, not a checkout quote. No accounts were connected, no MCP tools
were exercised, and no paid generation was run. “Official MCP” means the provider
publishes or maintains it, not that it was integration-tested here.

## Recommendation

Start with **HTML + exact diagrams**. If video proves useful, try **JSON2Video**
for narrated composition. Add **fal** only when generated illustrative footage
would help. A presenter/avatar is a separate choice, not a requirement for teaching.

Do not confuse three products:

- **Composition:** arrange known visuals, narration, captions, and timing.
- **Generative video:** synthesize short clips from text or images.
- **Avatar presentation:** animate a talking presenter from a script.

For technical explanations, correctness and editable labels favor composition.
Generative models can distort text, arrows, geometry, and cause-and-effect.

## Shortlist

| Service | What it is like / best fit | MCP evidence | Published cost snapshot |
| --- | --- | --- | --- |
| JSON2Video | Scene/template-driven cloud composition into MP4; useful for repeatable narrated explainers. Exact diagram assets must still be prepared. | Official remote OAuth MCP and local stdio server. | 600 trial credits, watermarked. $49.95 prepaid for 7,200 credits / up to 120 minutes. Base rendering is 1 credit per output second. |
| fal | Model marketplace for image, video, and audio generation; useful for short illustrative inserts, not a complete lesson by itself. | Official generation MCP, remote OAuth. Includes model discovery, schemas, pricing, and queued generation. | MCP itself is free; model runs are paid. Veo 3 Fast endpoint's visible pricing panel: $0.10/s without audio, $0.15/s with audio. See conflicting copy warning below. |
| Runway API | Generative clips and other media operations; useful as a cost/quality comparison or future API integration. | API confirmed; an official generation MCP was **not verified** in this research. Do not assume it plugs straight in. | $0.01 per credit; `gen4_turbo` 5 credits/s ($0.05/s); `gen4.5` 12 credits/s ($0.12/s). |

### JSON2Video details

- Official MCP source: [JSON2Video/json2video-mcp](https://github.com/JSON2Video/json2video-mcp).
- Remote endpoint: `https://mcp.json2video.com/mcp`; OAuth account authorization.
- Local option: `@json2video/cli` with Node.js 20+ and an API key. Review and pin the
  package before installation rather than running an unreviewed latest version.
- Tools include validation, templates, render submission, status checks, and uploads.
  Remote media upload takes public URLs; local file uploads need the local path or
  dashboard workflow. Public URLs are not appropriate for confidential content.
- [Pricing](https://json2video.com/pricing/): $49.95 prepaid / 120 minutes;
  $99.95 prepaid / 260 minutes. Professional subscription: $49.95/month for up to
  200 minutes. Hobby: $199.50 paid annually, shown as $16.63/month, 50 minutes/month.
  Annual equivalent is not a monthly cancellable price.

At the $49.95 prepaid rate, **one 60-second base render allocates about $0.42**
($49.95 / 120). This is not a $0.42 checkout option: the prepaid purchase is $49.95.
Each new render consumes credits, so revisions add cost. External narration or
transcription services may add charges. Trial videos are watermarked; prepaid
credits do not expire, while subscription credits expire monthly.

**Source conflict:** the MCP README mentions generated images/video, while the
pricing FAQ says JSON2Video does not natively generate images, video, or avatars.
Treat it as a compositor, not a source of included generative footage. Verify
whether any tool wraps an external service and how that service bills.

### fal details

- [Official generation MCP documentation](https://docs.fal.ai/model-apis/mcp).
- Remote endpoint: `https://mcp.fal.ai/mcp-relay`; OAuth. This is distinct from
  fal's documentation-only MCP, which cannot generate media.
- The published tools can discover models, inspect schemas, get pricing, upload
  inputs, and submit/check jobs. The account selected for MCP owns the charges.
- [Veo 3 Fast model page](https://fal.ai/models/fal-ai/veo3/fast).

**Pricing conflict:** that page's visible pricing panel says $0.10/s without audio
and $0.15/s with audio, but its descriptive copy still says $0.25/$0.40 per second.
At the panel rate, 60 generated seconds would be $6/$9; at the other quoted rate,
$15/$24. These are arithmetic planning examples, **not quotes for one supported
60-second call**. Check the live MCP pricing tool, allowed durations, resolution,
audio setting, and endpoint immediately before approval. Multiple short clips,
retries, voiceover, and final composition are additional work and may cost more.

### Runway details

[Official developer API pricing](https://docs.dev.runwayml.com/guides/pricing/)
confirms $0.01/credit and the rates above. At those rates, 60 generated seconds
would be $3 for Gen-4 Turbo or $7.20 for Gen-4.5, before retries and composition.
These are normalized calculations, not a single-call duration guarantee. Model
inputs and allowed durations differ. Consumer subscription credits must not be
assumed to fund developer API usage. An MCP adapter would need separate review.

## Avatar candidates: not yet verified enough to recommend

**HeyGen** is worth investigating if a talking instructor matters. GitHub search
returned community MCP repositories, but the guessed official MCP documentation
URL returned 404, its docs index returned 403, and the API pricing page did not
provide usable pricing in this fetch. **No current API price or official MCP claim
is made here.** [API pricing follow-up](https://www.heygen.com/api-pricing).
Do not substitute a consumer-plan headline price for API generation costs.

**Tavus** is another avatar/conversational-video candidate. Its pricing page was
reachable, but conversational minutes, replica creation, and prerecorded video
are different products. This pass did not verify a prerecorded explainer price
or a generation-capable official MCP. [Pricing follow-up](https://www.tavus.io/pricing).

This is a scoped shortlist, not an exhaustive market survey. Neither avatar
candidate is configured or selected.

## Suggested first experiment (not executed)

1. Pick a single concept and approve a 30–60 second storyboard.
2. Make exact diagram frames from the HTML explanation, with captions and narration.
3. Check live pricing and credit balance; agree on the full purchase and run cap.
4. Render once through JSON2Video. Review correctness, pacing, audio, and captions.
5. Add a short fal clip only if it teaches something the diagram cannot.

## Guardrails before connecting anything

Confirm provider, account, asset upload permission, and a maximum spend including
retries. Do not auto-top-up. Store tokens in client-managed credentials, never in
dotfiles or prompts. Review package provenance, tool permissions, retention terms,
voice consent, commercial rights, and generated asset URL exposure. Use OAuth
where supported; connect only the minimum tools needed. A prompt asking for
approval is not a server-side spending limit.
