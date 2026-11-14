import os
from dotenv import load_dotenv
import numpy
import ollama
import json

load_dotenv()
ollama_host = os.getenv("host")
model_name = os.getenv("MODE")

client = ollama.Client(host=ollama_host)

Embed_model = os.getenv("EMBED_MODEL")
KB_FOLDER = os.getenv("KB_FOLDER")
VECTOR_STORE_FILE = os.getenv("VECTOR_STORE_FILE")
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
def add_embeddings_to_documents(chunks):
    for chunk in chunks:
        vector = get_embeddings(chunk["text"])[0]
        chunk["vector"] = vector
        
    return chunks

# Search for the most similar document to the query
def search(query, chunks, top_k=3):
    query_vector = get_embeddings([query])[0]
    similarities = []
    
    for chunk in chunks:
        similarity = cosine_similarity(query_vector, chunk["vector"])
        similarities.append({
            "score": float(similarity),
            "source": chunk["source"],  # Pulls the filename
            "text": chunk["text"], 
            "size": len(chunk["text"])
        })
    
    # Sort by similarity in descending order
    similarities.sort(key=lambda x: x["score"], reverse=True)
    
    # Return the top_k most similar documents
    return similarities[:top_k]

# Testing the similarity search
def test_similarity_search(user_query, chunks, top_k=3):
    print("User query:", user_query)
    results = search(user_query, chunks, top_k)
    print(f"Top {top_k} results for query: '{user_query}'")
    for i, result in enumerate(results):
        print(f"Rank {i+1}:")
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Size: {result['size']}")
        print (f"Text: {result['text'][:200]}...")  # Print first 200 characters
        print("-" * 40)
        
        
        
def chunk_document(document):
    chunks = []
    chunk_id = 0
    for part in document["text"].split("\n\n"):  # Split by double newlines
        if part.strip():  # Avoid empty chunks
            chunks.append({
                "text": part.strip(),
                "source": document["source"],
                "chunk_id": chunk_id
            
            }) 
            chunk_id += 1
    
    return chunks

def create_chunks():
    documents = load_documents_from_folder()
    chunks = []
    for doc in documents:
       chunks.extend(chunk_document(doc))
       
    return chunks      


def save_vector_store(chunks):  
    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)
    
  
def load_vector_store():
    with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
        
        
        
          
# Let's start testing
chunks = []

if os.path.exists(VECTOR_STORE_FILE):
    print(f"Loading vector store from {VECTOR_STORE_FILE}...")
    chunks = load_vector_store()
    print(f"Loaded {len(chunks)} chunks from vector store file {VECTOR_STORE_FILE}.")

else:
    chunks = create_chunks()
    chunks = add_embeddings_to_documents(chunks)
    save_vector_store(chunks)
    print(f"Created and saved vector store with {len(chunks)} chunks to {VECTOR_STORE_FILE}.")

print(f"We embedded {len(chunks)} chunks from Knowledge base")

user_query = "What are benefits of maternity leave?"
test_similarity_search(user_query, chunks, top_k=3)
