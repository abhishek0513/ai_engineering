import os
from dotenv import load_dotenv
import ollama
from tools import Tools

load_dotenv()
ollama_host = os.getenv("host")
model_name = os.getenv("MODE")

client = ollama.Client(host=ollama_host)

stream = client.chat(
    model=model_name,
    messages=[{"role": "user", "content": "Tell the weather of pune and delhi"}],
    tools= Tools,
    stream=True,
)

full_response = ""

for chunk in stream: 
    piece = chunk.message.content 
    if piece.tool_calls:
        print(piece.tool_calls, end="", flush=True)
        # print(piece, end="", flush=True)
        # full_response += piece
