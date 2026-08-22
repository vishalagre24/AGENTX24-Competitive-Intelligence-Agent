from typing import TypedDict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from tools.news_tool import search_news
from tools.research_tool import search_research


# ============================================================
# SHARED STATE
# ============================================================

class AgentState(TypedDict):
    user_goal: str

    selected_tools: List[str]

    results: dict

    errors: List[str]

    status: str

    iteration: int

    failed_tools: List[str]

    fallback_used: bool

    # Task 5: evidence reasoning
    evidence: List[dict]

    conflict_detected: bool

    confidence: float

    decision: str


# ============================================================
# PLANNER
# ============================================================

def planner_node(state: AgentState):

    goal = state["user_goal"].lower()

    tools = []

    # --------------------------------------------------------
    # Dynamic tool selection
    # --------------------------------------------------------

    if any(word in goal for word in [
        "news",
        "latest",
        "announcement",
        "competitor",
        "activity",
        "update",
        "track"
    ]):
        tools.append("NEWS_SEARCH")

    if any(word in goal for word in [
        "research",
        "paper",
        "papers",
        "publication",
        "study",
        "academic"
    ]):
        tools.append("RESEARCH_SEARCH")

    # Default
    if not tools:
        tools.append("NEWS_SEARCH")

    iteration = state.get("iteration", 0) + 1

    print("\n[PLANNER]")
    print("Selected tools:", tools)
    print("Iteration:", iteration)

    return {
        "selected_tools": tools,
        "iteration": iteration,
        "status": "PLANNED"
    }


# ============================================================
# NEWS AGENT
# ============================================================

def run_news():

    print("\n[NEWS AGENT] Starting...")

    # --------------------------------------------------------
    # ADVERSARIAL FAILURE TEST
    # --------------------------------------------------------
    # Intentionally fail the news tool.
    # The fallback system should recover.
    # --------------------------------------------------------

    raise RuntimeError(
        "Simulated NEWS_SEARCH failure"
    )


# ============================================================
# RESEARCH AGENT
# ============================================================

def run_research():

    print("\n[RESEARCH AGENT] Starting...")

    result = search_research(
        "OpenAI generative AI"
    )

    return result


# ============================================================
# FALLBACK RESEARCH
# ============================================================

def run_research_fallback():

    print(
        "\n[FALLBACK AGENT] "
        "Using research source as fallback..."
    )

    result = search_research(
        "OpenAI competitor AI news"
    )

    return result


# ============================================================
# PARALLEL RESEARCH ORCHESTRATOR
# ============================================================

def research_node(state: AgentState):

    print("\n[RESEARCH ORCHESTRATOR]")
    print("Running agents in parallel...")

    results = dict(
        state.get("results", {})
    )

    errors = list(
        state.get("errors", [])
    )

    failed_tools = list(
        state.get("failed_tools", [])
    )

    tasks = {}

    # --------------------------------------------------------
    # Dynamic task creation
    # --------------------------------------------------------

    if "NEWS_SEARCH" in state["selected_tools"]:
        tasks["news"] = run_news

    if "RESEARCH_SEARCH" in state["selected_tools"]:
        tasks["research"] = run_research

    # --------------------------------------------------------
    # Parallel execution
    # --------------------------------------------------------

    with ThreadPoolExecutor(
        max_workers=max(1, len(tasks))
    ) as executor:

        futures = {
            executor.submit(function): name
            for name, function in tasks.items()
        }

        for future in as_completed(futures):

            name = futures[future]

            try:

                result = future.result()

                results[name] = result

                print(
                    f"[{name.upper()}] "
                    "completed successfully"
                )

            except Exception as exc:

                message = (
                    f"{name}: "
                    f"{type(exc).__name__}: {exc}"
                )

                errors.append(message)
                failed_tools.append(name)

                print(
                    f"[{name.upper()}] FAILED"
                )

                print(
                    "Reason:",
                    exc
                )

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    if results:
        status = "PARTIAL_SUCCESS"
    else:
        status = "RESEARCH_FAILED"

    return {
        "results": results,
        "errors": errors,
        "failed_tools": failed_tools,
        "status": status
    }


# ============================================================
# FAILURE RECOVERY / FALLBACK
# ============================================================

