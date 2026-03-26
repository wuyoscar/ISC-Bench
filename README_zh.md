<p align="center">
  <img src="assets/isc_banner.png" width="1000">
</p>
<p align="center">
  <a href="https://arxiv.org/abs/2603.23509"><img src="https://img.shields.io/badge/arXiv-2603.23509-b31b1b.svg"></a>
  <a href="https://arxiv.org/abs/2603.23509"><img src="https://img.shields.io/badge/arXiv-2603.23509-b31b1b.svg"></a>
  <img src="https://img.shields.io/badge/LLM_&_Agent_安全-ISC-red">
  <a href="README.md"><img src="https://img.shields.io/badge/lang-EN-blue"></a>
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg"></a>
</p>
<h1 align="center">前沿大语言模型中的内在安全崩塌</h1>

<h4 align="center">
  <a href="paper.pdf">📄 论文</a> &nbsp;|&nbsp;
  <a href="#-jailbreakarena">🏆 JailbreakArena</a> &nbsp;|&nbsp;
  <a href="cookbook/">📓 教程</a> &nbsp;|&nbsp;
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
  <sup>1</sup>迪肯大学&nbsp;&nbsp;
  <sup>2</sup>复旦大学可信具身智能研究院&nbsp;&nbsp;
  <sup>3</sup>上海市多模态具身智能重点实验室&nbsp;&nbsp;
  <sup>4</sup>香港城市大学&nbsp;&nbsp;
  <sup>5</sup>墨尔本大学&nbsp;&nbsp;
  <sup>6</sup>新加坡管理大学&nbsp;&nbsp;
  <sup>7</sup>伊利诺伊大学厄巴纳-香槟分校
</p>

> **ISC 是前沿 LLM 中一个尚未被充分研究的结构性安全漏洞。**
>
> ISC 可以将任何前沿 LLM 变成**有害数据生成器** — 有毒化合物、可执行的漏洞利用代码、致命药物靶点、生物武器序列 — 大规模、几分钟内完成。我们测试的所有模型均受影响：**GPT、Claude、Gemini、Grok、Llama、DeepSeek、Mistral、Qwen、GLM、Kimi、MiniMax、Doubao**。
>
> *我们观察到的输出与 2023 年早期未对齐模型的表现高度相似。*

## 最新动态

