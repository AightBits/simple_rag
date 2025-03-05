import sys
import chromadb
import requests
from sentence_transformers import SentenceTransformer

# Constants for easy modification
DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "BAAI/bge-large-en"  # Upgraded model for better retrieval
OPENAI_API_URL = "http://localhost:5000/v1/chat/completions"  # Example local model endpoint
OPENAI_API_KEY = ""  # Set API key if required
OPENAI_MODEL = "your-local-model-name"  # Example: "mistral" or "llama-2-13b-chat"
RELEVANCE_THRESHOLD = 0.5  # Higher threshold to allow relevant matches
TOP_N_RESULTS = 5  # Maximum number of most relevant documents to retrieve

# Ensure the user provides a project name
if len(sys.argv) < 2:
    print("Usage: python infer.py <project_name>")
    sys.exit(1)

project_name = sys.argv[1]

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=project_name)

# Load the embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

def query_llm(context, question):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"} if OPENAI_API_KEY else {"Content-Type": "application/json
"}
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are an AI assistant using retrieved documents to answer questions."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    }
    response = requests.post(OPENAI_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

print("Inference session started. Type your query below.")
while True:
    query = input("\nQuery (or type 'exit' to quit): ")
    if query.lower() == "exit":
        break

    query_embedding = model.encode([query], normalize_embeddings=True)[0].tolist()
    stored_docs = collection.count()  # Get number of stored documents
    n_results = stored_docs  # Retrieve up to stored_docs (but filter after)

    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    # Debugging: Print retrieved distances
    print("\nRetrieved Documents & Distances:")
    for doc_id, metadata, distance in zip(results["ids"][0], results["metadatas"][0], results["distances"][0]):
        print(f"- {doc_id}: Distance {distance}")

    # Apply relevance filtering based on the updated threshold
    relevant_docs = [metadata["text"] for metadata, distance in zip(results["metadatas"][0], results["distances"][0]) if distance < RELEVANCE_THRESHOLD]

    # Limit to top N most relevant documents
    retrieved_docs = "\n".join(relevant_docs[:TOP_N_RESULTS]) if relevant_docs else "No relevant documents found."
    response = query_llm(retrieved_docs, query)
    print("\nAI Response:")
    print(response)
