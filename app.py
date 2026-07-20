
import streamlit as st
from langgraph_setup import build_graph

st.set_page_config(page_title="LangGraph Research-to-Report", page_icon=":brain:")
st.title(":brain: Researcher + Writer — LangGraph")
st.caption("LangGraph StateGraph · Groq llama-3.3-70b-versatile · Explicit node pipeline")

topic = st.text_input("Enter a research topic", placeholder="e.g. AI agents in education")

if st.button("Generate Report", type="primary") and topic:
    app = build_graph()
    with st.spinner("Researcher node running, then Writer node..."):
        result = app.invoke({"topic": topic, "research": "", "report": ""})
    st.success("Report ready!")

    with st.expander("Show intermediate research"):
        st.write(result["research"])

    st.markdown(result["report"])
    st.download_button("Download report (.md)", result["report"], file_name="report.md")
elif not topic:
    st.info("Enter a topic above and click Generate Report to run the graph.")

with st.expander("How this differs from the CrewAI version"):
    st.write(
        "Instead of Agent/Task/Crew objects, this pipeline is an explicit "
        "LangGraph StateGraph: research_node writes into state[\'research\'], "
        "writer_node reads it back out and writes state[\'report\']. The edge "
        "researcher -> writer is the handoff, defined by hand instead of "
        "CrewAI\'s Process.sequential."
    )
