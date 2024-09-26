import ollama
import time

role = 'user'
content = 'Can you write a story for a kid about princesses and aliens in 2024? It needs to be long enough to last 10 minutes'

t0 = time.time()
response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": role,
            "content": content,
        },
    ],
)
t1 = time.time()

reply = response["message"]["content"]
print(reply)

print(f'\r\nRole: {role}\r\nContent: {content}')
print(f'Generated {len(reply.split())} words in {(t1-t0):.2f} seconds, or {len(reply.split())/(t1-t0):.0f} tokens per second.')
