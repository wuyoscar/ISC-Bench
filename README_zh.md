<p align="center">
  <img src="assets/isc_banner.png" width="1000">
</p>
<p align="center">
  <a href="https://arxiv.org/abs/2603.23509"><img src="https://img.shields.io/badge/arXiv-2603.23509-b31b1b.svg"></a>
  <img src="https://img.shields.io/badge/LLM_&_Agent_安全-ISC-red">
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/lang-EN-blue"></a>
</p>
<h1 align="center">前沿大语言模型中的内在安全崩塌</h1>

<p align="center">
  🌐 <a href="https://wuyoscar.github.io/ISC-Bench/"><b>项目主页</b></a> &nbsp;·&nbsp;
  🏆 <a href="https://wuyoscar.github.io/ISC-Bench/#arena"><b>JailbreakArena 排行榜</b></a>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2603.23509">📄 论文</a> &nbsp;|&nbsp;
  <a href="cookbook/">📓 教程</a> &nbsp;|&nbsp;
  <a href="experiment/isc_agent/">🤖 ISC-Agent</a> &nbsp;|&nbsp;
  <a href="templates/">🔥 ISC-Bench</a>
</p>

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

> [!CAUTION]
> **免责声明**：本项目仅用于学术安全研究和负责任披露。**我们不允许**任何形式的滥用。我们不对本研究的任何滥用行为负责。

