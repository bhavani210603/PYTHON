import time
import sys
import random
from typing import TypedDict
from langgraph.graph import StateGraph, END

# State 
class GraphState(TypedDict):
    input: str
    intent: str
    reply: str
    chat_history: list[str]

# Intent and Reply 
USER_INTENTS = {
    "greeting": ["hi", "hello", "hey", "good morning"],
    "question": ["how", "what", "why", "where", "when"],
    "complaint": ["not working", "broken", "issue", "problem"],
    "farewell": ["bye", "goodbye", "see you", "take care"],
    "smalltalk": ["how are you", "what’s up", "tell me something"],
    "request_info": ["i need", "can you give", "please send"],
    "thanks": ["thanks", "thank you", "appreciate it"],
    "order_status": ["track", "order status", "where is my order"],
    "cancel_order": ["cancel", "stop my order"],
    "escalate": ["talk to human", "representative", "escalate"],
    "book_cinema_ticket":[
    "book a ticket", "cinema ticket", "movie ticket", "i want to see a movie"
]
}

REPLIES = {
    "greeting": ["Hey there! ", "Nice to see you. "],
    "question": ["Hmm, let me think… ", "Here's what I found: "],
    "complaint": ["Oh no, I'm really sorry to hear that. ", "Let me help you fix it. "],
    "farewell": ["Goodbye! ", "Take care. See you soon! "],
    "smalltalk": ["Haha, I'm doing well. ", "Just waiting to chat! "],
    "request_info": ["Of course, here’s the info you need: "],
    "thanks": ["You’re welcome! ", "Anytime. "],
    "order_status": ["Let me check your order… ", "It looks like it's on the way. "],
    "cancel_order": ["Got it. ", "I’ll start the cancellation process now. "],
    "escalate": ["Alright, connecting you to a human agent. ", "Please hold… "],
    "unknown": ["I'm not quite sure what you mean. ", "Can you say that differently? "],
    "book_cinema_ticket":["Sure!", "Which movie and what time would you like to book?"]
}

# --- Intent Detection ---
def detect_intent(user_input):
    for intent, keywords in USER_INTENTS.items():
        if any(kw in user_input.lower() for kw in keywords):
            return intent
    return "unknown"

# Simulated Typing Reply
def simulate_reply(replys, thinking=(1.5, 3.5),delay=(0.5, 1.2)):
    #Typing indicator (typing...)
    print("\ntyping", end="")
    for i in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True) #Forces the text to appear instantly, not wait for the buffer.
    time.sleep(random.uniform(*thinking))
    print("\r" + " " * 30 + "\r", end="")  # Clear the typing...


    #Simulate natural typing
    for reply in replys:
        for char in reply:
            sys.stdout.write(char)
            sys.stdout.flush()
        time.sleep(random.uniform(*delay))
    print()  # Final newline


# --- LangGraph Node Function ---
def reply_node(state: GraphState) -> GraphState:
    user_input = state["input"] #Gets the user's input
    history=state.get("chat_history",[])
    intent = detect_intent(user_input) #Detects the intent
    response = REPLIES[intent] #Looks up the matching reply in REPLIES
    simulate_reply(response)
    history.append(f"You: {user_input}")
    history.append(f"Keerthana: {' '.join(response)}")
    return {
        "input": user_input,
        "intent": intent,
        "reply": " ".join(response),
        "chat_history": history
    }

# --- LangGraph Setup ---
workflow = StateGraph(GraphState)
workflow.add_node("handle_input", reply_node) 
workflow.set_entry_point("handle_input")
workflow.set_finish_point("handle_input")
app = workflow.compile()


#  Run the Graph
if __name__ == "__main__":
    chat_history=[]
    user_text = input("You: ")
    state = {
            "input": user_text,
            "intent": "",
            "reply": "",
            "chat_history": chat_history
        }
    result = app.invoke(state)
    chat_history = result["chat_history"]