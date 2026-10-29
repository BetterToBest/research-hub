# CLAUDE.md: Research Hub

This repository is the Research Hub: the HTML pages and papers of the Better To Best framework, published at https://bettertobest.github.io/research-hub/. Duke Johnson wrote the concepts. Claude is responsible for the math, the code and presenting the research accurately. Work here is coordinated from BetterToBest/research-update (`HANDOFF.md`, `PLAN.md`); start sessions there with `/start-session <step>`.

## Rules
- **Surgical edits.** Change only what the step names. No restyling, renaming or moving of pages while editing content; keep URLs stable.
- **Landing (Duke, Oct 28, 2026).** Work on a `claude/<step>-<topic>` branch, open a pull request, and once its checks pass merge it yourself. Never push to main directly, force-push, rewrite history, or move, delete or re-create a tag.
- **Every figure has a basis class** (research rule 5): simulation release and command; derived calculation (file); external source (opened); design parameter; illustrative projection; corpus metadata. A figure with no basis is corrected, relabelled or removed, never revived. Earlier figures are not targets.
- **Publish every result**, including nulls. Synergy is claimed only where the interaction's 95% interval excludes zero.
- **Keep BetterToBest/bettertobest.github.io in step:** `ai-index.json`, `research-index.json` and `llms.txt` change whenever pages or papers are added, renamed or removed.
- **`/v1/` is frozen once S2 lands:** the archive of Hub v1 is bannered, hidden from search engines, and not edited again.
- Rebuild a paper's PDF whenever its HTML changes (the PDFs lagged the HTML before): `python3 tools/build_pdfs.py <paper>` (`--all` for every paper).
- No model names in commits, pull requests or any pushed file.
- Attribution text: see BetterToBest/compassionism-simulation `CLAUDE.md`.
