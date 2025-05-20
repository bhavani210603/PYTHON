import os
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages

#set api key to os
os.environ["Groq_API_KEY"]="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"

#set llm model
llm=ChatGroq(model_name="Llama3-70b-8192",temperature=0.3)

#define state
class State(TypedDict):
    messages:Annotated[list,add_messages]

#define node
def chatbot(state:State):
    response = llm.invoke(state["messages"])  # Get the assistant's reply
    return {"messages": state["messages"] + [response]}  # Keep the conversation history

#build graph
workflow=StateGraph(State)
workflow.add_node("chat",chatbot)
workflow.add_edge("chat",END)
workflow.set_entry_point("chat")
workflow.set_finish_point("chat")

graph=workflow.compile()

messages=[{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_input=input("You :")

    if user_input.lower() in ['bye','quit','Thank You']:
        print("Okay, Bye see you later")
        break

    messages.append({"role":"user","content":user_input})

    state={"messages":messages}
    result=graph.invoke(state)

    messages=result["messages"]
    last_msg=messages[-1]

    print(f"{last_msg.type}:{last_msg.content}")



