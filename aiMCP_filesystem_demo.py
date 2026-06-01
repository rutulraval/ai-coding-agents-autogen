# ============================================================
# aiMCP_filesystem_demo.py — AI Agent + MCP Filesystem Server
# ============================================================
#
# 🧠 CONCEPT: The MCP Filesystem server exposes a controlled
# directory of your local machine to the AI agent. The agent
# can list files, read content, and navigate folders — all
# through natural language — without you writing a single
# file-reading function.
#
# This is powerful for building AI assistants that can:
#   - Summarise documents in a folder
#   - Search across files for information
#   - Audit project structures
#   - Prepare context from local codebases
#
# 📦 LIBRARIES USED:
#   - autogen-agentchat                      : Agent orchestration
#   - autogen-ext[openai]                    : LLM client (Gemini)
#   - autogen_ext.tools.mcp                  : MCP integration layer
#   - @modelcontextprotocol/server-filesystem: Official MCP FS server
#   - python-dotenv                          : .env loader
#
# 🔧 INSTALL:
#   pip install autogen-agentchat autogen-ext[openai] python-dotenv
#   npx -y @modelcontextprotocol/server-filesystem <allowed-path>
#
# 💡 AI AGENT MINDSET:
#   You define a "sandbox" directory that the agent is allowed to
#   access. It cannot go outside that path — a safe, auditable
#   boundary. The agent then navigates it using MCP tool calls.
#
# ⚠️  SECURITY NOTE:
#   Only expose directories you're comfortable sharing with the
#   agent. Never point this at sensitive system directories.
# ============================================================

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from dotenv import load_dotenv

# Load environment variables (API keys) from .env
load_dotenv()


async def main():
    # ----------------------------------------------------------
    # Step 1: Create the LLM model client
    # ----------------------------------------------------------
    model_client = OpenAIChatCompletionClient(model="gemini-2.5-flash")

    # ----------------------------------------------------------
    # Step 2: Configure the Filesystem MCP Server
    # The "-y" flag auto-confirms the npx package install.
    # The path at the end is the ONLY directory the agent can see.
    # Change this path to point to the folder you want the agent
    # to have access to on your machine.
    # ----------------------------------------------------------
    server_params = StdioServerParams(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "C:/path/to/your/allowed/directory"  # 📁 Update this path
        ]
    )

    # ----------------------------------------------------------
    # Step 3: Wrap the MCP server in a workbench
    # ----------------------------------------------------------
    filesystem_workbench = McpWorkbench(server_params)

    # ----------------------------------------------------------
    # Step 4: Create the agent with filesystem access
    # model_client_stream=False → collect full response before printing
    # ----------------------------------------------------------
    agent_with_filesystem_mcp = AssistantAgent(
        name="agent_with_filesystem_mcp",
        model_client=model_client,
        workbench=filesystem_workbench,
        model_client_stream=False,
        max_tool_iterations=3
    )

    # ----------------------------------------------------------
    # Step 5: Ask the agent to explore the filesystem
    # The agent will use MCP tools like list_directory and
    # read_file to answer the question.
    # ----------------------------------------------------------
    await Console(
        agent_with_filesystem_mcp.run_stream(
            task="List all files and folders in the allowed directory and inside backend folder"
        )
    )

    # Clean up the model client connection
    await model_client.close()


asyncio.run(main())
