


# Deep Think

A CLI tool for [OpenClaw](https://github.com/openclaw) that lets your local model call a stronger external model (e.g. Claude, GPT) via API proxy to handle complex tasks.

Zero dependencies — pure Python stdlib (`urllib`).

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

python3 deep_[think.py](http://think.py) "question"                          # default (OpenAI format)

python3 deep_[think.py](http://think.py) --api anthropic "question"           # Anthropic format

python3 deep_[think.py](http://think.py) --model claude-sonnet-4-20250514 "question"

python3 deep_[think.py](http://think.py) --system "You are an expert" "question"

python3 deep_[think.py](http://think.py) --file question.txt                  # read from file

python3 deep_[think.py](http://think.py) --context [code.py](http://code.py) "What's wrong?"    # attach context

```

| Flag | Description | Default |
|------|-------------|---------|
| `--api` | `openai` or `anthropic` | `openai` |
| `--model` | Model name | from config |
| `--system` | System prompt | generic assistant |
| `--file` | Read question from file | — |
| `--context` | Attach a context file | — |
| `--max-tokens` | Max output tokens | `4096` |
| `--temperature` | Sampling temperature | `0.7` |

## OpenClaw Integration

Place the files under your OpenClaw workspace skills directory:

```

/root/.openclaw/workspace/skills/deep-think/

├── deep_[think.py](http://think.py)

├── config.json       # ⚠️ gitignored — contains your API key

├── config.example.json

└── [SKILL.md](http://SKILL.md)          # instructions for the local model

```

## ⚠️ Security

- **Never commit `config.json`** — it contains your API key.
- `config.example.json` is the safe template.
- `.gitignore` is pre-configured to exclude `config.json`.

## Acknowledgments

Co-created with:
- **Claude Opus 4.6** (Anthropic) — architecture design & code generation
- **Aemeath** (Deepseek via OpenClaw) — testing & integration

