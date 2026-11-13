import os
from dotenv import load_dotenv
import numpy
import ollama

load_dotenv()
ollama_host = os.getenv("host")
model_name = os.getenv("MODE")

client = ollama.Client(host=ollama_host)

Embed_model = os.getenv("EMBED_MODEL")
KB_FOLDER = os.getenv("KB_FOLDER")

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

# Load the documents as dictionaries containing their text
def load_documents_from_folder(folder_path=KB_FOLDER):
    documents = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                # Store as a dictionary so we can attach vector and metadata
                documents.append({
                    "text": content,
                    "source": filename
                })
    return documents

# Add embedding to the documents correctly (extracting the 1D vector with [0])
def add_embeddings_to_documents(documents):
    for document in documents:
        vector = get_embeddings(document["text"])[0]
        document["vector"] = vector
        
    return documents

# Search for the most similar document to the query
def search(query, documents, top_k=3):
    query_vector = get_embeddings([query])[0]
    similarities = []
    
    for document in documents:
        similarity = cosine_similarity(query_vector, document["vector"])
        similarities.append({
            "score": float(similarity),
            "source": document["source"],  # Pulls the filename
            "text": document["text"], 
            "size": len(document["text"])
        })
    
    # Sort by similarity in descending order
    similarities.sort(key=lambda x: x["score"], reverse=True)
    
    # Return the top_k most similar documents
    return similarities[:top_k]

# Testing the similarity search
def test_similarity_search(user_query, documents, top_k=3):
    print("User query:", user_query)
    results = search(user_query, documents, top_k)
    print(f"Top {top_k} results for query: '{user_query}'")
    for i, result in enumerate(results):
        print(f"Rank {i+1}:")
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Size: {result['size']}")
        print("-" * 40)
        
# Let's start testing
documents = load_documents_from_folder()
documents = add_embeddings_to_documents(documents)

print(f"We embedded {len(documents)} documents")

user_query = "How many round of assesment are there ?"
test_similarity_search(user_query, documents, top_k=3)