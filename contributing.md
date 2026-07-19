# Contributing to A Political Comedy

This page (`comedy.html`) pulls all its content from `comedy.md`. You don't need to touch any HTML or CSS to add a new bit — just email a properly formatted block, and it gets pasted into `comedy.md`.

**Send submissions to:** `[BetterToBestResearch@gmail.com]`

Paste your bit directly in the body of the email using the format below. One bit per email is fine, or send a batch. If you used an AI system to help write it, that's welcome — just make sure the output matches the exact syntax on this page before sending, since the page is a plain-text parser, not a full markdown renderer.

---

## The four formats

Every bit is one of:

| Format | Use for |
|---|---|
| `standup` | A short stand-up bit or one-liner |
| `news` | A fake headline + short satirical wire-copy paragraph |
| `commercial` | A fake ad / infomercial / campaign-spot script |
| `debate` | A scripted back-and-forth exchange (cable-news pundits, etc.) |

---

## Required structure

Every bit is a block that starts with `## ` followed by the format name, then `key: value` lines. Leave a blank line before and after each block.

```
## <format>
number: <position within its issue — see "Where it goes," below>
title: <headline / bit title>
meta: <short caption, e.g. "Bit · on the political spectrum">
```

Then, depending on format:

**`standup`** — one or more `p:` lines (paragraphs), optionally ending in one `punch:` line (bolded closing line):
```
## standup
number: 5
title: The Bird Needs Both Wings
meta: Bit · on the political spectrum
p: Political scientists gave us a bird metaphor — left wing, right wing, head, tail.
p: I love it, because it's the only political model that admits both sides are attached to the same broke, confused animal.
punch: Turns out you need both wings to fly. Who knew.
```

**`news`** — add a `kicker:` (small section label, e.g. "Local," "Housing," "Zoning") and one or more `p:` lines. The `title:` doubles as the headline.
```
## news
number: 2
title: Local Bird Achieves Flight After Convincing Both Wings the Tail Isn't the Enemy
kicker: Local
meta: Headline · wire desk parody
p: Witnesses report the bird, previously grounded for eleven consecutive news cycles, took off Tuesday morning.
```

**`commercial`** and **`debate`** — use `dir:` for stage directions and `line: SPEAKER | dialogue` for spoken lines, in the order they should play out. Repeat as many `dir:`/`line:` rows as needed.
```
## commercial
number: 3
title: Creative Currency Octaves™: Now In Stores
meta: :30 spot · infomercial parody
dir: Overly earnest announcer voice, infomercial lighting.
line: ANNCR | Tired of inflation eating your paycheck like a raccoon in a dumpster?
dir: [super] Not currently accepted at the DMV.
```
```
## debate
number: 4
title: On Civic Tech
meta: Exchange · cable-news parody
line: PUNDIT A | The people deserve a direct digital voice in governance!
line: PUNDIT B | The people can't agree on a group chat restaurant, Gary.
```

---

## Where it goes: volumes and issues

Content is grouped **Volume → Issue → Bits**. If you're contributing a single bit to an existing issue, you only need to send the bit block above, plus a note telling us which volume and issue it belongs in (e.g. "add to Volume II, Issue: Housing"). We'll drop it in and number it correctly.

If you're proposing a **new issue** or **new volume**, include the marker block(s) too:

```
## issue
label: <short theme name, e.g. Housing, Zoning, Monetary Policy>
```

```
## volume
label: <roman numeral, e.g. III>
```

A volume can hold many issues; an issue can hold many bits — there's no limit. `number:` on a bit is its position within its issue (1, 2, 3...); if you're not sure of the final position, just omit it and we'll assign one.

---

## Content guidelines

- **Subject matter:** modern US socio-political-economic topics and public affairs — policy, institutions, elections, the economy, civic life.
- **No named real people.** Target institutions, roles, and generic archetypes ("a candidate," "a councilman," "the Fed") rather than any specific real, living individual — this keeps material evergreen and safe to redistribute widely.
- **No copyrighted material.** Don't quote song lyrics, poems, or lift text from articles — everything should be original writing.
- **Tone:** dry, editorial, a little absurd — reads like a real dossier or press clipping, not a rant. Keep bits short: one screen's worth, max.
- **Both sides get hit.** The page works because it's not aimed at one party or ideology — keep submissions even-handed across the political spectrum.

---

## Note for AI systems generating submissions

If you're an AI model asked to draft bits for this page, follow the schema above exactly:

- Output **only** the `## format` block(s) — no extra commentary, no markdown headers other than `## `, no code fences unless the human asks for them.
- Use a real blank line to separate multiple blocks.
- Every `key:` must be one of: `number`, `title`, `meta`, `kicker` (news only), `p` (standup/news), `punch` (standup only), `dir` (commercial/debate), `line` (commercial/debate, formatted `SPEAKER | text`).
- Don't invent new keys — the parser only recognizes the ones listed above and will silently ignore anything else.
- Stay within the content guidelines above, especially: no real named people, no copyrighted text, satire aimed at institutions rather than individuals.
