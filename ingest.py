import sys
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Constants for easy modification
DB_PATH = "./chroma_db"
PROJECTS_DIR = "./projects"
EMBEDDING_MODEL = "BAAI/bge-large-en"  # Upgraded model for better retrieval

# Ensure the user provides a project name
if len(sys.argv) < 2:
    print("Usage: python ingest.py <project_name>")
    sys.exit(1)

project_name = sys.argv[1]
project_data_path = os.path.join(PROJECTS_DIR, project_name)

client = chromadb.PersistentClient(path=DB_PATH)

# Forcefully delete the existing collection to reset dimensionality
try:
    client.delete_collection(project_name)
    print(f"Deleted existing collection for project: {project_name} to reset dimensions.")
except Exception:
    print(f"No existing collection found for project: {project_name}, creating a new one.")

collection = client.get_or_create_collection(name=project_name)

# Load the upgraded embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

if not os.path.exists(project_data_path):
    print(f"Project directory '{project_data_path}' not found. Please add text files to ingest.")
    sys.exit(1)

# Process text files
for filename in os.listdir(project_data_path):
    file_path = os.path.join(project_data_path, filename)

    if filename.endswith(".txt"):
        print(f"Processing file: {filename}")  # Debug: Print filename

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            print(f"File content (first 100 chars): {text[:100]}...")  # Debug: Print some text

            embedding = model.encode([text], normalize_embeddings=True)[0].tolist()  # Normalize for cosine similarity
            print(f"Embedding length: {len(embedding)}")  # Debug: Print embedding size

            # Ensure unique IDs
            doc_id = f"{project_name}_{filename}"

            collection.add(ids=[doc_id], embeddings=[embedding], metadatas=[{"text": text}])
            print(f"Ingested {filename} successfully with ID: {doc_id}.")

print("Ingestion complete.")