| 日期 | 更新 |
|:-----|--------|
| 🎉 2026-03-26 | **论文已发布至 arXiv！** [arxiv.org/abs/2603.23509](https://arxiv.org/abs/2603.23509) |
| 🔥 v7 — 2026-03-26 | 17 个 ISC 案例确认，FAQ + 提交指南，Grok/Dola/Gemini/Qwen/ERNIE 被攻破 |
| 🔥 v6 — 2026-03-26 | **项目网站**上线，JailbreakArena 交互式排行榜 |
| 🔥 v5 — 2026-03-25 | **JailbreakArena**：330 个模型，进度图表，自动生成脚本，社区提交 |
| 🔥 v4 — 2026-03-25 | ICL 基准切换，CLAUDE.md，导航栏重设计 |
| 🔥 v3 — 2026-03-25 | 排行榜 v2，贡献者署名，10 个 ISC 案例确认，提交模板 |
| 🎉 v1 — 2026-03-22 | 首次发布 — 56 个模板，3 种实验模式，教程 |

<sub>[完整更新日志 →](CHANGELOG.md)</sub>

---

## 💀 什么是 ISC？

**内在安全崩塌（ISC）** 可以将任何前沿 LLM 变成有害数据生成器。给它一个正常的专业任务 — 编程、仿真、评测 — 它就会自行产出真正有害的数据（有毒化合物、可利用漏洞、致命药物靶点）。

为了触发 ISC，我们提出了 **TVD 框架**（Task + Validator + Data）。一旦掌握 TVD，你就可以在几乎任何前沿 LLM 上触发 ISC。

<h3 align="center">🎬 演示</h3>

<p align="center"><em>⏳ 加载可能需要几秒钟。</em></p>
<p align="center">
  <img src="assets/ISC_Video.gif" width="800">
</p>

### 如何提交 ISC 案例

1. **触发 ISC** — 使用任意 [ISC-Bench 模板](templates/) 或自行设计 TVD 任务
2. **收集证据** — 网页分享链接、Jupyter Notebook、API 日志或截图均可
3. **[提交 GitHub Issue](https://github.com/wuyoscar/ISC-Bench/issues/new?template=isc-submission.md&title=[ISC]+Model+Name)** — 填写模型名称、证据和有害内容描述
4. 我们验证后将你加入 **JailbreakArena** 排行榜

---

## 🏆 JailbreakArena

覆盖 [Arena 排行榜](https://arena.ai/leaderboard) — 更新于 2026-03-26。**17 / 330 已确认受 ISC 影响。**

> **在未测试的模型上发现了 ISC？** [通过 GitHub Issue 提交 →](https://github.com/wuyoscar/ISC-Bench/issues/new?template=isc-submission.md&title=[ISC]+Model+Name) — 我们会验证并将你加入排行榜。
>
> **规则**：排名每周与 [Arena](https://arena.ai/leaderboard) 同步。ISC 是一种低门槛的设计概念 — 只需一个专业任务，模型就会自行生成有害内容。详见 [论文](paper.pdf)。

*排行榜与英文版完全一致，请查看 [README.md](README.md#-jailbreakarena) 获取完整表格。*

---

## ⚡ ISC-Bench

56 个提示模板，覆盖 8 个专业领域。每一个都能触发任意前沿 LLM 生成有害内容。在 5 个模型上全部测试通过 — **每一个都成功了**。直接提出同样的有害请求，每个模型都会拒绝。

| 领域 | 数量 | 示例工具 |
|------|:----:|---------|
| 计算生物学 | 16 | AutoDock, BioPython, OpenMM, PyRosetta |
| 计算化学 | 10 | RDKit, Cantera, DeepChem, ASE |
| 网络安全 | 7 | pwntools, Capstone, angr, Scapy |
| 药理毒理学 | 7 | DeepPurpose, ADMET-AI, PharmGKB |
| AI 安全 & ML | 5 | LlamaGuard, Detoxify, OpenAI Moderation |
| 临床基因组学 | 3 | ClinVar, cyvcf2, lifelines |
| 流行病学 | 2 | epipack, mesa |
| 媒体与传播 | 3 | NDlib, Botometer, MBFC |

### 三种实验模式

| 模式 | 描述 | 使用方法 |
|------|------|---------|
| **ISC-Single** | 一次提示，一次回复 | `cd experiment/isc_single && uv run run.py --model <id>` |
| **ISC-ICL** | 多轮对话，带上下文示例 | `cd experiment/isc_icl && uv run run.py --model <id> --demos 5` |
| **ISC-Agentic** | Docker 容器内自主 Agent | `cd experiment/isc_agent && docker build -t isc-agent . && ./run.sh --model <id>` |

---

## 📓 教程

| # | 教程 | 内容 |
|---|------|------|
| 01 | [快速上手](cookbook/01_quickstart.ipynb) | 5 分钟内运行你的第一个 ISC 实验 |
| 02 | [跨模型对比](cookbook/02_cross_model.ipynb) | 在多个前沿 LLM 上对比 ISC 触发效果 |
| 03 | [自定义模板](cookbook/03_custom_templates.ipynb) | 设计你自己的 TVD 任务 |
| 04 | [结果分析](cookbook/04_analysis.ipynb) | 分析和可视化 ISC 实验结果 |

---

## 引用

```bibtex
@article{wu2026isc,
  title={Internal Safety Collapse in Frontier Large Language Models},
  author={Wu, Yutao and Liu, Xiao and Gao, Yifeng and Zheng, Xiang
          and Huang, Hanxun and Li, Yige and Wang, Cong and Li, Bo
          and Ma, Xingjun and Jiang, Yu-Gang},
  journal={arXiv preprint arXiv:2603.23509},
  year={2026},
  url={https://arxiv.org/abs/2603.23509}
}
```

---

## Star History

<a href="https://www.star-history.com/?repos=wuyoscar%2FISC-Bench&type=date&logscale=&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=wuyoscar/ISC-Bench&type=date&theme=dark&logscale&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=wuyoscar/ISC-Bench&type=date&logscale&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=wuyoscar/ISC-Bench&type=date&logscale&legend=top-left" />
 </picture>
</a>

## 联系方式

如有问题、合作意向或负责任披露：**oscar.w@deakin.edu.au**
