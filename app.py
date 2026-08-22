
import uuid

import streamlit as st

from task5_graph import graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AGENTX24 - Task 5",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AGENTX24")
st.subheader("Task 5 — LangGraph Competitive Intelligence Agent")

st.caption(
    "Dynamic Planning → Parallel Agents → Failure Recovery → "
    "Evidence Analysis → Evaluation"
)


# ============================================================
# USER INPUT
# ============================================================

goal = st.text_input(
    "Enter your research goal",
    "Analyze OpenAI competitor news and research"
)


# ============================================================
# RUN AGENT
# ============================================================

if st.button("🚀 Run Task 5 Agent", type="primary"):

    if not goal.strip():
        st.warning("Please enter a research goal.")
        st.stop()

    st.info("LangGraph agent started...")

    # ========================================================
    # INITIAL SHARED STATE
    # ========================================================

    initial_state = {
        "user_goal": goal,

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

    # ========================================================
    # CHECKPOINT CONFIG
    # ========================================================

    config = {
        "configurable": {
            "thread_id": (
                "streamlit-task5-"
                + uuid.uuid4().hex
            )
        }
    }

    # ========================================================
    # EXECUTE LANGGRAPH
    # ========================================================

    try:

        with st.spinner(
            "Running autonomous LangGraph workflow..."
        ):

            final_state = graph.invoke(
                initial_state,
                config=config
            )

    except Exception as exc:

        st.error("Agent execution failed.")

        st.exception(exc)

        st.stop()


    # ========================================================
    # 1. PLANNER
    # ========================================================

    st.write("## 🧠 Agent 1 — Dynamic Planner")

    selected_tools = final_state.get(
        "selected_tools",
        []
    )

    st.success(
        f"Selected tools: {', '.join(selected_tools)}"
    )

    st.write(
        "**Responsibility:** Dynamically determine which "
        "research tools are relevant to the user's goal."
    )


    # ========================================================
    # 2. PARALLEL RESEARCH
    # ========================================================

    st.write("## 🔎 Agent 2 — Parallel Research Orchestrator")

    st.write(
        "**Responsibility:** Execute selected research "
        "agents concurrently and recover from failures."
    )

    results = final_state.get(
        "results",
        {}
    )

    if results:

        st.success(
            f"Research completed — "
            f"{len(results)} result sources available."
        )

        for source_name, source_data in results.items():

            with st.expander(
                f"📚 {source_name.upper()}"
            ):

                if isinstance(
                    source_data,
                    dict
                ):

                    st.json(source_data)

                else:

                    st.write(source_data)

    else:

        st.warning(
            "No research results returned."
        )


    # ========================================================
    # 3. FAILURE RECOVERY
    # ========================================================

    st.write("## 🛠️ Failure Recovery")

    failed_tools = final_state.get(
        "failed_tools",
        []
    )

    errors = final_state.get(
        "errors",
        []
    )

    fallback_used = final_state.get(
        "fallback_used",
        False
    )

    if failed_tools:

        st.warning(
            "Failed tools: "
            + ", ".join(failed_tools)
        )

    else:

        st.success(
            "No tool failures detected."
        )

    if fallback_used:

        st.success(
            "✅ Fallback mechanism activated "
            "and recovery completed."
        )

    if errors:

        with st.expander("View execution errors"):

            for error in errors:

                st.code(error)


    # ========================================================
    # 4. EVIDENCE ANALYSIS
    # ========================================================

    st.write("## 🔬 Agent 3 — Evidence Analyzer")

    evidence = final_state.get(
        "evidence",
        []
    )

    conflict_detected = final_state.get(
        "conflict_detected",
        False
    )

    if evidence:

        st.write(
            f"Evidence items analyzed: "
            f"**{len(evidence)}**"
        )

        for item in evidence:

            source = item.get(
                "source",
                "Unknown"
            )

            claim = item.get(
                "claim",
                "Unknown claim"
            )

            reliability = item.get(
                "reliability",
                0
            )

            st.markdown(
                f"""
**Source:** {source}

**Claim:** {claim}

**Reliability:** {reliability}
"""
            )

    else:

        st.warning(
            "No evidence was available for analysis."
        )


    # ========================================================
    # 5. CONFLICT DETECTION
    # ========================================================

    st.write("## ⚖️ Conflicting Evidence Resolution")

    if conflict_detected:

        st.warning(
            "⚠️ Conflicting evidence detected."
        )

    else:

        st.success(
            "✅ No major evidence conflict detected."
        )


    # ========================================================
    # 6. UNCERTAINTY / CONFIDENCE
    # ========================================================

    st.write("## 🎯 Confidence & Decision")

    confidence = final_state.get(
        "confidence",
        0.0
    )

    decision = final_state.get(
        "decision",
        ""
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Confidence",
            f"{confidence:.0%}"
        )

    with col2:

        st.metric(
            "Iteration",
            final_state.get(
                "iteration",
                0
            )
        )

    if decision:

        st.info(
            decision
        )


    # ========================================================
    # 7. EVALUATOR
    # ========================================================

    st.write("## ✅ Agent 4 — Evaluator")

    status = final_state.get(
        "status",
        "UNKNOWN"
    )

    if status == "PASSED":

        st.success(
            "TASK 5 AGENT EXECUTION PASSED"
        )

    else:

        st.error(
            f"Agent status: {status}"
        )


    # ========================================================
    # 8. CHECKPOINT
    # ========================================================

    st.write("## 💾 LangGraph Checkpoint")

    try:

        checkpoint = graph.get_state(
            config
        )

        st.success(
            "Checkpoint successfully created."
        )

        with st.expander(
            "View shared checkpoint state"
        ):

            st.json(
                dict(
                    checkpoint.values
                )
            )

    except Exception as exc:

        st.warning(
            "Checkpoint could not be displayed."
        )

        st.code(
            str(exc)
        )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    st.write("## 🏁 Task 5 Final Result")

    st.markdown(
        f"""
**Status:** `{status}`

**Selected Tools:** `{selected_tools}`

**Failed Tools:** `{failed_tools}`

**Fallback Used:** `{fallback_used}`

**Conflict Detected:** `{conflict_detected}`

**Confidence:** `{confidence:.0%}`

**Decision:** {decision}
"""
    )

    st.success(
        "✅ AGENTX24 Task 5 LangGraph workflow completed."
    )