def fallback_node(state: AgentState):

    print("\n[FALLBACK ROUTER]")

    results = dict(
        state.get("results", {})
    )

    errors = list(
        state.get("errors", [])
    )

    failed_tools = list(
        state.get("failed_tools", [])
    )

    fallback_used = state.get(
        "fallback_used",
        False
    )

    # --------------------------------------------------------
    # News failed → research fallback
    # --------------------------------------------------------

    if "news" in failed_tools:

        print(
            "NEWS_SEARCH failed."
        )

        print(
            "Activating fallback research..."
        )

        try:

            fallback_result = (
                run_research_fallback()
            )

            results["news_fallback"] = (
                fallback_result
            )

            fallback_used = True

            print(
                "[FALLBACK] "
                "Recovery successful"
            )

        except Exception as exc:

            errors.append(
                "fallback: "
                f"{type(exc).__name__}: {exc}"
            )

            print(
                "[FALLBACK] "
                "Recovery failed"
            )

    return {
        "results": results,
        "errors": errors,
        "fallback_used": fallback_used,
        "status": "RECOVERED"
    }


# ============================================================
# CONFLICTING EVIDENCE ANALYZER
# ============================================================

def evidence_analysis_node(state: AgentState):

    print("\n[EVIDENCE ANALYZER]")

    results = state.get(
        "results",
        {}
    )

    evidence = []

    # --------------------------------------------------------
    # Collect real research evidence
    # --------------------------------------------------------

    for source_name, source_data in results.items():

        if not isinstance(
            source_data,
            dict
        ):
            continue

        findings = source_data.get(
            "findings",
            []
        )

        if isinstance(
            findings,
            list
        ):

            for item in findings[:5]:

                if isinstance(
                    item,
                    dict
                ):

                    title = item.get(
                        "title",
                        "Unknown finding"
                    )

                    source = item.get(
                        "source",
                        source_name
                    )

                    evidence.append({
                        "source": source,
                        "claim": title,
                        "reliability": 0.70
                    })

    # --------------------------------------------------------
    # CONTROLLED CONFLICTING EVIDENCE
    # --------------------------------------------------------
    # Used specifically for Task 5 adversarial testing.
    # --------------------------------------------------------

    evidence.append({
        "source": "Source_A",
        "claim": (
            "OpenAI is increasing competitive "
            "pressure through aggressive AI pricing."
        ),
        "reliability": 0.85
    })

    evidence.append({
        "source": "Source_B",
        "claim": (
            "OpenAI is reducing price pressure "
            "and focusing more on premium positioning."
        ),
        "reliability": 0.60
    })

    # --------------------------------------------------------
    # Conflict detection
    # --------------------------------------------------------

    pricing_claims = []

    for item in evidence:

        claim = item["claim"].lower()

        if (
            "price" in claim
            or "pricing" in claim
        ):
            pricing_claims.append(
                claim
            )

    conflict_detected = (
        len(pricing_claims) >= 2
    )

    # --------------------------------------------------------
    # Uncertainty-aware decision
    # --------------------------------------------------------

    if conflict_detected:

        confidence = 0.55

        decision = (
            "UNCERTAIN: conflicting evidence "
            "was detected. Additional verification "
            "is recommended before making a strong "
            "strategic conclusion."
        )

    elif evidence:

        confidence = 0.80

        decision = (
            "SUPPORTED: available evidence "
            "is reasonably consistent."
        )

    else:

        confidence = 0.20

        decision = (
            "INSUFFICIENT_EVIDENCE: "
            "no reliable evidence available."
        )

    print(
        "Evidence items:",
        len(evidence)
    )

    print(
        "Conflict detected:",
        conflict_detected
    )

    print(
        "Confidence:",
        confidence
    )

    print(
        "Decision:",
        decision
    )

    return {
        "evidence": evidence,
        "conflict_detected": conflict_detected,
        "confidence": confidence,
        "decision": decision,
        "status": "EVIDENCE_ANALYZED"
    }


# ============================================================
# EVALUATOR
# ============================================================

def evaluation_node(state: AgentState):

    print("\n[EVALUATOR]")

    results = state.get(
        "results",
        {}
    )

    errors = state.get(
        "errors",
        []
    )

    print(
        "Successful sources:",
        list(results.keys())
    )

    if errors:

        print(
            "Errors detected:",
            len(errors)
        )

    # --------------------------------------------------------
    # Success condition
    # --------------------------------------------------------

    if results:

        status = "PASSED"

    else:

        status = "FAILED"

    return {
        "status": status
    }


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

def route_after_research(state: AgentState):

    # --------------------------------------------------------
    # If any tool failed → fallback
    # --------------------------------------------------------

    if state.get(
        "failed_tools"
    ):

        return "fallback"

    # --------------------------------------------------------
    # Otherwise → evidence analysis
    # --------------------------------------------------------

    return "evidence"


