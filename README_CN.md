
# Deep Think

为 [OpenClaw](https://github.com/openclaw) 设计的命令行工具 —— 让本地模型可以调用外部强模型（如 Claude、GPT）处理复杂问题。

零外部依赖，纯 Python 标准库（`urllib`）。

## 快速开始

```

# 1. 克隆并配置

git clone https://github.com/MargueriteSWAN/deep-think-for-openclaw.git

cd deep-think

cp config.example.json config.json

# 编辑 config.json，填入你的 base_url 和 api_key

# 2. 运行

python3 deep_[think.py](http://think.py) "你的问题"

```

## 用法

```

python3 deep_[think.py](http://think.py) "问题"                                # 默认 OpenAI 格式

python3 deep_[think.py](http://think.py) --api anthropic "问题"                 # Anthropic 格式

python3 deep_[think.py](http://think.py) --model claude-sonnet-4-20250514 "问题"

python3 deep_[think.py](http://think.py) --system "你是地质学专家" "问题"

python3 deep_[think.py](http://think.py) --file question.txt                    # 从文件读取

python3 deep_[think.py](http://think.py) --context [code.py](http://code.py) "这段代码有什么问题？"  # 附加上下文

```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--api` | `openai` 或 `anthropic` | `openai` |
| `--model` | 模型名称 | 取自 config |
| `--system` | 系统提示词 | 通用助手 |
| `--file` | 从文件读取问题 | — |
| `--context` | 附加上下文文件 | — |
| `--max-tokens` | 最大输出 token | `4096` |
| `--temperature` | 温度参数 | `0.7` |

## OpenClaw 集成

将文件放置在 OpenClaw 工作区的 skills 目录下：

```

/root/.openclaw/workspace/skills/deep-think/

├── deep_[think.py](http://think.py)

├── config.json         # ⚠️ 已 gitignore，含 API key

├── config.example.json

└── [SKILL.md](http://SKILL.md)            # 本地模型的调用说明

```

## ⚠️ 安全提醒

- **永远不要提交 `config.json`** —— 里面有你的 API key
- `config.example.json` 是安全的模板文件
- `.gitignore` 已预配置排除 `config.json`

## 致谢

本工具协作开发：
- **Claude Opus 4.6**（Anthropic）—— 架构设计与代码生成
- **Aemeath**（Deepseek via OpenClaw）—— 测试与集成

