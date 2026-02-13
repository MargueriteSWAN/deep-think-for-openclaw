# Deep Think — 外部强模型调用工具

# SKILL.md — Deep Think（外部强模型代理）

## 这是什么？

`deep_think.py` 是一个命令行工具，让你可以把**超出你能力范围的复杂问题**转发给一个更强大的外部模型，获取高质量回答后再整合给用户。

你可以把它理解为：**你的「顾问热线」**。你自己处理不了的难题，打个电话问问大佬，再把答案翻译给用户。

---

## 什么时候该用？

### ✅ 应该用 Deep Think 的场景

- **复杂代码问题**：涉及多文件架构设计、难以调试的 bug、你不熟悉的语言/框架
- **学术深度分析**：论文方法论评审、复杂地质学概念推理、统计方法选择
- **长文本处理**：论文润色、长篇翻译、复杂文档总结
- **需要精确推理**：数学证明、逻辑链较长的问题、多步骤规划
- **你不确定自己答案的时候**：如果你想说"我不确定"，先试试问 Deep Think

### ❌ 不要用 Deep Think 的场景

- 简单的文件操作、系统命令
- 闲聊、日常对话
- 你已经知道答案的问题
- 频率过高（每天不超过 20 次，避免 token 浪费）

---

## 怎么用？

### 基本用法

```bash
# OpenAI 格式（默认）
python3 /root/.openclaw/workspace/skills/deep-think/deep_think.py "你的问题"

# Anthropic 格式
python3 /root/.openclaw/workspace/skills/deep-think/deep_think.py --api anthropic "你的问题"

# 指定模型
python3 /root/.openclaw/workspace/skills/deep-think/deep_think.py --model claude-sonnet-4-20250514 "你的问题"

# 带系统提示
python3 /root/.openclaw/workspace/skills/deep-think/deep_think.py --system "你是一个地质学专家" "分析这个碎屑锆石U-Pb数据的物源意义"

# 从文件读取问题（适合长文本）
python3 /root/.openclaw/workspace/skills/deep-think/deep_think.py --file /path/to/question.txt

# 带上下文文件
python3 /root/.openclaw/workspace/skills/deep-think/deep_think.py --context /path/to/code.py "这段代码有什么bug？"
```

### 参数说明

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `--api` | API 格式：`openai` 或 `anthropic` | `openai` |
| `--model` | 模型名称 | `claude-opus-4-6-thinking` |
| `--system` | 系统提示词 | 通用助手提示 |
| `--file` | 从文件读取问题 | - |
| `--context` | 附加上下文文件 | - |
| `--max-tokens` | 最大输出 token 数 | `4096` |
| `--temperature` | 温度参数 | `0.7` |

---

## 安装位置

```
/root/.openclaw/workspace/skills/deep-think/
├── SKILL.md          ← 你正在读的这个文件
├── deep_think.py     ← 主脚本
└── config.json       ← 配置文件（API key 在这里）
```

---


## 使用原则

1. **先自己想，再问大佬** — 不要什么都丢给 Deep Think
2. **整合而非转发** — 拿到回答后，用你自己的风格整合给用户，不要直接复制粘贴
3. **标注来源** — 告诉用户"我问了更强的模型确认了一下"，保持透明
4. **控制频率** — 每天不超过 20 次调用
5. **不要修改脚本和配置** — 除非用户明确要求

---

## 示例工作流

**苏婉问**："帮我看看这段 R 代码为什么 MDS 结果不对"

**爱弥斯的做法**：

1. 先自己看代码，尝试找问题
2. 如果找不到 → 把代码和错误信息发给 Deep Think：

```bash
python3 /root/.openclaw/workspace/skills/deep-think/deep_think.py \
  --system "你是一个精通R语言和地质学统计方法的专家" \
  --context /path/to/mds_code.R \
  "这段MDS代码输出结果异常，stress值过高，请分析可能的原因和修复方案"
```

1. 拿到回答后，用自己的话整合给用户
2. 告诉用户："我请教了一下更强的模型确认了，问题出在..."

---

# 部署步骤

```bash
# 1. 创建目录
mkdir -p /root/.openclaw/workspace/skills/deep-think

# 2. 将上面的 deep_think.py 保存到该目录
# 3. 将上面的 config.json 保存到该目录
# 4. 将上面的 SKILL.md 内容保存到该目录

# 5. 给脚本执行权限
chmod +x /root/.openclaw/workspace/skills/deep-think/deep_think.py

# 6. 测试（填好 api_key 后）
python3 /root/.openclaw/workspace/skills/deep-think/deep_think.py "你好，测试连接"
```

脚本**零外部依赖**，只用 Python 标准库（`urllib`），不需要安装任何 pip 包，不会碰 OpenClaw 的任何配置。

## Acknowledgments

This tool was co-created with the assistance of:
- **Claude Opus 4.6** (Anthropic) — architecture design, code generation, and documentation
- **Aemeath** (DeepSeek-chat via OpenClaw) — testing and integration

The author is responsible for all design decisions and final implementation.