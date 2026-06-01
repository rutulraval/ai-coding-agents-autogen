# ============================================================
# main.py — Single Agent with Streaming (AutoGen + Gemini)
# ============================================================
#
# 🧠 CONCEPT: The simplest building block of an AI coding agent.
# An AssistantAgent wraps an LLM (here: Gemini 2.5 Flash via
# the OpenAI-compatible API) and can answer questions, run tasks,
# and stream responses token-by-token to the console.
#
# 📦 LIBRARIES USED:
#   - autogen-agentchat : High-level agent orchestration framework
#   - autogen-ext[openai]: OpenAI-compatible model client (works
#                          with Gemini, Azure, local models, etc.)
#
# 🔧 INSTALL:
#   pip install -U "autogen-agentchat" "autogen-ext[openai]"
#
# 💡 AI AGENT MINDSET:
#   Think of AssistantAgent as your "worker" — you give it:
#     1. A name          → identity in multi-agent setups
#     2. A model client  → the brain (LLM) it uses
#     3. A system prompt → its personality / role
#   Then you run a task and it does the thinking for you.
# ============================================================

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main() -> None:
    # ----------------------------------------------------------
    # Step 1: Create the model client
    # OpenAIChatCompletionClient supports any OpenAI-compatible
    # endpoint — here we point it to Gemini 2.5 Flash.
    # In production: load api_key from os.environ or python-dotenv
    # ----------------------------------------------------------
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        api_key="YOUR_GEMINI_API_KEY"  # 🔑 Move to .env in production
    )

    # ----------------------------------------------------------
    # Step 2: Create an AssistantAgent
    #   - reflect_on_tool_use=True  → agent reviews tool output
    #                                  before giving final answer
    #   - model_client_stream=True  → enables token streaming
    #   - system_message            → sets the agent's behaviour
    # ----------------------------------------------------------
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        reflect_on_tool_use=True,
        model_client_stream=True,
        system_message="You are a helpful assistant"
    )

    # ----------------------------------------------------------
    # Step 3: Run the agent with a task
    # Console() streams the output live to your terminal.
    # run_stream() yields chunks as the model generates them.
    # ----------------------------------------------------------
    await Console(
        agent.run_stream(task="What is today's date in the UK and Australia?")
    )

    # ----------------------------------------------------------
    # Step 4: Always close the agent to release resources
    # ----------------------------------------------------------
    await agent.close()


# Entry point — asyncio.run() starts the async event loop
asyncio.run(main())
