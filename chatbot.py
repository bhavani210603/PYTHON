import os
import streamlit as st
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages

#set my groq api
os.environ["GROQ_API_KEY"]="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"

#Deine state structure
class State(TypedDict):
    messages:Annotated[list,add_messages]

#Initilize LLM Model
llm = ChatGroq(model_name="Llama3-70b-8192", temperature=0.7)

# define node
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

#Build graph
workflow=StateGraph(State)
workflow.add_node("chat",chatbot)
workflow.set_entry_point("chat")
workflow.add_edge("chat",END)

#compile the graph
graph= workflow.compile()

#run the graph with an initial user meassage
initial_state={"messages":[{"role":"user","content":"How are you?"}]}

final_state=graph.invoke(initial_state)

#Display messages
for msg in final_state["messages"]:
    print(f"{msg.type}: {msg.content}")

