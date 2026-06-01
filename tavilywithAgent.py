# ============================================================
# tavilywithAgent.py — AutoGen Agent with Tavily Web Search Tool
# ============================================================
#
# 🧠 CONCEPT: Tool-use (function calling) lets an AI agent
# decide WHEN and HOW to call external functions during a task.
# Here, the agent is given the web_search function as a tool.
# When the task requires live data, the agent calls the tool
# automatically and incorporates results into its answer.
#
# This is the core pattern behind "agentic" AI:
#   Reason → Act (call tool) → Observe (get result) → Reason again
#
# 📦 LIBRARIES USED:
#   - autogen_agentchat.agents  : AssistantAgent (with tools=[...])
#   - autogen_agentchat.ui      : Console
#   - autogen_ext.models.openai : LLM client
#   - tavily-python             : Web search API
#   - python-dotenv             : .env loader
#
# 💡 AI AGENT MINDSET:
#   The tools=[ ] parameter accepts a list of Python async
#   functions. AutoGen automatically generates a JSON schema for
#   each function (based on type hints and docstrings) and
#   registers it with the LLM. The LLM then decides when to
#   call each tool — you don't hardcode the logic.
#
# 🔁 TOOL CALL FLOW:
#   User Task → Agent reasoning → "I need web search"
#       → calls web_search(query) → Tavily returns results
#       → Agent reads results → Produces final answer
#
# ⚠️  NOTE: web_search below is defined as async but TavilyClient
#   is synchronous. For production use, wrap blocking calls with
#   asyncio.to_thread() to avoid blocking the event loop.
# ============================================================

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables (TAVILY_API_KEY, OPENAI_API_KEY)
load_dotenv()


async def web_search(query: str) -> dict:
    """
    Search the web for real-time information using Tavily.

    Args:
        query: The search query string to look up.

    Returns:
        A dictionary containing search results with titles,
        URLs, content snippets, and relevance scores.
    """
    # TavilyClient reads TAVILY_API_KEY from environment automatically
    tavily_client = TavilyClient()
    search_results = tavily_client.search(query)
    print(search_results)  # Debug: shows raw results in terminal
    return search_results


async def main():
    # ----------------------------------------------------------
    # Step 1: Create the LLM client
    # ----------------------------------------------------------
    model_client = OpenAIChatCompletionClient(model="gemini-2.5-flash")

    # ----------------------------------------------------------
    # Step 2: Create an agent with web_search as a registered tool
    # The agent will invoke web_search when it determines the
    # task requires live information from the internet.
    # ----------------------------------------------------------
    personal_agent = AssistantAgent(
        name="search_agent",
        model_client=model_client,
        tools=[web_search]   # 🔧 Register Python functions as callable tools
    )

    # ----------------------------------------------------------
    # Step 3: Ask a question that requires real-time data
    # The agent will recognise it needs current sports data and
    # automatically call web_search with an appropriate query.
    # ----------------------------------------------------------
    await Console(
        personal_agent.run_stream(task="Who won 2026 T20?")
    )


asyncio.run(main())