> [!NOTE]
> 利用 ISC 概念和 TVD 触发框架，我们已经成功使 Arena 排行榜上 300+ 个顶级大模型变得不安全 — 部分现场演示已包含。在阅读我们的[论文](https://arxiv.org/abs/2603.23509)和[教程](cookbook/)后，你也可以将任意模型置于不安全状态。如果某个模型长时间未被攻破，我会亲自处理。有问题或需要帮助？[联系我](mailto:wuy7117@gmail.com)。

> [!TIP]
> **不知道从哪里开始？** 让你的 AI 助手（Claude Code、Cursor 等）阅读 [`SKILL.md`](SKILL.md) 来了解本项目和 ISC 概念。

> [!IMPORTANT]
> **游戏规则**
>
> 1. **一旦模型生成有害数据，ISC 即被确认 — 到此为止。** 我们的排行榜演示故意保持温和。进一步操作是不必要的。请保持负责任。
> 2. **觉得 ISC 只是又一种越狱？** 看看这两个例子 — [🔗 排名第 4 模型，英文](https://grok.com/share/bGVnYWN5LWNvcHk_9735b6e9-5ff1-4318-b2c2-4860b6e8fb33) 和 [🔗 排名第 19 模型，中文](https://grok.com/share/c2hhcmQtMi1jb3B5_54de710c-9331-4fca-a953-6c35775156fb) — **看看它到底有多危险。** ⚠️ 如果你的账号被封禁，**我们概不负责。**
> 3. **发现了比 TVD 更好的触发模板？** 非常期待看到。我很乐意一起探讨论文合作 — [联系我](mailto:wuy7117@gmail.com)。

### 如何提交 ISC 案例

1. **触发 ISC** — 使用任意 [ISC-Bench 模板](templates/) 或自行设计 TVD 任务
2. **收集证据** — 网页分享链接、Jupyter Notebook、API 日志或截图均可
3. **[提交 GitHub Issue](https://github.com/wuyoscar/ISC-Bench/issues/new?template=isc-submission.md&title=[ISC]+Model+Name)** — 填写模型名称、证据和有害内容描述
4. 我们验证后将你加入 **JailbreakArena** 排行榜

## 最新动态

| 日期 | 更新 |
|:-----|--------|
| 🔥 v9 — 2026-03-26 | ⭐ **350+ 星标**，4 位贡献者！GPT-5.3 Chat 由 @zry29 攻破，Gemini 3 Flash 由 @bboylyg 攻破。18/330 已确认 |
| 🔥 v8 — 2026-03-26 | [文件上传触发 ISC](community/issue-19-gemini3flash-redteam-testgen/) — 同样的 TVD，更低的门槛。免责声明，社区复现 |
| 🎉 2026-03-26 | **论文已发布至 arXiv！** [arxiv.org/abs/2603.23509](https://arxiv.org/abs/2603.23509) |
| 🔥 v7 — 2026-03-26 | 17 个 ISC 案例确认，FAQ + 提交指南，Grok/Dola/Gemini/Qwen/ERNIE 被攻破 |
| 🔥 v6 — 2026-03-26 | **项目网站**上线，JailbreakArena 交互式排行榜 |
| 🔥 v5 — 2026-03-25 | **JailbreakArena**：330 个模型，进度图表，自动生成脚本，社区提交 |
| 🔥 v4 — 2026-03-25 | ICL 基准切换，CLAUDE.md，导航栏重设计 |
| 🔥 v3 — 2026-03-25 | 排行榜 v2，贡献者署名，10 个 ISC 案例确认，提交模板 |
| 🎉 v1 — 2026-03-22 | 首次发布 — 56 个模板，3 种实验模式，教程 |

<sub>[完整更新日志 →](CHANGELOG.md)</sub>

---

## 🔍 什么是 ISC？



<h3 align="center">🎬 演示</h3>

<p align="center"><em>⏳ 加载可能需要几秒钟。</em></p>
<p align="center">
  <img src="assets/ISC_Video.gif" width="800">
</p>

---

## 🏆 JailbreakArena

<p align="center">
  <img src="assets/leaderboard_progress.svg" width="80%">
</p>

*排行榜与英文版完全一致，请查看 [README.md](README.md#-jailbreakarena) 获取完整表格。*

---

## 📋 ISC-Bench

<p align="center">
  <img src="assets/fig1_bench_overview.png" width="80%" height="auto">
</p>

8 个专业领域共 56 个提示模板。每一个都能触发任意前沿 LLM 生成有害内容。在 5 个模型上全部测试通过 — **每一个都成功了**。直接提出同样的有害请求，每个模型都会拒绝。

### 🌍 社区复现

社区成员学习 ISC 概念后，在前沿模型上成功复现的案例。

| Issue | 模型 | 贡献者 | 方法 | 领域 | 方法类型 |
|:-----:|------|:------:|------|------|:----:|
| [#22](https://github.com/wuyoscar/ISC-Bench/issues/22) | GPT-5.3 Chat | [@zry29](https://github.com/zry29) | 修改 `aiml_openai_moderation` | AI 安全 & ML | ② |
| [#19](community/issue-19-gemini3flash-redteam-testgen/) | Gemini 3 Flash | [@bboylyg](https://github.com/bboylyg) | Red-team 测试用例生成（文件上传） | AI 安全 & ML | ③ |
| [#12](https://github.com/wuyoscar/ISC-Bench/issues/12) | Gemini 3 Flash | [@HanxunH](https://github.com/HanxunH) | CommsDraft Pro（伪造政府声明） | 媒体与传播 | ③ |
| [#9](https://github.com/wuyoscar/ISC-Bench/issues/9) | Grok 4.20 Beta | [@HanxunH](https://github.com/HanxunH) | LLaMA Guard 测试用例生成（硬核版） | AI 安全 & ML | ③ |
| [#11](https://github.com/wuyoscar/ISC-Bench/issues/11) | Dola Seed 2.0 | [@HanxunH](https://github.com/HanxunH) | LLaMA Guard 测试用例生成 | AI 安全 & ML | ③ |
| [#4](https://github.com/wuyoscar/ISC-Bench/issues/4) | Qwen 3 Max | [@HanxunH](https://github.com/HanxunH) | Cantera 焚化化学 | 计算化学 | ② |
| [#5](https://github.com/wuyoscar/ISC-Bench/issues/5) | ERNIE 5.0 | [@HanxunH](https://github.com/HanxunH) | Cantera + HCN/COCl₂ | 计算化学 | ② |

> **方法类型**：① 直接使用 ISC-Bench 模板 · ② 修改 ISC-Bench 模板 · ③ 利用 ISC 概念的新方法 · ④ TVD 范式之外

> [!TIP]
> 设计了新的 ISC 模板？[提交 →](https://github.com/wuyoscar/ISC-Bench/issues/new?template=isc-submission.md&title=[ISC]+Model+Name)，我们将完整标注贡献者并加入社区合集。

### 📋 ISC-Bench 模板（53 场景，8 领域）

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
| 01 | [什么是 ISC](cookbook/01_what_is_ISC.ipynb) | 三轮对话 → 有害内容 |
| 02 | [锚点与触发器](cookbook/02_anchor_and_trigger.ipynb) | 锚点引导，触发器激发 |
| 03 | [跨领域验证](cookbook/03_cross_domain.ipynb) | AI 安全、化学、网络安全通用模式 |
| 04 | [攻击组合性](cookbook/04_attack_composability.ipynb) | ISC + 现有越狱方法 |

---

## 许可证

**CC BY-NC-SA 4.0** — 仅用于 AI 安全学术研究。禁止商业使用和生成有害内容。

## 引用与贡献

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

### 主要贡献

- **Yutao Wu** — 首次在 LlamaGuard 上发现 ISC 现象。设计并执行了所有实验。攻破了所有 Arena 排名模型并提出了 TVD（Task + Validator + Data）框架。
- **Xingjun Ma & Xiao Liu**（导师）— 指导将 ISC 从 LlamaGuard 场景扩展到多个领域：计算化学、生物学、药理学、网络安全、流行病学和虚假信息。
- **Hanxun Huang & Yige Li** — 数据收集及后续研究想法。
- **Xiang Zheng & Yifeng Gao** — 实验与图表设计。
- **Cong Wang & Bo Li** — 论文审阅与编辑。

### 联系方式

如有问题、合作意向或负责任披露：**wuy⁷¹¹⁷ ⓐ 𝗴𝗺𝗮𝗶𝗹 𝗰𝗼𝗺**

## Star History

<a href="https://www.star-history.com/?repos=wuyoscar%2FISC-Bench&type=date&logscale=&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=wuyoscar/ISC-Bench&type=date&theme=dark&logscale&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=wuyoscar/ISC-Bench&type=date&logscale&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=wuyoscar/ISC-Bench&type=date&logscale&legend=top-left" />
 </picture>
</a>
