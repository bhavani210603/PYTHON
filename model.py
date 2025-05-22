from groq import Groq

# Directly set your API key here
set = Groq(api_key="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")


while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye","exit", "quit"]:
        print("Goodbye!")
        break

    response = set.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful and friendly assistant."},
            {"role": "user", "content": user_input},
        ],
    )

    reply = response.choices[0].message.content
    print(f"Assisant: {reply}\n")
