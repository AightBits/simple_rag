# simple_rag

## Description

An extremely basic Retrieval-Augmented Generation (RAG) example using a vector database to retrieve context from ingested text documents and augment a language model's responses. This project provides two ingestion methods:
- **Full Ingest** – stores entire documents.
- **Chunked Ingest** – splits documents into overlapping chunks to better isolate relevant content.

The inference script retrieves the most relevant text based on a query, attaches similarity scores, and sends the context to an LLM for generating a response. This example is designed to illustrate the basics of integrating external data into LLM responses.

## How It Works

1. **Document Ingestion:**
   - The system processes text files stored in `./projects/<project_name>/`.
   - Depending on the ingestion method, either entire documents or smaller overlapping chunks are stored in a vector database (`chroma_db`).
   - Each document or chunk is converted into an embedding using a transformer-based model and stored along with its text.

2. **Query and Retrieval:**
   - When a user submits a query, it is also converted into an embedding.
   - The system searches for the most relevant stored embeddings using cosine similarity.
   - Retrieved documents and their similarity scores are displayed.

3. **Context Augmentation and Response Generation:**
   - The most relevant retrieved text is added as context to the prompt sent to the LLM.
   - The LLM generates a response using the retrieved information, improving accuracy by grounding it in stored documents.

4. **Understanding the Output:**
   - **Retrieved Documents & Distances:**
     - Each query returns a list of the most relevant documents (or chunks) with a similarity distance score.
     - A lower distance means a stronger match between the query and the retrieved text.
   - **AI Response:**
     - The response is generated based on the retrieved documents.
     - If no highly relevant text is found, the model may respond with limited or uncertain information.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AightBits/simple_rag.git
   cd simple_rag
   ```

2. **Run the install script:**

   ```bash
   bash setup.sh
   ```

   This script will:
   - Create a Python virtual environment (`venv`).
   - Install dependencies listed in `requirements.txt`.
   - Create the necessary directories (`chroma_db` and `projects`).

## Getting Started

After installation, activate your environment and view usage instructions by sourcing the `start.sh` script:

```bash
source start.sh
```

The `start.sh` script provides clear instructions on how to use the examples below. **Note:** Use only one ingestion method per project.

## Usage

1. **Prepare Your Data:**
   - Create a project directory under `./projects` (for example, `./projects/test`).
   - Add your `.txt` files to this directory.

   Example files:
   ```plaintext
   projects/test/john.txt:
   John is a cool guy who lives in Connecticut and likes pizza.
   
   projects/test/sarah.txt:
   Sarah is John's girlfriend and likes horses.
   
   projects/test/humphry.txt:
   Humphry lives in London.
   ```

2. **Ingest Data:**
   Choose one ingestion method:
   - **Option A: Full Ingest (stores entire documents):**
     ```bash
     python ingest.py <project_name>
     ```
   - **Option B: Chunked Ingest (splits documents into overlapping chunks):**
     ```bash
     python ingest_chunk.py <project_name>
     ```

3. **Run Inference:**
   Start an interactive inference session with:
   ```bash
   python infer.py <project_name>
   ```
   In the session, type your query (or `exit` to quit). The system will display the retrieved documents with similarity distances and the AI-generated response.

## Example Session

```plaintext
$ python ingest.py test
Processing file: john.txt
Ingested john.txt successfully.
Processing file: sarah.txt
Ingested sarah.txt successfully.
Processing file: humphry.txt
Ingested humphry.txt successfully.
Ingestion complete.

$ python infer.py test
Inference session started. Type your query below.

Query (or type 'exit' to quit): What can you tell me about John?

Retrieved Documents & Distances:
- john.txt: Distance 0.418
- sarah.txt: Distance 0.477
- humphry.txt: Distance 0.553

AI Response:
John is a cool guy who lives in Connecticut and likes pizza.

Query (or type 'exit' to quit): Who does John know?

Retrieved Documents & Distances:
- john.txt: Distance 0.395
- sarah.txt: Distance 0.451
- humphry.txt: Distance 0.512

AI Response:
Based on the retrieved documents, it is stated that John lives in Connecticut and has a girlfriend named Sarah. Therefore, John knows Sarah.

Query (or type 'exit' to quit): What can you tell me about Humphry?

Retrieved Documents & Distances:
- humphry.txt: Distance 0.276
- john.txt: Distance 0.613
- sarah.txt: Distance 0.630

AI Response:
I don't have any additional information about Humphry beyond his living in London. If you could provide more context or details about Humphry, I'd be happy to try and help further!
```

## License

This project is licensed under the Apache License 2.0.
