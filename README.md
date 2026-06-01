# 🤖 AI Coding Agents — AutoGen + MCP + Tavily + Gemini

> **A hands-on Python playground for learning how to build, orchestrate, and extend AI coding agents using Microsoft AutoGen, Model Context Protocol (MCP), Tavily real-time web search, and Google Gemini.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://python.org)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.4%2B-orange)](https://microsoft.github.io/autogen/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-brightgreen?logo=google)](https://aistudio.google.com)
[![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-purple)](https://tavily.com)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 📌 About This Repository

This repo captures a **real learning journey** into AI agent development. Each Python file is a self-contained demo focused on one key concept — from a single streaming agent all the way to multi-agent teams, browser automation via MCP, real-time web search, image understanding, and stateful memory transfer between agents.

Every file is **heavily commented** to explain not just *what* the code does, but *why* — building the mental model needed to design and extend AI coding agents confidently.

---

## 🗂️ Project Structure

```
ai-coding-agents-autogen/
│
├── main.py                    # 🟢 START HERE — Single agent, streaming output
├── aiMCP_Demo.py              # 🌐 Agent controls a browser via Playwright MCP
├── aiMCP_filesystem_demo.py   # 📁 Agent reads local files via Filesystem MCP
├── multiagentdemo.py          # 👥 Multi-agent team (Marketing + Data Analyst)
├── multimodaldemo.py          # 🖼️  Agent analyses images (multimodal input)
├── state_preserve_demo.py     # 💾 Save & transfer agent memory between agents
├── tavillyWebSearchDemo.py    # 🔍 Real-time web search with Tavily (standalone)
├── tavilywithAgent.py         # 🔍🤖 Tavily wired into an agent as a tool
├── userproxydemo.py           # 🧑 Human-in-the-loop with UserProxyAgent
│
├── .env.example               # 🔑 Template for API keys (copy to .env)
├── requirements.txt           # 📦 Python dependencies
├── .gitignore                 # 🚫 Excludes secrets, venvs, caches
└── README.md                  # 📖 This file
```

---

## 🧠 Core Concepts Covered

| Demo File | Concept | Key Classes |
|-----------|---------|-------------|
| `main.py` | Single agent + streaming | `AssistantAgent`, `Console` |
| `aiMCP_Demo.py` | MCP + browser control | `McpWorkbench`, `StdioServerParams` |
| `aiMCP_filesystem_demo.py` | MCP + filesystem access | `McpWorkbench`, `StdioServerParams` |
| `multiagentdemo.py` | Multi-agent round robin | `RoundRobinGroupChat`, `MaxMessageTermination` |
| `multimodaldemo.py` | Multimodal (image) input | `MultiModalMessage`, `Image` |
| `state_preserve_demo.py` | State save / load / transfer | `save_state()`, `load_state()` |
| `tavillyWebSearchDemo.py` | Real-time web search | `TavilyClient` |
| `tavilywithAgent.py` | Tool-augmented agent | `tools=[]`, `TavilyClient` |
| `userproxydemo.py` | Human-in-the-loop | `UserProxyAgent`, `TextMentionTermination` |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/rutulraval/ai-coding-agents-autogen.git
cd ai-coding-agents-autogen
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up API keys

```bash
cp .env.example .env
# Edit .env and add your actual API keys
```

You'll need:
- **Gemini API Key** → [Google AI Studio](https://aistudio.google.com/app/apikey) (free tier available)
- **Tavily API Key** → [tavily.com](https://tavily.com) (free tier available)

### 5. Install Node.js (for MCP demos)

The MCP demos (`aiMCP_Demo.py`, `aiMCP_filesystem_demo.py`) require Node.js to run MCP servers:

- Download from [nodejs.org](https://nodejs.org)
- Verify: `node --version` and `npx --version`

### 6. Run your first demo

```bash
# Simplest demo — single agent with streaming
python main.py

# Multi-agent collaboration
python multiagentdemo.py

# Real-time web search
python tavilywithAgent.py
```

---

## 📦 Libraries & Frameworks Used

### 🔷 AutoGen (`autogen-agentchat`, `autogen-ext`, `autogen-core`)
Microsoft's open-source framework for building multi-agent AI systems. Provides:
- **`AssistantAgent`** — An LLM-powered agent that can reason, use tools, and stream responses
- **`UserProxyAgent`** — A human placeholder that accepts keyboard input during agent conversations
- **`RoundRobinGroupChat`** — Orchestrates multiple agents taking turns in a fixed order
- **`McpWorkbench`** — Connects agents to external tools via the Model Context Protocol (MCP)
- **`MultiModalMessage`** — Bundles text + images into a single agent message
- **`save_state()` / `load_state()`** — Serialises and restores agent conversation history

### 🔷 Model Context Protocol (MCP)
An open standard (by Anthropic) for connecting AI agents to external tools and data sources via a common protocol. Used here with:
- **`@playwright/mcp`** — Exposes Playwright browser automation as MCP tools
- **`@modelcontextprotocol/server-filesystem`** — Exposes a sandboxed local directory as MCP tools

### 🔷 Tavily
An AI-optimised web search API that returns clean, structured results designed for LLM consumption — not raw HTML. Ideal for giving agents access to real-time information.

### 🔷 Google Gemini (via OpenAI-compatible API)
`gemini-2.5-flash` is used as the underlying LLM for all agents. AutoGen's `OpenAIChatCompletionClient` works with any OpenAI-compatible endpoint, making it easy to swap to GPT-4, Claude, Ollama, or a local model.

### 🔷 python-dotenv
Loads environment variables (API keys) from a `.env` file, keeping secrets out of source code.

---

## 💡 Recommended Learning Order

If you're new to AI agents, work through the demos in this order:

```
1. main.py                   → Understand what an agent is
2. multiagentdemo.py         → See agents collaborate
3. userproxydemo.py          → Put yourself in the loop
4. tavillyWebSearchDemo.py   → Give agents real-time data
5. tavilywithAgent.py        → Wire tools into an agent
6. state_preserve_demo.py    → Persist & transfer memory
7. multimodaldemo.py         → Add image understanding
8. aiMCP_filesystem_demo.py  → Connect agents to your filesystem
9. aiMCP_Demo.py             → Control a browser with an agent
```

---

## 🔐 Security Best Practices

- ✅ Always store API keys in `.env` — never hardcode them in Python files
- ✅ Add `.env` to `.gitignore` (already done in this repo)
- ✅ Use `.env.example` as a template to share key names without values
- ✅ When using Filesystem MCP, only expose directories you're comfortable with
- ✅ Set termination conditions on all agent loops to prevent runaway execution

---

## 🛠️ Extending This Project

Ideas for building on top of these demos:

- 🧩 Add a **code execution tool** so agents can write and run Python
- 📧 Connect **Gmail MCP** to build an email-managing agent
- 🗃️ Use **SQLite or Postgres MCP** for database-querying agents
- 🧪 Build a **test-writing agent** that reads your codebase via Filesystem MCP
- 📊 Combine Tavily + multi-agent for an **automated research report** generator
- 🔄 Use `save_state()` to build **persistent AI assistants** across sessions

---

## 👤 Author

**Rutul Raval** · [github.com/rutulraval](https://github.com/rutulraval)

---

## 📄 License

MIT — feel free to use, modify, and share.
