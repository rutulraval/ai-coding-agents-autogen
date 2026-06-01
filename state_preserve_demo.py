# ============================================================
# state_preserve_demo.py — Agent State Save & Load (Memory Transfer)
# ============================================================
#
# 🧠 CONCEPT: AI agents are stateless by default — each new run
# starts fresh with no memory of previous conversations. This
# demo shows how to:
#   1. Save an agent's conversation state to a file (JSON)
#   2. Load that state into a DIFFERENT agent
#
# This unlocks powerful patterns:
#   - Persist agent memory across application restarts
#   - Hand off context from one specialist agent to another
#   - Build "briefing" workflows where Agent B picks up where A left off
#   - Store conversation snapshots for debugging or auditing
#
# 📦 LIBRARIES USED:
#   - autogen_agentchat.agents  : AssistantAgent (save_state / load_state)
#   - autogen_agentchat.ui      : Console
#   - autogen_ext.models.openai : LLM client
#   - json                      : Serialize/deserialize state to file
#   - os                        : Environment variable management
#
# 💡 AI AGENT MINDSET:
#   save_state() snapshots the full message history of an agent.
#   load_state() injects that history into another agent so it
#   has full context of the previous conversation — as if it had
#   been in the room the whole time.
#
# 🏗️ WORKFLOW:
#   marketing_agent runs task → save_state() → write to file
#   read file → data_analyst_agent.load_state() → ask follow-up
# ============================================================

import asyncio
import json
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# ⚠️  In production, use python-dotenv and a .env file
os.environ['OPENAI_API_KEY'] = 'YOUR_GEMINI_API_KEY'

# Path for saving/loading agent state
STATE_FILE = "marketingcontext.txt"  # 💾 Stores serialised agent conversation


async def main():
    # ----------------------------------------------------------
    # Step 1: Shared model client for both agents
    # ----------------------------------------------------------
    model_client = OpenAIChatCompletionClient(model="gemini-2.5-flash")

    # ----------------------------------------------------------
    # Step 2: Create the first agent (marketing expert)
    # and run it on a task to generate a conversation history
    # ----------------------------------------------------------
    marketing_agent = AssistantAgent(
        name="marketing_person",
        model_client=model_client,
        system_message="You are a marketing expert with 30 years of experience in marketing in the AI industry."
    )

    await Console(
        marketing_agent.run_stream(
            task="How are different festivals marketed in the UK for Indian and Pakistani origin people?"
        )
    )

    # ----------------------------------------------------------
    # Step 3: Save the agent's state (full message history)
    # save_state() returns a dict that can be JSON-serialised.
    # ----------------------------------------------------------
    agent_state = await marketing_agent.save_state()

    with open(STATE_FILE, "w") as f:
        json.dump(agent_state, f)
    print(f"\n💾 State saved to '{STATE_FILE}'")

    # ----------------------------------------------------------
    # Step 4: Load the saved state back from file
    # ----------------------------------------------------------
    with open(STATE_FILE, "r") as f:
        saved_state = json.load(f)

    # ----------------------------------------------------------
    # Step 5: Create a DIFFERENT agent (data analyst)
    # and inject the marketing agent's conversation history.
    # The data analyst now "knows" everything discussed previously.
    # ----------------------------------------------------------
    data_analyst_agent = AssistantAgent(
        name="data_analyst",
        model_client=model_client,
        system_message="You are a data analyst with 20 years of experience in data analysis in the AI industry."
    )

    await data_analyst_agent.load_state(saved_state)
    print("📂 State loaded into data_analyst_agent\n")

    # ----------------------------------------------------------
    # Step 6: The data analyst can now reference the marketing
    # agent's previous conversation as if it was present
    # ----------------------------------------------------------
    await Console(
        data_analyst_agent.run_stream(
            task="What is the marketing agent discussing about?"
        )
    )

    await model_client.close()


asyncio.run(main())
