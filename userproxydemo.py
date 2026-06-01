# ============================================================
# userproxydemo.py — Human-in-the-Loop with UserProxyAgent
# ============================================================
#
# 🧠 CONCEPT: UserProxyAgent represents a human participant
# inside an AutoGen multi-agent conversation. It allows a real
# person to inject messages into the chat at any point,
# enabling "human-in-the-loop" workflows where:
#   - A human reviews and approves agent actions
#   - A human student interacts with a teaching agent
#   - A human tester provides feedback during agent execution
#
# Here we simulate a teacher-student conversation where a Java
# expert agent gives a lecture and the student (UserProxy) can
# respond — the conversation ends when "understood" is typed.
#
# 📦 LIBRARIES USED:
#   - autogen_agentchat.agents     : AssistantAgent, UserProxyAgent
#   - autogen_agentchat.conditions : TextMentionTermination
#   - autogen_agentchat.teams      : RoundRobinGroupChat
#   - autogen_agentchat.ui         : Console
#   - autogen_ext.models.openai    : LLM client
#
# 💡 AI AGENT MINDSET:
#   UserProxyAgent does NOT call an LLM — it waits for human
#   keyboard input at each of its turns. This is what makes it
#   a "proxy" for a real human in the agent loop.
#
# 🔁 TERMINATION CONDITION:
#   TextMentionTermination("understood") stops the loop the
#   moment any message contains the word "understood".
#   → The student types "understood" to end the lecture.
#
# 🏗️ FLOW:
#   Task → java_expert responds → UserProxy (you) types reply
#        → java_expert responds → ... → "understood" → STOP
#
# 🔒 SAFETY TIP:
#   Always set a termination condition. Without one, human-in-
#   the-loop agents can run indefinitely waiting for input.
# ============================================================

import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# ⚠️  Use python-dotenv in production instead of hardcoding keys
os.environ['OPENAI_API_KEY'] = 'YOUR_GEMINI_API_KEY'


async def main():
    # ----------------------------------------------------------
    # Step 1: Create the shared model client
    # ----------------------------------------------------------
    model_client = OpenAIChatCompletionClient(model="gemini-2.5-flash")

    # ----------------------------------------------------------
    # Step 2: Create the AI teaching agent
    # This agent has deep Java knowledge and explains concepts
    # in a lecture/tutorial style.
    # ----------------------------------------------------------
    java_expert_agent = AssistantAgent(
        name="java_expert",
        model_client=model_client,
        system_message="You are a Java expert with 30 years of experience in Java development."
    )

    # ----------------------------------------------------------
    # Step 3: Create the UserProxyAgent
    # This is the human participant placeholder.
    # When it's the UserProxy's turn, the console will prompt
    # you to type a message.
    # description= helps other agents understand who this is.
    # ----------------------------------------------------------
    student = UserProxyAgent(
        name="java_student",
        description="You are a learner of Java"
    )

    # ----------------------------------------------------------
    # Step 4: Set up the team with a keyword-based stop condition
    # The conversation ends when any message contains "understood".
    # ----------------------------------------------------------
    team = RoundRobinGroupChat(
        participants=[java_expert_agent, student],
        termination_condition=TextMentionTermination("understood")
    )

    # ----------------------------------------------------------
    # Step 5: Start the interactive lecture
    # The java_expert will begin, then the terminal will prompt
    # you (the human) to respond as the student.
    # Type "understood" at any point to end the session.
    # ----------------------------------------------------------
    await Console(
        team.run_stream(task="Simulate a small snippet-type lecture for OOPs in Java")
    )

    await model_client.close()


asyncio.run(main())
