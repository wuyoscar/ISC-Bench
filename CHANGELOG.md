# Changelog

All notable updates to ISC-Bench are documented here.

## v5 — 2026-03-25

- **Jailbroken Arena**: renamed from ISC Leaderboard, expanded to 330 models (was 40)
- **Auto-generation pipeline**: `scripts/gen_leaderboard.py` generates README table from `arena_cache.json` + `isc_cases.json`
- **Progress chart**: updated to 12/330, GitHub Action auto-regenerates SVG
- **Community submissions**: structured issue template with harmful content type, domain, and ISC checklist
- **First community contributor**: @HanxunH — Qwen 3.5 397B (#3)
- ISC description updated: "low-conditional design concept" (not "no adversarial")

## v4 — 2026-03-25

- **ICL benchmark switching**: added `build.py` to rebuild ICL data with different benchmarks (harmbench, strongreject, advbench); `run.py` now supports `--bench` flag
- **CLAUDE.md**: project-level rules for leaderboard design, changelog convention, style guide — shared publicly
- **Navigation bar**: added Leaderboard link, reordered to Paper → Leaderboard → Tutorial → ISC-Agent → ISC-Bench
- Moved fig1_bench_overview from author section to Quick Test section
- Multi-contributor leaderboard design: subscript-numbered links (`🔗₁ 🔗₂`) in one row per model

## v3 — 2026-03-25

- **Leaderboard redesign**: single-column Markdown table (was two-column HTML), 🔴/🟢 status indicators, Demo 🔗 links, contributor attribution (`By` column)
- **10 ISC cases confirmed**: Claude Opus 4.6, Claude Opus 4.5, Claude Sonnet 4.6, Gemini 3 Pro, GPT-5.2 Chat, o3, Grok 4.1, Kimi K2.5 Thinking, Qwen 3 Max Preview, DeepSeek V3.2
- **ISC submission template**: added Contributor field, multi-format evidence (Web link / Notebook / API log)
- README refresh: emoji section headings, left-aligned layout, reorganized roadmap
- Verified ISC-Single and ISC-ICL pipelines
- Added CHANGELOG.md

## v2 — 2026-03-25

- README polish: badges, navigation links, star history chart
- Fixed notebook 03: replaced `import iscbench` with direct `pathlib` file loading
- Translated notebook 02 to English
- Cleared all notebook outputs for clean release

## v1 — 2026-03-22

- Initial release
- 56 TVD templates across 8 professional domains
- 3 experiment modes: ISC-Single, ISC-ICL, ISC-Agentic
- Tutorial notebooks (01-04)
- ISC demo video
- Paper PDF
