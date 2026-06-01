# ============================================================
# multimodaldemo.py — Multimodal AI Agent (Image Understanding)
# ============================================================
#
# 🧠 CONCEPT: Multimodal agents can process both text AND images
# (and in advanced setups: audio, video, documents). This demo
# shows how to pass an image file to an AutoGen agent and ask
# it a question about the visual content.
#
# This is the foundation for building agents that can:
#   - Analyse screenshots and UI mockups
#   - Inspect charts and data visualisations
#   - Describe product photos for e-commerce
#   - Review medical or technical images
#   - Read handwritten notes or whiteboard diagrams
#
# 📦 LIBRARIES USED:
#   - autogen_agentchat.agents   : AssistantAgent
#   - autogen_agentchat.messages : MultiModalMessage (text + image)
#   - autogen_agentchat.ui       : Console
#   - autogen_core               : Image (helper to load image files)
#   - autogen_ext.models.openai  : OpenAI-compatible LLM client
#
# 🔧 INSTALL:
#   pip install autogen-agentchat autogen-ext[openai] autogen-core
#
# 💡 AI AGENT MINDSET:
#   MultiModalMessage bundles multiple content types into a single
#   message. The list can contain any mix of strings (text) and
#   Image objects. The LLM receives all of it together and
#   responds with awareness of both the text question and the image.
#
# 🖼️  IMAGE FORMATS SUPPORTED:
#   JPEG, PNG, GIF, WebP — via autogen_core.Image.from_file()
#   You can also load from URL: Image.from_uri("https://...")
# ============================================================

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def analyzeImage():
    # ----------------------------------------------------------
    # Step 1: Create a multimodal-capable model client
    # Gemini 2.5 Flash natively supports vision (image input).
    # ----------------------------------------------------------
    model_client = OpenAIChatCompletionClient(
        name="ImageAnalyzerAgent",
        model="gemini-2.5-flash",
        api_key="YOUR_GEMINI_API_KEY",  # 🔑 Use .env in production
        reflect_on_tool_use=True,
        model_client_stream=True,
        system_message="You are a helpful assistant"
    )

    # ----------------------------------------------------------
    # Step 2: Create the assistant agent
    # ----------------------------------------------------------
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client
    )

    # ----------------------------------------------------------
    # Step 3: Load an image from disk
    # Image.from_file() reads the file and encodes it for the API.
    # Update this path to point to any image on your machine.
    # ----------------------------------------------------------
    img = Image.from_file("C:\\path\\to\\your\\image.jpeg")  # 📸 Update path

    # ----------------------------------------------------------
    # Step 4: Create a MultiModalMessage
    # The content list can contain strings and Image objects
    # in any order. Here: [question_text, image]
    # source="user" marks this as coming from the human side.
    # ----------------------------------------------------------
    mm_message = MultiModalMessage(
        content=["What do you see in this image?", img],
        source="user"
    )

    # ----------------------------------------------------------
    # Step 5: Run the agent with the multimodal message as the task
    # ----------------------------------------------------------
    await Console(
        agent.run_stream(task=mm_message)
    )

    # Clean up resources
    await agent.close()


asyncio.run(analyzeImage())
