# AGENTX24 — Competitive Intelligence Agent

AGENTX24 is a competitive intelligence research agent designed to analyze competitor activity using dynamic tool selection, parallel research, failure recovery, evidence analysis, and uncertainty-aware decision making.

## Task 5 — Agent Framework

For Task 5, AGENTX24 uses **LangGraph** to implement a stateful agent workflow.

### Why LangGraph?

LangGraph was selected because it provides explicit graph-based state management, conditional routing, checkpointing, and support for iterative agent workflows. These capabilities are useful for building an agent that can react to tool failures and change its execution path instead of following only a fixed sequence.

## Architecture

```text
User Research Goal
        |
        v
Dynamic Planner
        |
        v
Parallel Research Orchestrator
       / \
      /   \
 News     Research
  |          |
  |          |
  +----+-----+
       |
       v
 Failure Detection
       |
       v
 Fallback Recovery
       |
       v
 Evidence Analyzer
       |
       v
 Conflict Detection
       |
       v
 Confidence / Decision
       |
       v
 Evaluator
       |
       v
 Final Result
```

## Task 5 Capabilities

### Dynamic Planning

The planner analyzes the user's research goal and dynamically selects relevant research tools.

For example:

```text
Analyze OpenAI competitor news and research
```

selects:

```text
NEWS_SEARCH
RESEARCH_SEARCH
```

### Multi-Agent Orchestration

The research stage coordinates separate News and Research agents.

### Parallel Execution

Selected research tasks are executed concurrently using Python's `ThreadPoolExecutor`.

### Shared State

LangGraph maintains a shared `AgentState` containing:

* User research goal
* Selected tools
* Research results
* Errors
* Failed tools
* Iteration count
* Fallback status
* Evidence
* Conflict status
* Confidence
* Decision

### Conditional Routing

The graph changes its execution path depending on the current state.

A failed research tool is routed to the fallback node, while successful research proceeds to evidence analysis.

### Checkpointing

LangGraph `InMemorySaver` is used as the checkpoint mechanism.

The final shared state can be retrieved from the graph checkpoint after execution.

### Failure Recovery

The Task 5 adversarial test intentionally simulates a News Search failure.

The system detects the failure and activates a fallback research path.

Example:

```text
NEWS_SEARCH FAILED
        ↓
FALLBACK ROUTER
        ↓
Fallback Research
        ↓
Recovery Successful
```

### Conflicting Evidence

The evidence analyzer evaluates collected evidence and detects conflicting claims.

The adversarial test includes contradictory pricing-related claims to demonstrate conflict detection.

### Uncertainty-Aware Decisions

When conflicting evidence is detected, the system does not make an overly strong conclusion.

Instead, it produces an uncertainty-aware decision and lowers the confidence score.

Example:

```text
Conflict detected: True
Confidence: 0.55
Decision: UNCERTAIN
```

### Self-Evaluation

An evaluator node checks the execution state and determines whether the workflow successfully produced usable results.

### Loop / Deadlock Protection

The graph maintains an iteration counter and limits retry behavior to prevent uncontrolled execution loops.

## Adversarial Test

The Task 5 adversarial test demonstrates recovery from a simulated tool failure.

Test scenario:

```text
Research Goal:
Analyze OpenAI competitor news and research
```

The News agent is intentionally forced to fail.

Expected recovery:

```text
Planner
   ↓
Parallel Research
   ↓
News Failure
   ↓
Fallback
   ↓
Evidence Analysis
   ↓
Conflict Detection
   ↓
Evaluator
   ↓
PASSED
```

Observed test results include:

```text
Status: PASSED
Failed tools: ['news']
Fallback used: True
Conflict detected: True
Confidence: 0.55
```

## Demo Research Goal

Use the following research goal to demonstrate the system:

> Analyze OpenAI competitor news and research

This goal is useful because it can trigger both news and research tool selection.

## Running the Project

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the Task 5 graph test:

```powershell
python .\task5_graph.py
```

Run the Streamlit application:

```powershell
python -m streamlit run .\app.py --server.port 8502
```

Then open:

```text
http://localhost:8502
```

## Project Structure

```text
AGENTX24/
│
├── app.py
├── agent.py
├── planner.py
├── task5_graph.py
│
├── data/
│   └── memory.py
│
├── tools/
│   ├── multi_source_research.py
│   ├── mysql_tool.py
│   ├── news_tool.py
│   ├── patents.py
│   ├── publications.py
│   ├── research.py
│   ├── research_tool.py
│   ├── verification.py
│   └── web_search_tool.py
│
└── .gitignore
```

## Security

Environment variables and API keys are stored locally in `.env` and are excluded from Git using `.gitignore`.

Do not commit API keys, passwords, or other credentials to the repository.

## Task 5 Result

The Task 5 LangGraph implementation successfully demonstrates:

* Dynamic planning
* Multi-agent orchestration
* Parallel execution
* Shared state
* Conditional routing
* Checkpointing
* Failure recovery
* Tool fallback
* Conflicting-evidence detection
* Uncertainty-aware decisions
* Self-evaluation
* Loop/deadlock protection
* Adversarial testing
