
import os
import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage


class CrewState(TypedDict):
    topic: str
    research: str
    report: str


@st.cache_resource
def build_graph():
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    groq_chat = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4, api_key=api_key)

    def research_node(state: CrewState) -> CrewState:
        msgs = [
            SystemMessage(content="You are a meticulous research analyst."),
            HumanMessage(content=f"Research the topic \'{state[\'topic\']}\' and list "
                                  f"5 verifiable findings as bullet points."),
        ]
        state["research"] = groq_chat.invoke(msgs).content
        return state

    def writer_node(state: CrewState) -> CrewState:
        msgs = [
            SystemMessage(content="You are a clear, structured technical writer."),
            HumanMessage(content=f"Using this research brief:\n\n{state[\'research\']}\n\n"
                                  f"Write a markdown report on \'{state[\'topic\']}\' with an "
                                  f"intro, 3 sections, and a conclusion."),
        ]
        state["report"] = groq_chat.invoke(msgs).content
        return state

    graph = StateGraph(CrewState)
    graph.add_node("researcher", research_node)
    graph.add_node("writer", writer_node)
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", END)

    return graph.compile()
