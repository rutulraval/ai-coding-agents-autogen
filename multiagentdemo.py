# ============================================================
# multiagentdemo.py — Multi-Agent Team with Round Robin Chat
# ============================================================
#
# 🧠 CONCEPT: Multi-agent systems let you decompose complex
# problems by assigning specialist roles to different agents.
# Each agent has its own system prompt (persona/expertise) and
# they collaborate in turns to produce a richer, more nuanced
# answer than a single agent could.
#
# Pattern used: RoundRobinGroupChat
#   → Agents take turns speaking in a fixed circular order.
#   → Great for structured debates, collaborative analysis,
#     and iterative refinement of ideas.
#
# 📦 LIBRARIES USED:
#   - autogen_agentchat.agents     : AssistantAgent
#   - autogen_agentchat.conditions : MaxMessageTermination
#   - autogen_agentchat.teams      : RoundRobinGroupChat
#   - autogen_agentchat.ui         : Console (streaming output)
#   - autogen_ext.models.openai    : OpenAI-compatible LLM client
#
# 💡 AI AGENT MINDSET:
#   Think of this as a "boardroom simulation".
#   Each agent brings a unique lens to the problem:
#     - marketing_agent → brand, perception, customer strategy
#     - data_analyst    → numbers, trends, evidence-based reasoning
#   The team chat produces a conversation you can read like
#   meeting minutes — with diverse expert opinions.
#
# 🔁 TERMINATION CONDITIONS:
#   MaxMessageTermination(max_messages=3) stops the chat after
#   3 total messages across all agents. This prevents runaway
#   loops. Other options include TextMentionTermination (stop
#   when an agent says a keyword like "DONE").
#
# 🏗️ ARCHITECTURE:
#   Task → RoundRobinGroupChat
#               ├── marketing_agent (turn 1)
#               ├── data_analyst    (turn 2)
#               └── [STOP at max_messages=3]
# ============================================================

import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Set API key via environment variable
# ⚠️  In production: use a .env file + dotenv, never hardcode keys
os.environ['OPENAI_API_KEY'] = 'YOUR_GEMINI_API_KEY'


async def main():
    # ----------------------------------------------------------
    # Step 1: Shared model client
    # Both agents use the same underlying LLM — but their
    # system_message gives them completely different personalities.
    # ----------------------------------------------------------
    model_client = OpenAIChatCompletionClient(model="gemini-2.5-flash")

    # ----------------------------------------------------------
    # Step 2: Define specialist agents
    # The system_message is the key — it defines the agent's
    # expertise, communication style, and perspective.
    # ----------------------------------------------------------
    marketing_agent = AssistantAgent(
        name="marketing_person",
        model_client=model_client,
        system_message="You are a marketing expert with 30 years of experience in marketing in the AI industry."
    )

    data_analyst_agent = AssistantAgent(
        name="data_analyst",
        model_client=model_client,
        system_message="You are a data analyst with 20 years of experience in data analysis in the AI industry."
    )

    # ----------------------------------------------------------
    # Step 3: Form the team with a termination condition
    # RoundRobinGroupChat cycles through participants in order.
    # MaxMessageTermination stops after N total messages.
    # ----------------------------------------------------------
    team = RoundRobinGroupChat(
        participants=[marketing_agent, data_analyst_agent],
        termination_condition=MaxMessageTermination(max_messages=3)
    )

    # ----------------------------------------------------------
    # Step 4: Run the team on a business problem
    # Both agents will weigh in from their own perspective.
    # ----------------------------------------------------------
    await Console(
        team.run_stream(
            task="What is the best way to tackle a sinking share price of our company and to improve it?"
        )
    )

    # Release model client resources
    await model_client.close()


asyncio.run(main())
