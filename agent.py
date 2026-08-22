import os

from dotenv import load_dotenv
from google import genai

from planner import decide_task
from tools.research import research_competitor
from tools.patents import search_patents
from tools.publications import search_publications


# ==========================================
# 1. LOAD ENVIRONMENT
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("KEY FOUND:", bool(api_key))

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# ==========================================
# 2. USER GOAL
# ==========================================

user_input = input(
    "\nEnter your research goal: "
).strip()

if not user_input:
    user_input = "Track OpenAI competitor activity"


print("\nUSER GOAL:")
print(user_input)


# ==========================================
# 3. PLANNER
# ==========================================

task = decide_task(user_input)

print("\nPLANNER DECISION:")
print(task)


# ==========================================
# 4. TOOL EXECUTION
# ==========================================

results = {}


if task == "NEWS_SEARCH":

    print("\nRunning News Tool...")

    results["news"] = research_competitor("OpenAI")


elif task == "PATENT_SEARCH":

    print("\nRunning Patent Tool...")

    results["patents"] = search_patents("OpenAI")


elif task == "RESEARCH_SEARCH":

    print("\nRunning Research Publication Tool...")

    results["research"] = search_publications(
        "generative AI"
    )


elif task == "MULTI_SOURCE_RESEARCH":

    print("\nRunning multiple research tools...")

    results["news"] = research_competitor("OpenAI")

    results["patents"] = search_patents("OpenAI")

    results["research"] = search_publications(
        "generative AI"
    )


else:

    print("\nUnknown task.")
    exit()


# ==========================================
# 5. DISPLAY RAW RESULTS
# ==========================================

print("\n===== TOOL RESULTS =====")

for name, data in results.items():

    print(f"\n--- {name.upper()} ---")
    print(data)


# ==========================================
# 6. GEMINI ANALYSIS
# ==========================================

prompt = f"""
You are an autonomous Competitive Intelligence AI Agent.

USER GOAL:
{user_input}

PLANNER DECISION:
{task}

RESEARCH RESULTS:
{results}

Analyze the available information and create a concise
competitive intelligence report.

Include:

1. Key Findings
2. Important Trends
3. Competitive Implications
4. Potential Risks
5. Recommended Actions

Rules:
- Do not invent facts.
- Clearly identify insufficient information.
- Base conclusions on the supplied research results.
- Prefer specific evidence over generic statements.
"""


print("\nSENDING DATA TO GEMINI...")


try:

    chat = client.chats.create(
        model="gemini-3.6-flash"
    )

    response = chat.send_message(prompt)

    print("\n===== INSIGHT REPORT =====")

    if response.text:
        print(response.text)
    else:
        print("Gemini returned an empty response.")


except Exception as e:

    print("\nGEMINI ERROR:")
    print(type(e).__name__)
    print(str(e))