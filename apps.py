from flask import Flask, render_template, request, session
from groq import Groq
import time
#import uuid to generate secret key 

app = Flask(__name__)
app.secret_key = 'chatbot'  # Required for session

# Set API to Groq
set = Groq(api_key="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")

# Initialize chat history in session
def init_chat_history():
    if 'chat_history' not in session:
        session['chat_history'] = []


@app.route("/", methods=["GET", "POST"])
def index():
    init_chat_history()
    
    if request.method == "POST":
        user_input = request.form["user_input"]
        
        # Add user message to history
        session['chat_history'].append({
            'sender': 'user',
            'message': user_input
        })
        
        # Get assistant reply
        time.sleep(20)  
        response = set.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0.5,
            top_p=0.4,
            messages=[
                {"role": "system", "content": "You are a helpful and friendly assistant."},
                {"role": "user", "content": user_input},
            ],
        )
        reply = response.choices[0].message.content
        
        # Add assistant reply to history
        session['chat_history'].append({
            'sender': 'assistant',
            'message': reply,
        })
        
        # Save the session
        session.modified = True
        
        return render_template("index.html", chat_history=session['chat_history'])
    
    return render_template("index.html", chat_history=session['chat_history'])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)