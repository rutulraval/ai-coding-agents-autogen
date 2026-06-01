# ============================================================
# aiMCP_Demo.py — AI Agent + MCP (Playwright Browser Control)
# ============================================================
#
# 🧠 CONCEPT: MCP (Model Context Protocol) is a standard that
# lets AI agents connect to external tools and services via a
# defined protocol. Instead of hardcoding tools, the agent
# discovers and uses tools exposed by an MCP server at runtime.
#
# Here, we connect an AI agent to Playwright via its MCP server,
# allowing the agent to control a real browser — navigate pages,
# click buttons, fill forms — just by receiving natural language
# instructions.
#
# 📦 LIBRARIES USED:
#   - autogen-agentchat          : Agent orchestration
#   - autogen-ext[openai]        : LLM client (Gemini)
#   - autogen_ext.tools.mcp      : MCP tool integration layer
#   - @playwright/mcp (npm)      : Playwright MCP server (Node.js)
#   - python-dotenv              : Loads secrets from .env file
#
# 🔧 INSTALL:
#   pip install autogen-agentchat autogen-ext[openai] python-dotenv
#   npm install -g @playwright/mcp   (requires Node.js)
#
# 💡 AI AGENT MINDSET:
#   MCP turns your agent into a "browser operator".
#   The agent receives a task in plain English and figures out
#   which browser actions (navigate, click, scroll) to call.
#   max_tool_iterations limits how many tool calls per turn,
#   preventing infinite loops.
#
# 🏗️ ARCHITECTURE:
#   User Task → AssistantAgent → McpWorkbench → Playwright MCP
#                                                    ↓
#                                             Real Browser
# ============================================================

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from dotenv import load_dotenv

# Load API keys from .env file (OPENAI_API_KEY, TAVILY_API_KEY, etc.)
load_dotenv()


async def main():
    # ----------------------------------------------------------
    # Step 1: Set up the LLM client
    # API key is picked up automatically from the environment
    # variable OPENAI_API_KEY (loaded via load_dotenv above).
    # ----------------------------------------------------------
    model_client = OpenAIChatCompletionClient(model="gemini-2.5-flash")

    # ----------------------------------------------------------
    # Step 2: Define MCP Server Parameters
    # StdioServerParams launches the MCP server as a child process
    # communicating over stdin/stdout.
    #   - command : the executable to run (npx)
    #   - args    : launches the Playwright MCP server in headless mode
    # ----------------------------------------------------------
    server_params = StdioServerParams(
        command="npx",
        args=["@playwright/mcp@latest", "--headless"],
    )

    # ----------------------------------------------------------
    # Step 3: Create the McpWorkbench
    # The workbench manages the lifecycle of the MCP server and
    # exposes its tools to the agent as callable functions.
    # ----------------------------------------------------------
    playwright_workbench = McpWorkbench(server_params)

    # ----------------------------------------------------------
    # Step 4: Create an agent wired to the MCP workbench
    #   - workbench=playwright_workbench → gives the agent browser tools
    #   - max_tool_iterations=3          → limit calls per agent turn
    # ----------------------------------------------------------
    agent_with_mcp = AssistantAgent(
        name="agent_with_mcp",
        model_client=model_client,
        workbench=playwright_workbench,
        model_client_stream=True,
        max_tool_iterations=3
    )

    # ----------------------------------------------------------
    # Step 5: Give the agent a natural language browser task
    # The agent will decide which Playwright MCP tools to call
    # (e.g., browser_navigate, browser_snapshot) on its own.
    # ----------------------------------------------------------
    await Console(
        agent_with_mcp.run_stream(task="Launch BBC.com")
    )


asyncio.run(main())
