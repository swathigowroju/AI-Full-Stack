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

    def research_node(state):
        topic = state["topic"]
        msgs = [
            SystemMessage(content="You are a meticulous research analyst."),
            HumanMessage(content="Research the topic '" + topic +
                          "' and list 5 verifiable findings as bullet points."),
        ]
        state["research"] = groq_chat.invoke(msgs).content
        return state

    def writer_node(state):
        topic = state["topic"]
        research = state["research"]
        prompt = (
            "Using this research brief:\n\n" + research +
            "\n\nWrite a markdown report on '" + topic +
            "' with an intro, 3 sections, and a conclusion."
        )
        msgs = [
            SystemMessage(content="You are a clear, structured technical writer."),
            HumanMessage(content=prompt),
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
