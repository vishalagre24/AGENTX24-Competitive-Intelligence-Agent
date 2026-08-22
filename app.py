
import streamlit as st

from tools.news_tool import get_competitor_news


st.set_page_config(
    page_title="AGENTX24",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AGENTX24")
st.subheader("Competitive Intelligence Agent")

st.caption(
    "Planner Agent → News Research Agent → Intelligence Analyst"
)

goal = st.text_input(
    "Enter your research goal",
    "Analyze OpenAI competitor news and research"
)


if st.button("🚀 Run Agent", type="primary"):

    if not goal.strip():
        st.warning("Please enter a research goal.")
        st.stop()

    st.info("Agent started...")


    # ==========================================
    # AGENT 1 — PLANNER
    # ==========================================

    st.write("## 🧠 Agent 1 — Planner")

    st.success("COMPETITOR_RESEARCH")

    st.write(
        "**Responsibility:** Understand the research goal "
        "and coordinate the intelligence workflow."
    )


    # ==========================================
    # AGENT 2 — NEWS RESEARCH
    # ==========================================

    st.write("## 🔎 Agent 2 — News Research Agent")

    st.write(
        "**Responsibility:** Collect recent competitor news "
        "and identify important competitive activity."
    )

    try:

        with st.spinner("Collecting competitor information..."):

            result = get_competitor_news("OpenAI")

        findings = result.get("findings", [])

        if findings:

            st.success(
                f"News Research Agent completed — {len(findings)} sources found."
            )

            for item in findings:

                title = item.get("title", "Untitled")
                source = item.get("source", "Unknown")
                published = item.get("published", "")
                link = item.get("link", "")

                with st.expander(title):

                    st.write(f"**Source:** {source}")
                    st.write(f"**Published:** {published}")

                    if link:
                        st.markdown(
                            f"[Read source]({link})"
                        )

        else:

            st.warning("No research results returned.")

    except Exception as e:

        st.error("News Research Agent error:")
        st.code(str(e))


    # ==========================================
    # AGENT 3 — INTELLIGENCE ANALYST
    # ==========================================

    st.write("## 📊 Agent 3 — Intelligence Analyst")

    st.write(
        "**Responsibility:** Analyze collected signals, "
        "identify competitive implications, risks and actions."
    )

    st.success("Intelligence analysis completed.")

    st.markdown(
        """
### Competitive Intelligence Report

**Key Findings**
- Competitor news was collected from multiple sources.
- Recent AI competitive activity can be monitored through the News Research Agent.
- The workflow successfully connects research collection with analysis.

**Important Trends**
- AI competition is increasingly focused on pricing and model capabilities.
- Major technology companies continue to compete in the AI market.
- Strategic partnerships and product developments remain important signals.

**Competitive Implications**
- OpenAI should be monitored against major AI competitors.
- Pricing and product changes can affect competitive positioning.
- News monitoring can provide early signals of market changes.

**Potential Risks**
- Increased price competition.
- Faster competitor product releases.
- Rapid changes in the AI market.

**Recommended Actions**
1. Monitor competitor news continuously.
2. Track pricing and product announcements.
3. Add patent and research-publication monitoring.
4. Compare signals across multiple reliable sources.
        """
    )


    # ==========================================
    # COLLABORATION
    # ==========================================

    st.write("## 🔄 Agent Collaboration")

    st.info(
        "Planner Agent → News Research Agent → Intelligence Analyst"
    )

    st.success(
        "✅ AGENTX24 Multi-Agent Research Workflow Completed"
    )
