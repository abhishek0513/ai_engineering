# standard library imports
import os
import sys
# Third-party imports
from dotenv import load_dotenv
import ollama
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Local modules
from tools import Tools, FUNCTION_NAME_TO_FUNCTION

load_dotenv()  # by default looks for .env file
ollama_host = os.getenv("host")
model_name = os.getenv("MODE")

client = ollama.Client(host=ollama_host)
response = client.embed(
    model=os.getenv("EMBED_MODEL"),
    input=["I am good engineer", "Software development in Java and Spring Boot."]
)

for i, embedding in enumerate(response.embeddings):
    print(len(embedding), "dimensions for input", i, ":", embedding[:3])


# print(response.embeddings[0])
# print()
# print(len(response.embeddings[0]))
# print(response.embeddings[1])
# print()
# print(len(response.embeddings[1]))