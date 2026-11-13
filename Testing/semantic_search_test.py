import os
import sys
import numpy

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
def get_embeddings(input_texts):
    response = client.embed(
        model=os.getenv("EMBED_MODEL"),
        input=input_texts
    )
    return response.embeddings

def cosine_similarity(A, B):
    dot_product = numpy.dot(A, B)
    norm_A = numpy.linalg.norm(A)
    norm_B = numpy.linalg.norm(B)
    return dot_product / (norm_A * norm_B)


text1 = "Python is a programming language."
text2 = "Java is a programming language."
text3 = "Python is a snake."
text4 = "I love programming in Python."
text5 = "I love apple."


embedding1 = get_embeddings([text1])[0]
embedding2 = get_embeddings([text2])[0]
embedding3 = get_embeddings([text3])[0]
embedding4 = get_embeddings([text4])[0]
embedding5 = get_embeddings([text5])[0]

similarity_1_2 = cosine_similarity(embedding1, embedding2)
similarity_1_3 = cosine_similarity(embedding1, embedding3)
similarity_1_4 = cosine_similarity(embedding1, embedding4)
similarity_1_5 = cosine_similarity(embedding1, embedding5)

print(f"Similarity between '{text1}' and '{text2}': {similarity_1_2:.4f}")
print(f"Similarity between '{text1}' and '{text5}': {similarity_1_5:.4f}")