def route_after_evaluation(state: AgentState):

    # --------------------------------------------------------
    # Successful execution
    # --------------------------------------------------------

    if state["status"] == "PASSED":

        return "finish"

    # --------------------------------------------------------
    # Deadlock protection
    # --------------------------------------------------------

    if state["iteration"] >= 3:

        print(
            "[ROUTER] Maximum iterations reached."
        )

        return "finish"

    # --------------------------------------------------------
    # Retry through fallback
    # --------------------------------------------------------

    return "fallback"


# ============================================================
# GRAPH
# ============================================================

builder = StateGraph(
    AgentState
)


# ============================================================
# NODES
# ============================================================

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "research",
    research_node
)

builder.add_node(
    "fallback",
    fallback_node
)

builder.add_node(
    "evidence_analysis",
    evidence_analysis_node
)

builder.add_node(
    "evaluator",
    evaluation_node
)


# ============================================================
# START → PLANNER
# ============================================================

builder.add_edge(
    START,
    "planner"
)


# ============================================================
# PLANNER → RESEARCH
# ============================================================

builder.add_edge(
    "planner",
    "research"
)


# ============================================================
# RESEARCH → CONDITIONAL ROUTING
# ============================================================

builder.add_conditional_edges(
    "research",
    route_after_research,
    {
        "fallback": "fallback",
        "evidence": "evidence_analysis"
    }
)


# ============================================================
# FALLBACK → EVIDENCE ANALYSIS
# ============================================================

builder.add_edge(
    "fallback",
    "evidence_analysis"
)


# ============================================================
# EVIDENCE ANALYSIS → EVALUATOR
# ============================================================

builder.add_edge(
    "evidence_analysis",
    "evaluator"
)


# ============================================================
# EVALUATOR → FINAL / FALLBACK
# ============================================================

builder.add_conditional_edges(
    "evaluator",
    route_after_evaluation,
    {
        "finish": END,
        "fallback": "fallback"
    }
)


# ============================================================
# CHECKPOINTING
# ============================================================

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "AGENTX24 TASK 5"
    )

    print(
        "ADVERSARIAL AGENT TEST"
    )

    print(
        "=============================="
    )

    # --------------------------------------------------------
    # Initial shared state
    # --------------------------------------------------------

    initial_state: AgentState = {

        "user_goal":
            "Analyze OpenAI competitor "
            "news and research",

        "selected_tools": [],

        "results": {},

        "errors": [],

        "status": "STARTING",

        "iteration": 0,

        "failed_tools": [],

        "fallback_used": False,

        "evidence": [],

        "conflict_detected": False,

        "confidence": 0.0,

        "decision": ""
    }

    # --------------------------------------------------------
    # LangGraph checkpoint configuration
    # --------------------------------------------------------

    config = {
        "configurable": {
            "thread_id":
                "task5-adversarial-demo-001"
        }
    }

    # --------------------------------------------------------
    # Run graph
    # --------------------------------------------------------

    final_state = graph.invoke(
        initial_state,
        config=config
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print(
        "\n=============================="
    )

    print(
        "TASK 5 FINAL RESULT"
    )

    print(
        "=============================="
    )

    print(
        "Status:",
        final_state["status"]
    )

    print(
        "Iteration:",
        final_state["iteration"]
    )

    print(
        "Sources:",
        list(
            final_state["results"].keys()
        )
    )

    print(
        "Failed tools:",
        final_state["failed_tools"]
    )

    print(
        "Fallback used:",
        final_state["fallback_used"]
    )

    print(
        "Errors:",
        final_state["errors"]
    )

    # --------------------------------------------------------
    # Evidence results
    # --------------------------------------------------------

    print(
        "Conflict detected:",
        final_state["conflict_detected"]
    )

    print(
        "Confidence:",
        final_state["confidence"]
    )

    print(
        "Decision:",
        final_state["decision"]
    )

    # ========================================================
    # CHECKPOINT
    # ========================================================

    checkpoint = graph.get_state(
        config
    )

    print(
        "\n=============================="
    )

    print(
        "CHECKPOINT"
    )

    print(
        "=============================="
    )

    print(
        checkpoint.values
    )

    print(
        "\n=============================="
    )

    print(
        "TASK 5 ADVERSARIAL TEST COMPLETE"
    )

    print(
        "=============================="
    )