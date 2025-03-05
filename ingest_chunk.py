import sys
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Constants for easy modification
DB_PATH = "./chroma_db"
PROJECTS_DIR = "./projects"
EMBEDDING_MODEL = "BAAI/bge-large-en"  # Upgraded model for better retrieval

# Chunking parameters
CHUNK_SIZE = 500        # Maximum number of characters per chunk
CHUNK_OVERLAP = 100     # Number of characters to overlap between chunks

def chunk_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= len(text):
            break
        # Move start pointer with overlap
        start = end - chunk_overlap
    return chunks

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
        print(f"Processing file: {filename}")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            print(f"File content (first 100 chars): {text[:100]}...")

            # Chunk the text
            chunks = chunk_text(text)
            print(f"Created {len(chunks)} chunks from {filename}.")

            for idx, chunk in enumerate(chunks):
                # Create a unique ID for each chunk
                doc_id = f"{project_name}_{filename}_chunk{idx}"
                embedding = model.encode([chunk], normalize_embeddings=True)[0].tolist()
                collection.add(ids=[doc_id], embeddings=[embedding], metadatas=[{"text": chunk}])
                print(f"Ingested chunk {idx} of {filename} successfully with ID: {doc_id}.")

print("Ingestion complete.")
