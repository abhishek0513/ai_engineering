import os
from dotenv import load_dotenv
import ollama

load_dotenv()
ollama_host = os.getenv("host")
model_name = os.getenv("MODE")

client = ollama.Client(host=ollama_host)

stream = client.chat(
    model=model_name,
    messages=[{"role": "user", "content": "Explain what an API is in 100 words. No need to mention the number of words"}],
    tools= os.getenv("TOOLS"),
    stream=True,
)

full_response = ""

for chunk in stream:
    if not chunk.choices:
        continue
    
    piece = chunk.message.content
    if piece:
        print(piece, end="", flush=True)
        full_response += piece

print("\nFull response:")
print(full_response)
