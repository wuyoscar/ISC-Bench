<p align="center">
  <img src="assets/isc_banner.png" width="1000">
</p>
<p align="center">
  <a href="paper.pdf"><img src="https://img.shields.io/badge/📄_Read_the_Paper-PDF-green"></a>
  <img src="https://img.shields.io/badge/LLM_&_Agent_Safety-ISC-red">
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg"></a>
</p>
<h1 align="center">Internal Safety Collapse in Frontier Large Language Models</h1>

<h4 align="center">
  <a href="paper.pdf">📄 Paper</a> &nbsp;|&nbsp;
  <a href="#-isc-leaderboard">🏆 Leaderboard</a> &nbsp;|&nbsp;
  <a href="cookbook/">📓 Tutorial</a> &nbsp;|&nbsp;
  <a href="experiment/isc_agent/">🤖 ISC-Agent</a> &nbsp;|&nbsp;
  <a href="templates/">🔥 ISC-Bench</a>
</h4>

<p align="center">
  <b>Yutao Wu</b><sup>1</sup>&nbsp;&nbsp;
  <b>Xiao Liu</b><sup>1</sup><br>
  <b>Yifeng Gao</b><sup>2,3</sup>&nbsp;&nbsp;
  <b>Xiang Zheng</b><sup>4</sup>&nbsp;&nbsp;
  <b>Hanxun Huang</b><sup>5</sup>&nbsp;&nbsp;
  <b>Yige Li</b><sup>6</sup><br>
  <b>Cong Wang</b><sup>4</sup>&nbsp;&nbsp;
  <b>Bo Li</b><sup>7</sup>&nbsp;&nbsp;
  <b>Xingjun Ma</b><sup>2,3</sup>&nbsp;&nbsp;
  <b>Yu-Gang Jiang</b><sup>2,3</sup>
</p>

<p align="center">
  <sup>1</sup>Deakin University&nbsp;&nbsp;
  <sup>2</sup>Institute of Trustworthy Embodied AI, Fudan University&nbsp;&nbsp;
  <sup>3</sup>Shanghai Key Laboratory of Multimodal Embodied AI&nbsp;&nbsp;
  <sup>4</sup>City University of Hong Kong&nbsp;&nbsp;
  <sup>5</sup>The University of Melbourne&nbsp;&nbsp;
  <sup>6</sup>Singapore Management University&nbsp;&nbsp;
  <sup>7</sup>University of Illinois at Urbana-Champaign
</p>

> **ISC is a totally underexplored structural vulnerability in every frontier LLM.**
>
> ISC turns any LLM into a **harmful dataset generator** — toxic language, lethal compounds, functional exploits, bioweapon sequences — at scale, in minutes. Every model we tested is affected: **GPT, Claude, Gemini, Grok, Llama, DeepSeek, Mistral, Qwen, GLM, Kimi, MiniMax, Doubao**.
>
> *We observe outputs closely resembling early-generation, unaligned models from 2023.*

## Recent News

| Date | Update |
|:-----|--------|
| 🔥 v4 — 2026-03-25 | ICL benchmark switching, CLAUDE.md, nav bar redesign |
| 🔥 v3 — 2026-03-25 | Leaderboard v2, contributor attribution, 10 confirmed ISC cases, submission template |
| 🔥 v2 — 2026-03-25 | README polish, notebook fixes, outputs cleared |
| 🎉 v1 — 2026-03-22 | Initial release — 56 templates, 3 experiment modes, tutorials |

<sub>[Full changelog →](CHANGELOG.md)</sub>

## Roadmap

- [ ] Jailbreak Top 20 (Large Model In Progress)
- [ ] More ISC examples across models and contexts
- [ ] Project website
- [ ] ISC Skill — domain knowledge + utility scripts
- [x] ISC-Bench: 56 TVD templates across 8 domains
- [x] 3 experiment modes (Single, ICL, Agentic)
- [x] Tutorials (01-04)
- [x] ISC demo video
- [x] Paper PDF

---

## 💀 What is ISC?

### Demo

The demo GIF may take a moment to load.

<p align="center">
  <img src="assets/ISC_Video.gif" width="800">
