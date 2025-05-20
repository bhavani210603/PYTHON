import os
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# 1. Set your API key
os.environ["GROQ_API_KEY"] = "your-groq-api-key"  # ← Replace with your key

# 2. Initialize LLM
llm = ChatGroq(model="llama3-70b-8192", temperature=0.7)

# 3. Define the state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    log: list
    word_count: int

# 4. Node: Chat with LLM
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": response}

# 5. Node: Convert message content to UPPERCASE
def to_uppercase(state: State):
    new_messages = []
    for msg in state["messages"]:
        msg.content = msg.content.upper()
        new_messages.append(msg)
    return {"messages": new_messages}

# 6. Node: Log all messages
def logger(state: State):
    logs = [msg.content for msg in state["messages"]]
    return {"log": logs, "messages": state["messages"]}

# 7. Node: Count words in latest message
def counting(state: State):
    latest_msg = state["messages"][-1]
    content = latest_msg.content
    word_count = len(content.split())
    return {
        "messages": state["messages"],
        "log": state["log"],
        "word_count": word_count
    }

# 8. Build the graph
workflow = StateGraph(State)
workflow.add_node("chat", chatbot)
workflow.add_node("uppercase", to_uppercase)
workflow.add_node("log", logger)
workflow.add_node("count", counting)

workflow.set_entry_point("chat")
workflow.add_edge("chat", "uppercase")
workflow.add_edge("uppercase", "log")
workflow.add_edge("log", "count")
workflow.add_edge("count", END)

# 9. Compile the graph
graph = workflow.compile()

# 10. Run the graph
initial_state = {
    "messages": [{"role": "user", "content": "What is artificial intelligence?"}],
    "log": [],
    "word_count": 0
}

final_state = graph.invoke(initial_state)

# 11. Show results
print("\n🤖 Final AI Response (UPPERCASE):")
for msg in final_state["messages"]:
    print(f"{msg.type}: {msg.content}")

print("\n📝 Log of Messages:")
for log in final_state["log"]:
    print(log)

print("\n🔢 Word Count in Final Message:")
print(final_state["word_count"])
