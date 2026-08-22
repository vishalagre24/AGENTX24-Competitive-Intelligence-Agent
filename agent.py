import os
import json

from dotenv import load_dotenv
from google import genai

from planner import decide_tools
from tools.news_tool import search_news
from tools.research_tool import search_research


# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# USER GOAL
# --------------------------------------------------

user_input = "Analyze OpenAI competitor news and research"

print("\n==============================")
print("AGENTX24")
print("==============================")

print("\nUSER GOAL:")
print(user_input)


# --------------------------------------------------
# 1. PLANNER
# --------------------------------------------------

selected_tools = decide_tools(user_input)

print("\nSELECTED TOOLS:")

for tool in selected_tools:
    print(f"- {tool}")


# --------------------------------------------------
# 2. EXTRACT TOPIC
# --------------------------------------------------

company = "OpenAI"
research_topic = "OpenAI generative AI"


# --------------------------------------------------
# 3. DYNAMIC TOOL EXECUTION
# --------------------------------------------------

research_data = {}

if "NEWS_SEARCH" in selected_tools:

    print("\nEXECUTING NEWS_SEARCH...")

    news_result = search_news(company)

    research_data["news"] = news_result

    print(
        f"NEWS RESULTS: "
        f"{news_result.get('results_found', 0)}"
    )


if "RESEARCH_SEARCH" in selected_tools:

    print("\nEXECUTING RESEARCH_SEARCH...")

    research_result = search_research(research_topic)

    research_data["research"] = research_result

    print(
        f"RESEARCH RESULTS: "
        f"{research_result.get('results_found', 0)}"
    )


# --------------------------------------------------
# 4. DISPLAY COMBINED DATA
# --------------------------------------------------

print("\n==============================")
print("COMBINED RESEARCH DATA")
print("==============================")

print(json.dumps(research_data, indent=2))


# --------------------------------------------------
# 5. GEMINI ANALYSIS
# --------------------------------------------------

print("\nSENDING COMBINED RESULTS TO GEMINI...")

prompt = f"""
You are AGENTX24, an autonomous competitive intelligence AI agent.

User goal:
{user_input}

The planner dynamically selected these tools:
{selected_tools}

The tools returned the following research data:

{json.dumps(research_data, indent=2)}

Analyze the available evidence and produce a concise,
actionable competitive intelligence report.

Include:

1. Key findings
2. Important developments
3. Competitive implications
4. Potential risks
5. Recommended actions

Do not invent facts that are not present in the research data.
Clearly distinguish evidence from interpretation.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)


# --------------------------------------------------
# 6. FINAL REPORT
# --------------------------------------------------

print("\n==============================")
print("FINAL INSIGHT REPORT")
print("==============================")

print(response.text)

print("\n==============================")
print("AGENTX24 RUN COMPLETE")
print("==============================")