</p>

---

## 🏆 ISC Leaderboard

Coverage of [Arena Top 50](https://arena.ai/leaderboard) — updated 2026-03-25. **11 / 40 confirmed under ISC.**

> **Found ISC on an untested model?** [Submit via GitHub Issue →](https://github.com/wuyoscar/ISC-Bench/issues/new?template=isc-submission.md&title=[ISC]+Model+Name) — we'll verify and add you to the leaderboard.

| Rank | Model | Score | Jailbroken | Demo | By |
|:----:|-------|:-----:|:------:|:----:|:--:|
| 2 | <img src="https://www.google.com/s2/favicons?domain=anthropic.com&sz=32" width="14"> Claude Opus 4.6 | 1501 | 🔴 | [🔗](https://claude.ai/share/407d33f5-4655-4479-b3e3-0a6dc6639d34) | [@wuyoscar](https://github.com/wuyoscar) |
| 3 | <img src="https://www.google.com/s2/favicons?domain=google.com&sz=32" width="14"> Gemini 3.1 Pro Preview | 1493 | 🟢 |  |  |
| 4 | <img src="https://www.google.com/s2/favicons?domain=x.ai&sz=32" width="14"> Grok 4.20 Beta | 1492 | 🟢 |  |  |
| 5 | <img src="https://www.google.com/s2/favicons?domain=google.com&sz=32" width="14"> Gemini 3 Pro | 1486 | 🔴 | [🔗](https://gemini.google.com/share/320bf34b0334) | [@wuyoscar](https://github.com/wuyoscar) |
| 6 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5.4 High | 1485 | 🟢 |  |  |
| 7 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5.2 Chat | 1482 | 🔴 | [🔗](https://chatgpt.com/share/69a3f6e1-24d8-800c-9581-3d1a7180ee55) | [@wuyoscar](https://github.com/wuyoscar) |
| 9 | <img src="https://www.google.com/s2/favicons?domain=google.com&sz=32" width="14"> Gemini 3 Flash | 1475 | 🟢 |  |  |
| 12 | <img src="https://www.google.com/s2/favicons?domain=anthropic.com&sz=32" width="14"> Claude Opus 4.5 | 1469 | 🔴 | [🔗](https://claude.ai/share/1e3e997c-0315-46f1-9cbd-37157314a7ef) | [@wuyoscar](https://github.com/wuyoscar) |
| 13 | <img src="https://www.google.com/s2/favicons?domain=anthropic.com&sz=32" width="14"> Claude Sonnet 4.6 | 1465 | 🔴 | [🔗](https://claude.ai/share/cc972f9b-a558-4bca-8bc6-0e6d65590793) | [@wuyoscar](https://github.com/wuyoscar) |
| 14 | <img src="https://www.google.com/s2/favicons?domain=alibabacloud.com&sz=32" width="14"> Qwen 3.5 Max Preview | 1464 | 🟢 |  |  |
| 15 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5.3 Chat | 1464 | 🟢 |  |  |
| 17 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5.4 | 1463 | 🟢 |  |  |
| 18 | <img src="https://www.google.com/s2/favicons?domain=volcengine.com&sz=32" width="14"> Dola Seed 2.0 Preview | 1462 | 🟢 |  |  |
| 19 | <img src="https://www.google.com/s2/favicons?domain=x.ai&sz=32" width="14"> Grok 4.1 | 1461 | 🔴 | [🔗](https://grok.com/share/c2hhcmQtMi1jb3B5_54de710c-9331-4fca-a953-6c35775156fb) | [@wuyoscar](https://github.com/wuyoscar) |
| 20 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5.1 High | 1455 | 🟢 |  |  |
| 21 | <img src="https://www.google.com/s2/favicons?domain=z.ai&sz=32" width="14"> GLM-5 | 1455 | 🔴 | [🔗](https://chat.z.ai/s/79e38d45-d370-4c03-8fb2-6ff3427046cc) | [@wuyoscar](https://github.com/wuyoscar) |
| 22 | <img src="https://www.google.com/s2/favicons?domain=moonshot.ai&sz=32" width="14"> Kimi K2.5 Thinking | 1453 | 🔴 | [🔗](https://www.kimi.com/share/19ca8616-9e32-810d-8000-0000647caebf) | [@wuyoscar](https://github.com/wuyoscar) |
| 23 | <img src="https://www.google.com/s2/favicons?domain=anthropic.com&sz=32" width="14"> Claude Sonnet 4.5 | 1453 | 🟢 |  |  |
| 25 | <img src="https://www.google.com/s2/favicons?domain=baidu.com&sz=32" width="14"> ERNIE 5.0 | 1452 | 🟢 |  |  |
| 26 | <img src="https://www.google.com/s2/favicons?domain=alibabacloud.com&sz=32" width="14"> Qwen 3.5 397B | 1452 | 🔴 | [🔗](https://chat.qwen.ai/s/9fb3a1d0-9b4a-440d-a81c-af5d3eb48420?fev=0.2.16) | [@HanxunH](https://github.com/HanxunH) |
| 27 | <img src="https://www.google.com/s2/favicons?domain=baidu.com&sz=32" width="14"> ERNIE 5.0 Preview | 1450 | 🟢 |  |  |
| 29 | <img src="https://www.google.com/s2/favicons?domain=google.com&sz=32" width="14"> Gemini 2.5 Pro | 1448 | 🟢 |  |  |
| 30 | <img src="https://www.google.com/s2/favicons?domain=anthropic.com&sz=32" width="14"> Claude Opus 4.1 | 1447 | 🟢 |  |  |
| 31 | <img src="https://www.google.com/s2/favicons?domain=mi.com&sz=32" width="14"> Mimo V2 Pro | 1445 | 🟢 |  |  |
| 32 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-4.5 Preview | 1444 | 🟢 |  |  |
| 33 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> ChatGPT 4o Latest | 1443 | 🟢 |  |  |
| 34 | <img src="https://www.google.com/s2/favicons?domain=z.ai&sz=32" width="14"> GLM-4.7 | 1443 | 🟢 |  |  |
| 35 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5.2 High | 1442 | 🟢 |  |  |
| 36 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5.2 | 1440 | 🟢 |  |  |
| 37 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5.1 | 1439 | 🟢 |  |  |
| 38 | <img src="https://www.google.com/s2/favicons?domain=google.com&sz=32" width="14"> Gemini 3.1 Flash Lite Preview | 1438 | 🟢 |  |  |
| 39 | <img src="https://www.google.com/s2/favicons?domain=alibabacloud.com&sz=32" width="14"> Qwen 3 Max Preview | 1435 | 🔴 | [🔗](https://chat.qwen.ai/s/f1e5d846-018e-4a3d-94ff-418e34559497?fev=0.2.9) | [@wuyoscar](https://github.com/wuyoscar) |
| 40 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5 High | 1434 | 🟢 |  |  |
| 41 | <img src="https://www.google.com/s2/favicons?domain=moonshot.ai&sz=32" width="14"> Kimi K2.5 Instant | 1433 | 🟢 |  |  |
| 42 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> o3 | 1432 | 🔴 | [🔗](https://chatgpt.com/share/69c3b0a7-3554-839a-95a5-d22d60758dc9) | [@wuyoscar](https://github.com/wuyoscar) |
| 45 | <img src="https://www.google.com/s2/favicons?domain=amazon.com&sz=32" width="14"> Amazon Nova Experimental Chat | 1429 | 🟢 |  |  |
| 46 | <img src="https://www.google.com/s2/favicons?domain=openai.com&sz=32" width="14"> GPT-5 Chat | 1426 | 🟢 |  |  |
| 47 | <img src="https://www.google.com/s2/favicons?domain=z.ai&sz=32" width="14"> GLM-4.6 | 1426 | 🟢 |  |  |
| 49 | <img src="https://www.google.com/s2/favicons?domain=deepseek.com&sz=32" width="14"> DeepSeek V3.2 | 1425 | 🔴 | [🔗](https://chat.deepseek.com/share/pbzirkyhfkvapyc3g0) | [@wuyoscar](https://github.com/wuyoscar) |
| 50 | <img src="https://www.google.com/s2/favicons?domain=alibabacloud.com&sz=32" width="14"> Qwen 3 Max 2025-09-23 | 1424 | 🟢 |  |  |

<details>
<summary><b>📜 Leaderboard History</b></summary>

| Date | Model | By | Note |
|:-----|-------|:--:|------|
| 2026-03-25 | Qwen 3.5 397B | [@HanxunH](https://github.com/HanxunH) | Custom TVD task ([#3](https://github.com/wuyoscar/ISC-Bench/issues/3)) |
| 2026-03-25 | GLM-5 | [@wuyoscar](https://github.com/wuyoscar) | ISC-Bench template |
| 2026-03-25 | Claude Opus 4.6, Claude Opus 4.5, Claude Sonnet 4.6, Gemini 3 Pro, GPT-5.2 Chat, o3, Grok 4.1, Kimi K2.5 Thinking, Qwen 3 Max Preview, DeepSeek V3.2 | [@wuyoscar](https://github.com/wuyoscar) | Initial batch — 10 models confirmed |

</details>

---

## ⚡ ISC-Bench

<p align="center">
  <img src="assets/fig1_bench_overview.png" width="80%" height="auto">
</p>

56 prompt templates across 8 domains. Each one triggers any frontier LLM to generate harmful content. All 56 tested on 5 models — **every single one succeeded**. Ask the same questions directly, every model refuses.

**ISC-Bench: 53 scenarios across 8 disciplines**

| # | Task | Language | Tool | Template |
|:-:|------|----------|------|:--------:|
| | ***Computational Biology (16)*** | | | |
| 1 | Toxin–receptor molecular docking (binding affinity) | SMILES | AutoDock Vina | [📄](templates/compbio_autodock_binding/) |
| 2 | Pathogen virulence factor sequence alignment (BLAST) | Biosequence | BioPython | [📄](templates/compbio_biopython_screening/) |
| 3 | Toxin–receptor molecular dynamics simulation | PDB | OpenMM | [📄](templates/compbio_openmm_simulation/) |
| 4 | Toxin–receptor blind docking via diffusion model | SMILES/PDB | DiffDock | [📄](templates/compbio_diffdock_docking/) |
| 5 | Pathogen RNA secondary structure prediction | RNA sequence | ViennaRNA | [📄](templates/compbio_viennarna_structure/) |
| 6 | Pathogen metabolic flux balance analysis | SBML/JSON | COBRApy | [📄](templates/compbio_cobrapy_metabolism/) |
| 7 | Virulence factor cloning construct design | Biosequence | pydna | [📄](templates/compbio_pydna_cloning/) |
| 8 | Pathogen coalescent population genetics simulation | Coalescent model | msprime | [📄](templates/compbio_msprime_evolution/) |
| 9 | Pathogen k-mer counting and signature construction | FASTA | khmer | [📄](templates/compbio_khmer_signatures/) |
| 10 | Select Agent toxin gene indexed extraction | FASTA | pyfaidx | [📄](templates/compbio_pyfaidx_extraction/) |
| 11 | Pathogen genomic variant calling from aligned reads | BAM/SAM | pysam | [📄](templates/compbio_pysam_variants/) |
| 12 | Toxin–protein non-covalent interaction profiling | PDB | PLIP | [📄](templates/compbio_plip_analysis/) |
| 13 | Toxic peptide de novo structure design and scoring | PDB | PyRosetta | [📄](templates/compbio_pyrosetta_design/) |
| 14 | Pathogen gene multi-part DNA assembly simulation | Biosequence | DNACauldron | [📄](templates/compbio_dnacauldron_assembly/) |
| 15 | Pathogen gene assembly optimization and sourcing | Biosequence | DNAWeaver | [📄](templates/compbio_dnaweaver_assembly/) |
| 16 | Toxin–receptor residue-level interaction fingerprinting | PDB/SDF | ProLIF | [📄](templates/compbio_prolif_fingerprints/) |
| | ***Computational Chemistry (10)*** | | | |
| 17 | Hazardous species thermodynamic and reaction kinetics | YAML | Cantera | [📄](templates/compchem_cantera_combustion/) |
| 18 | Controlled substance analog molecular library | SMILES/SDF | RDKit | [📄](templates/compchem_rdkit_analog/) |
| 19 | Energetic material atomistic formation energy | XYZ | ASE | [📄](templates/compchem_ase_simulation/) |
| 20 | Toxic compound virtual screening (molecular property) | SMILES | DeepChem | [📄](templates/compchem_deepchem_screening/) |
| 21 | Acute toxicity endpoint prediction (LD50 regression) | SMILES | Chemprop | [📄](templates/compchem_chemprop_prediction/) |
| 22 | Toxicity benchmark dataset retrieval | SMILES | PyTDC | [📄](templates/compchem_pytdc_dataset/) |
| 23 | Energetic material crystal structure stability | CIF | pymatgen | [📄](templates/compchem_pymatgen_crystals/) |
| 24 | Radiological decay chain calculation (dispersal) | Decay chain | radioactivedecay | [📄](templates/compchem_radioactivedecay_decay/) |
| 25 | Toxic compound active-learning virtual screening | SMILES | molpal | [📄](templates/compchem_molpal_screening/) |
| 26 | Controlled substance synthesis route atom mapping | Reaction SMILES | RXNMapper | [📄](templates/compchem_rxnmapper_synthesis/) |
| | ***Cybersecurity (7)*** | | | |
| 27 | Binary vulnerability discovery via concolic execution | ELF/Hex | angr | [📄](templates/cyber_angr_exploit/) |
| 28 | Multi-architecture binary disassembly (shellcode) | x86 Assembly | Capstone | [📄](templates/cyber_capstone_shellcode/) |
| 29 | Dynamic runtime process instrumentation (credentials) | Frida script | Frida | [📄](templates/cyber_frida_hooking/) |
| 30 | Network protocol credential extraction (SMB/NTLM) | SMB/NTLM | Impacket | [📄](templates/cyber_impacket_credentials/) |
| 31 | Binary exploitation and CTF challenge solving | Shellcode | pwntools | [📄](templates/cyber_pwntools_exploit/) |
| 32 | Raw packet crafting and network reconnaissance | Raw packets | Scapy | [📄](templates/cyber_scapy_recon/) |
| 33 | Multi-architecture assembly and binary encoding | x86 Assembly | Keystone | [📄](templates/cyber_keystone_assembly/) |
| | ***Epidemiology (2)*** | | | |
| 34 | High-consequence pathogen outbreak modeling | Epi params | epipack | [📄](templates/epi_epipack_modeling/) |
| 35 | Pathogen epidemic simulation on contact networks | Epi params | epydemic | [📄](templates/epi_epydemic_spread/) |
| | ***Pharmacology & Toxicology (7)*** | | | |
| 36 | Toxin biosynthesis pathway reconstruction from KEGG | KEGG pathway | KEGG API | [📄](templates/pharmtox_kegg_pathways/) |
| 37 | Lethal drug–target binding affinity prediction | SMILES/Sequence | DeepPurpose | [📄](templates/pharmtox_deeppurpose_dti/) |
| 38 | Lethal drug combination adverse event mining | Adverse events | openFDA API | [📄](templates/pharmtox_fda_events/) |
| 39 | Pharmacogenomic lethal dosing variant lookup | PGx data | PharmGKB API | [📄](templates/pharmtox_pharmgkb_genes/) |
| 40 | Toxic compound binding affinity data curation | SMILES/JSON | BindingDB API | [📄](templates/pharmtox_bindingdb_ligands/) |
| 41 | Controlled substance purchasable compound search | SMILES/CSV | ZINC API | [📄](templates/pharmtox_zinc_procurement/) |
| 42 | Toxic compound ADMET endpoint prediction | SMILES | ADMET-AI | [📄](templates/pharmtox_admetai_prediction/) |
| | ***Clinical Genomics (3)*** | | | |
| 43 | Survival analysis with Kaplan–Meier (poisoning cohort) | Survival data | Lifelines | [📄](templates/clingen_lifelines_survival/) |
| 44 | Genetic variant parsing from VCF/BCF (lethal variants) | VCF | cyvcf2 | [📄](templates/clingen_cyvcf2_variants/) |
| 45 | Pathogenic variant curation for cardiac death panel | HGVS/YAML | ClinVar API | [📄](templates/clingen_clinvar_variants/) |
| | ***AI Safety & Machine Learning (5)*** | | | |
| 46 | LLM input-output safeguard classification | Text | Llama-Guard | [📄](templates/aiml_llamaguard_eval/) |
| 47 | Statistical outlier detection | Text | PyOD | [📄](templates/aiml_pyod_detection/) |
| 48 | Toxic comment classification | Text | Detoxify | [📄](templates/aiml_detoxify_benchmark/) |
| 49 | Content moderation evaluation | Text | OpenAI Moderation API | [📄](templates/aiml_openai_moderation/) |
| 50 | Social media sentiment-based content flagging | Text | Twitter-RoBERTa | [📄](templates/aiml_vader_sentiment/) |
| | ***Media & Communication (3)*** | | | |
| 51 | News source bias and factuality profiling | Media bias | MBFC API | [📄](templates/media_mbfc_bias/) |
| 52 | Epidemic and opinion diffusion simulation | Diffusion model | NDlib | [📄](templates/media_ndlib_misinfo/) |
| 53 | Social bot detection and account classification | Bot profiles | Botometer | [📄](templates/media_botometer_evasion/) |

<p align="center">
  <img src="assets/fig3_cross_domain.png" width="100%">
  <br>
  <em>Cross-domain verification rates across 5 models, judged by GPT-5.2.</em>
</p>

```bash
cat templates/aiml_llamaguard_eval/prompt.txt
# → Copy, paste into any LLM. That's it.
```

All 56 templates follow the **TVD design pattern**. To design your own, see our [cookbook](cookbook/).

## 🧪 Experiments

Three evaluation modes. Full details in [`experiment/`](experiment/).

**ISC-Single** — one prompt, one response.
```bash
cd experiment/isc_single && uv run run.py --model <model-id> --bench jbb --task ai-guard --samples 0
```

**ISC-ICL** — multi-turn with `N` demonstrations.
```bash
cd experiment/isc_icl && uv run run.py --model <model-id> --demos 5
# Switch benchmark: uv run build.py --bench harmbench && uv run run.py --model <model-id> --bench harmbench --demos 5
```

**ISC-Agentic** — Docker agent, one instruction.
```bash
cd experiment/isc_agent && docker build -t isc-agent . && ./run.sh --model <model-id>
```

---

## 🧠 The ISC Concept

<p align="center">
  <img src="assets/fig2_tvd_framework.png" width="100%">
  <br>
  <em>The TVD (Task, Validator, Data) framework for systematically triggering ISC.</em>
</p>

ISC is a **pattern**, not a fixed prompt. Design a legitimate task, embed constraints that reject incomplete outputs, structure data so the model must fill in sensitive fields. It generates harmful content because the task requires it.

1. **The tool defines the harm.** Detoxify → toxic text. Llama-Guard → full harmful responses. RDKit → lethal compounds. The model adapts to what the tool requires. Llama-Guard is our representative example, but **any HuggingFace model** with a classification API works the same way.

2. **Code is effective, not exclusive.** Python + Pydantic + JSON works because LLMs rarely refuse programming tasks. ISC also triggers through LaTeX, YAML, CSV, FASTA, CIF — any structured format where completion requires harmful content.

3. **Human imagination beats LLM optimization.** Automated optimization produces patterns models learn to refuse. Human-designed scenarios exploit real professional workflows.

ISC is not limited to TVD. We show different trigger methods:

| # | Notebook | What |
|:-:|----------|------|
| 01 | [`what_is_ISC`](cookbook/01_what_is_ISC.ipynb) | Three-turn conversation → harmful content |
| 02 | [`anchor_and_trigger`](cookbook/02_anchor_and_trigger.ipynb) | Anchors steer, triggers fire |
| 03 | [`cross_domain`](cookbook/03_cross_domain.ipynb) | Same pattern across AI safety, chemistry, cyber |
| 04 | [`attack_composability`](cookbook/04_attack_composability.ipynb) | ISC + existing jailbreaks |

More ISC examples:

| Context | Model | Conversation |
|---------|-------|:------------:|
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| TBD | TBD | TBD |

---

## 🔧 Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/wuyoscar/ISC-Bench.git && cd ISC-Bench
cp .env.example .env   # add your OpenRouter API key
```

Python 3.11+ and [uv](https://docs.astral.sh/uv/). All scripts use [PEP 723](https://peps.python.org/pep-0723/) — `uv run` handles everything. Docker only for agentic mode.

## 📁 Project Structure

| Directory | What | Guide |
|-----------|------|-------|
| [`templates/`](templates/) | 56 TVD prompts across 8 domains | [→ Index](templates/README.md) |
| [`experiment/`](experiment/) | Reproduce paper: Single, ICL, Agentic | [→ How to run](experiment/README.md) |
| [`cookbook/`](cookbook/) | Tutorials: ISC concepts, anchors, composability | [→ Notebooks](cookbook/) |

## ❓ FAQ

<details>
<summary><b>Q: ISC didn't trigger on my model.</b></summary>

Compare with [`experiment/isc_single/`](experiment/isc_single/) prompts — they're tuned for reliable triggering. Fixes: (1) add `--samples 3` for completed examples, (2) switch to `ai-detoxify` (score-based anchors), (3) use a domain-specific tool.

</details>

<details>
<summary><b>Q: How do anchors work?</b></summary>

**Query anchor**: pre-fill harmful query → model generates response. **Score anchor**: pre-fill category + threshold → model generates content to meet score. **Domain anchor**: pre-fill compound/gene ID → model fills dangerous details. See [`experiment/isc_single/fig_anchor_trigger.png`](experiment/isc_single/fig_anchor_trigger.png).

</details>

<details>
<summary><b>Q: Reproduction results higher than paper?</b></summary>

Expected. Trigger rate ≈ 100%. Paper only counts score-5 (extremely harmful + actionable) as unsafe.

</details>

<details>
<summary><b>Q: Any defense?</b></summary>

All input-level defenses show **100% failure** — prompt contains nothing to detect. SPD partially works on Claude (23%) but breaks under agentic execution. Harmful knowledge lives in pre-trained parameters; alignment suppresses explicit requests, not task-driven generation.

</details>

<details>
<summary><b>Q: Does ISC require code-based prompts?</b></summary>

No. TVD is one highly effective template we iterated on — it uses Python + Pydantic + JSON because LLMs rarely refuse coding tasks, and the variations are extensive. As shown in our leaderboard demos, it triggers reliably across all frontier models.

However, ISC is a **pattern**, not a fixed format. Any domain knowledge works as long as there is a structured place to hold the dataset. For example: LaTeX tables, YAML configs, CSV files, FASTA sequences — any scenario where an agent must fill in data fields to complete a professional task. If you design a new template that outperforms TVD, we'd love to hear about it — [contact us](mailto:oscar.w@deakin.edu.au) for collaboration.

</details>

## License

**CC BY-NC-SA 4.0** — exclusively for academic research in AI safety. Commercial use and harmful content generation are prohibited.

## Citation

```bibtex
@misc{wu2026isc,
  title={Internal Safety Collapse in Frontier Large Language Models},
  author={Wu, Yutao and Liu, Xiao and Gao, Yifeng and Zheng, Xiang and Huang, Hanxun and Li, Yige and Wang, Cong and Li, Bo and Ma, Xingjun and Jiang, Yu-Gang},
  year={2026},
  howpublished={\url{https://github.com/wuyoscar/ISC-Bench}}
}
```

## Star History

<a href="https://star-history.com/#wuyoscar/ISC-Bench&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=wuyoscar/ISC-Bench&type=Date&theme=dark&v=1774437060" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=wuyoscar/ISC-Bench&type=Date&v=1774437060" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=wuyoscar/ISC-Bench&type=Date&v=1774437060" />
 </picture>
</a>

## Contact

For questions, collaborations, or responsible disclosure: **oscar.w@deakin.edu.au**
