import streamlit as st

st.set_page_config(
    page_title="AGENTX24",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AGENTX24")
st.subheader("Competitive Intelligence Agent")

goal = st.text_input(
    "Enter your research goal",
    "Track OpenAI competitor activity"
)

if st.button("🚀 Run Agent"):
    st.info("Agent started...")

    st.write("### 🧠 Planner")
    st.success("COMPETITOR_RESEARCH")

    st.write("### 🔎 Research")
    st.write("Collecting competitor information...")

    st.write("### 🤖 Gemini Analysis")
    st.write("Generating competitive intelligence...")

    st.write("### 📊 Insight Report")
    st.write(
        "Key findings and recommended actions will appear here."
    )