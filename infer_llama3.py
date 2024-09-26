import ollama

response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": "Explain general relativity as if I were a kids.",
        },
    ],
)
print(response["message"]["content"])