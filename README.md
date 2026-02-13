```markdown
# Deep Think

An external strong-model proxy for [OpenClaw](https://github.com/recursal/OpenClaw). Lets your local model call a more capable API (OpenAI / Anthropic compatible) to handle complex tasks.

Zero dependencies — pure Python stdlib.

## Quick Start

```

# 1. Clone & configure

git clone https://github.com/MargueriteSWAN/deep-think.git

cd deep-think

cp config.example.json config.json

# Edit config.json — fill in your base_url and api_key

# 2. Run

python3 deep_[think.py](http://think.py) "Your question here"

```

## Usage

```

# Default (OpenAI-compatible endpoint)

python3 deep_[think.py](http://think.py) "Your question"

# Anthropic endpoint

python3 deep_[think.py](http://think.py) --api anthropic "Your question"

# Custom model

python3 deep_[think.py](http://think.py) --model claude-sonnet-4-20250514 "Your question"

# With system prompt

python3 deep_[think.py](http://think.py) --system "You are a geology expert" "Analyze this data"

# Read question from file

python3 deep_[think.py](http://think.py) --file question.txt

# Attach context file

python3 deep_[think.py](http://think.py) --context [code.py](http://code.py) "What's wrong with this code?"

```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--api` | `openai` or `anthropic` | `openai` |
| `--model` | Model name | from config |
| `--system` | System prompt | generic assistant |
| `--file` | Read question from file | — |
| `--context` | Prepend file content as context | — |
| `--max-tokens` | Max output tokens | `4096` |
| `--temperature` | Sampling temperature | `0.7` |

## Configuration

Copy the example and fill in your values:

```

cp config.example.json config.json

```

```

{

"base_url": "https://your-api-proxy.example.com",

"api_key": "sk-your-key-here",

"default_model": "claude-opus-4-6-thinking",

"default_api": "openai",

"max_tokens": 4096,

"temperature": 0.7

}

```

> ⚠️ **Never commit `config.json`** — it contains your API key. It is already in `.gitignore`.

## For OpenClaw Agents

Place the script in your workspace skills directory:

```

/root/.openclaw/workspace/skills/deep-think/

├── deep_[think.py](http://think.py)

├── config.json       ← your private config (git-ignored)

├── config.example.json

└── [SKILL.md](http://SKILL.md)          ← agent-facing instructions

```

See `SKILL.md` for guidance on when and how your agent should invoke this tool.

## Acknowledgments

Co-created with assistance from:
- **Claude Opus 4.6** (Anthropic) — architecture design, code generation, and documentation
- **Aemeath** (DeepSeek-chat via OpenClaw) — testing and integration

The author is responsible for all design decisions and final implementation.

## License

MIT
```

---
