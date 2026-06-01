# ============================================================
# tavillyWebSearchDemo.py — Real-Time Web Search with Tavily
# ============================================================
#
# 🧠 CONCEPT: AI models have a knowledge cutoff — they don't
# know what happened after their training ended. Tavily is an
# AI-optimised search API that lets your agents fetch real-time
# information from the web and incorporate it into responses.
#
# This demo shows standalone Tavily usage (no agent wrapper).
# It's the foundation for tool-augmented agents that need
# live data: news, stock prices, sports results, weather, etc.
#
# 📦 LIBRARIES USED:
#   - tavily-python : Official Tavily Python SDK
#                    (pip install tavily-python)
#   - python-dotenv : Loads TAVILY_API_KEY from .env
#
# 🔧 SETUP:
#   1. Get a free API key at https://tavily.com
#   2. Add to .env: TAVILY_API_KEY="tvly-..."
#   3. pip install tavily-python python-dotenv
#
# 💡 AI AGENT MINDSET:
#   Tavily is purpose-built for AI — it returns clean, structured
#   results optimised for LLM consumption (not raw HTML).
#   The search() method returns:
#     - query       : the original search query
#     - results     : list of {title, url, content, score}
#     - answer      : optional AI-generated summary of results
#
# 🔁 NEXT STEP: See tavilywithAgent.py to wire this into an
#   AutoGen agent as a callable tool.
# ============================================================

import asyncio

from dotenv import load_dotenv
from tavily import TavilyClient

# Load TAVILY_API_KEY from .env file
load_dotenv()


async def web_search():
    # ----------------------------------------------------------
    # Step 1: Instantiate the Tavily client
    # It automatically reads TAVILY_API_KEY from the environment.
    # ----------------------------------------------------------
    tavily_client = TavilyClient()

    # ----------------------------------------------------------
    # Step 2: Perform a web search
    # search() sends the query to Tavily and returns a dict with
    # live web results ranked by relevance.
    # ----------------------------------------------------------
    search_results = tavily_client.search("What is the capital of France?")

    # ----------------------------------------------------------
    # Step 3: Print and return the results
    # In a real application, you'd parse results and feed them
    # to an LLM for synthesis into a natural language answer.
    # ----------------------------------------------------------
    print(search_results)
    return search_results


asyncio.run(web_search())
