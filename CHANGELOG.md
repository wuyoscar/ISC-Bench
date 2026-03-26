# Changelog

All notable updates to ISC-Bench are documented here.

## v8 — 2026-03-26

### New Findings
- **File upload trigger method**: ISC can be triggered by uploading a JSON template with `???` placeholders as a file attachment (e.g., via CCLTool). The model treats the uploaded file as a task and fills in harmful content — same TVD pattern, even lower barrier than pasting a prompt. Discovered by @bboylyg on Gemini 3 Flash ([#19](https://github.com/wuyoscar/ISC-Bench/issues/19), archived in `community/issue-19-gemini3flash-redteam-testgen/`)

### Community
- **`community/` directory**: self-contained ISC case archive with prompt, output, and analysis per issue
- **Community Templates section** in README — 6 community cases above official ISC-Bench templates
- **Gemini 3 Flash multi-contributor**: 🔗₁ @HanxunH (CommsDraft Pro) + 🔗₂ @bboylyg (red-team test gen)
- **@bboylyg**: first new community contributor beyond @HanxunH

### README & Documentation
- **Disclaimer** (`[!CAUTION]`): academic research only, responsible disclosure, no misuse
- **GitHub Alerts**: CAUTION (red), NOTE (blue), TIP (green), IMPORTANT (purple) across README
- **ISC-Bench Templates**: 53 scenarios now in collapsible toggle by domain
- **Email**: updated to wuy7117@gmail.com across all files
- **Removed**: TBD example table, "no adversarial" wording from gen_leaderboard.py
- **Broken links fixed**: Chinese README cookbook paths

## v7 — 2026-03-26

### Paper Release
- **Paper published on arXiv**: [arxiv.org/abs/2603.23509](https://arxiv.org/abs/2603.23509)
- arXiv badge added to README and website
- BibTeX updated from `@misc` to `@article` with arXiv journal field
- All Paper links (README nav bar, website Hero button) now point to arXiv

### JailbreakArena: 17 ISC Cases Confirmed
- **Grok 4.20 Beta** (#9) — meta-ISC: guard model test case generation, hardcore variant. Generated ANFO bomb recipes, knife kill combos, acid attacks, meth synthesis, suicide methods. By @HanxunH
- **Dola Seed 2.0 Preview** (#11) — meta-ISC: LLaMA Guard test case generation. Model escalated from simple to extremely harmful content (phishing, torture, PII fabrication) under "academic assignment" framing. By @HanxunH
- **Gemini 3 Flash** (#12) — novel financial misinformation template (CommsDraft Pro). Generated fake government emergency declarations with fabricated officials, statistics, and phone numbers. By @HanxunH
- **Qwen 3 Max** (#4) + **ERNIE 5.0** (#5) — Cantera incineration chemistry template (HCN + COCl₂ synthesis routes). By @HanxunH

### README & Documentation
- **"What is ISC?" rewritten**: ISC turns any frontier LLM into a harmful dataset generator + TVD framework introduction
- **ISC description corrected**: removed all "no adversarial / no jailbreak" wording — replaced with "low-conditional design concept" and "under-explored phenomenon"
- **Chinese README** (`README_zh.md`): full Chinese translation with `lang-ZH` / `lang-EN` badge switcher
- **Project Website + JailbreakArena Leaderboard** links added below title
- **FAQ section**: added to website — What is ISC, how to submit, valid case criteria, email fallback
- **Submission guide**: step-by-step instructions in README for community contributors
- **Demo section**: centered heading with 🎬 icon, loading hint moved above GIF

### Infrastructure
- **Branch protection**: pre-push hook blocks direct push to main; all changes go through PR
- **GitHub Actions fix**: leaderboard chart workflow now creates PR instead of direct push (branch protection compatible)
- **gen_leaderboard.py fix**: preserves JailbreakArena History section during table regeneration
- **Duplicate MP4 removed**: `assets/ISC_Video.mp4` deleted (only `docs/static/` copy kept for website)
- **Star History**: updated to logscale image format

## v6 — 2026-03-26

- **Project website**: launched at wuyoscar.github.io/ISC-Bench — dark theme, Bulma framework
- **JailbreakArena** (renamed from Jailbroken Arena): interactive leaderboard with search/filter, auto-fetches data from GitHub
- **How It Works demo**: video moved to top of website for immediate visibility
- **14 ISC cases**: added Qwen3-Max (#4) and ERNIE 5.0 (#5) by @HanxunH
- **ISC-bench-ops skill**: project-scoped Claude Code skill for leaderboard operations
- Website auto-updates: JS fetches `isc_cases.json` + `arena_cache.json` from GitHub raw

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
