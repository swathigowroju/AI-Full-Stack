from groq import Groq
from colorama import init, Fore

client = Groq(api_key="GROQ_API_KEY")

# This list stores the entire conversation
messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

print("AI Chatbot ready! Type your question. Type quit to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
      model="llama-3.3-70b-versatile", messages=messages)

    reply = response.choices[0].message.content
    print( f"AI: {reply}")

    messages.append({"role": "assistant", "content": reply})
   
