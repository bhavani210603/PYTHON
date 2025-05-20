from flask import Flask, render_template, request
import os
import asyncio
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
import time

app = Flask(__name__)

os.environ["GROQ_API_KEY"]="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"
# Initialize LLM
llm = ChatGroq(model_name="Llama3-70b-8192", temperature=0.7)

# Define state class
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define chatbot node
def chatbot(state: State):
    time.sleep(10)  # Simulate delay
    response=llm.invoke(state["messages"])
    return {"messages": response}

# Define workflow
workflow = StateGraph(State)
workflow.add_node("chat", chatbot)
workflow.add_edge("chat", END)
workflow.set_entry_point("chat")
graph = workflow.compile()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
async def chat():
    user_input = request.form["user_input"]
    initial_state = {"messages": [{"role": "user", "content": user_input}]}
    final_state = await graph.ainvoke(initial_state)
    for msg in final_state["messages"]:
        bot_response=(f"{msg.type}: {msg.content}")
    return render_template("index.html", response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)
