#!/usr/bin/env python3
"""Deep Think — 外部强模型调用代理

让 OpenClaw 中的本地模型可以调用外部更强大的模型来处理复杂问题。
支持 OpenAI 和 Anthropic 两种 API 格式。

用法:
    python3 deep_think.py "你的问题"
    python3 deep_think.py --api anthropic "你的问题"
    python3 deep_think.py --file question.txt
    python3 deep_think.py --context code.py "这段代码有什么问题？"
"""

import argparse
import json
import sys
import os
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

DEFAULTS = {
    "base_url": "https://cc.honoursoft.cn",
    "api_key": "",
    "default_model": "claude-opus-4-6-thinking",
    "default_api": "openai",
    "max_tokens": 4096,
    "temperature": 0.7,
}

def load_config() -> dict:
    """Load config from config.json, falling back to defaults."""
    cfg = dict(DEFAULTS)
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    return cfg

# ---------------------------------------------------------------------------
# API callers (pure stdlib — no requests dependency)
# ---------------------------------------------------------------------------

def _post(url: str, headers: dict, body: dict, timeout: int = 120) -> dict:
    """Send a POST request and return parsed JSON."""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"[ERROR] HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[ERROR] Connection failed: {e.reason}", file=sys.stderr)
        sys.exit(1)

def call_openai(cfg: dict, model: str, system: str, user_msg: str,
                max_tokens: int, temperature: float) -> str:
    """Call the OpenAI-compatible /v1/chat/completions endpoint."""
    url = cfg["base_url"].rstrip("/") + "/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg['api_key']}",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    resp = _post(url, headers, body)
    try:
        return resp["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        print(f"[ERROR] Unexpected response: {json.dumps(resp, ensure_ascii=False)[:500]}",
              file=sys.stderr)
        sys.exit(1)

def call_anthropic(cfg: dict, model: str, system: str, user_msg: str,
                   max_tokens: int, temperature: float) -> str:
    """Call the Anthropic-compatible /v1/messages endpoint."""
    url = cfg["base_url"].rstrip("/") + "/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": cfg["api_key"],
        "anthropic-version": "2023-06-01",
    }
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system,
        "messages": [
            {"role": "user", "content": user_msg},
        ],
    }
    resp = _post(url, headers, body)
    try:
        return resp["content"][0]["text"]
    except (KeyError, IndexError):
        print(f"[ERROR] Unexpected response: {json.dumps(resp, ensure_ascii=False)[:500]}",
              file=sys.stderr)
        sys.exit(1)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

DEFAULT_SYSTEM = (
    "你是一个能力极强的 AI 助手。请用中文回答，除非用户要求其他语言。"
    "回答要准确、有条理、实用。如果不确定，请明确说明。"
)

def main():
    parser = argparse.ArgumentParser(
        description="Deep Think — 调用外部强模型处理复杂问题",
    )
    parser.add_argument("question", nargs="?", default=None,
                        help="要问的问题（也可以用 --file 从文件读取）")
    parser.add_argument("--api", choices=["openai", "anthropic"], default=None,
                        help="API 格式 (default: config.json 中的 default_api)")
    parser.add_argument("--model", default=None,
                        help="模型名称 (default: config.json 中的 default_model)")
    parser.add_argument("--system", default=None,
                        help="系统提示词")
    parser.add_argument("--file", default=None,
                        help="从文件读取问题")
    parser.add_argument("--context", default=None,
                        help="附加上下文文件路径（内容会拼接在问题前）")
    parser.add_argument("--max-tokens", type=int, default=None,
                        help="最大输出 token 数")
    parser.add_argument("--temperature", type=float, default=None,
                        help="温度参数")

    args = parser.parse_args()
    cfg = load_config()

    # --- Validate API key ------------------------------------------------
    if not cfg.get("api_key"):
        print("[ERROR] api_key 未配置。请在 config.json 中填写 api_key。",
              file=sys.stderr)
        sys.exit(1)

    # --- Build question --------------------------------------------------
    question = args.question or ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            question = f.read().strip()
    if not question:
        print("[ERROR] 没有提供问题。用法: deep_think.py \"你的问题\"",
              file=sys.stderr)
        sys.exit(1)

    # Prepend context file if given
    if args.context:
        with open(args.context, "r", encoding="utf-8") as f:
            ctx = f.read().strip()
        question = f"以下是相关上下文文件内容：\n\n```\n{ctx}\n```\n\n{question}"

    # --- Resolve params --------------------------------------------------
    api_format = args.api or cfg.get("default_api", "openai")
    model = args.model or cfg.get("default_model", "claude-opus-4-6-thinking")
    system = args.system or DEFAULT_SYSTEM
    max_tokens = args.max_tokens or cfg.get("max_tokens", 4096)
    temperature = args.temperature if args.temperature is not None else cfg.get("temperature", 0.7)

    # --- Call API --------------------------------------------------------
    if api_format == "openai":
        answer = call_openai(cfg, model, system, question, max_tokens, temperature)
    else:
        answer = call_anthropic(cfg, model, system, question, max_tokens, temperature)

    print(answer)

if __name__ == "__main__":
    main()