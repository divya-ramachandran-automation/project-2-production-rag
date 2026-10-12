# Production RAG Assistant

A production-style Retrieval-Augmented Generation (RAG) application built with Python and OpenAI.

The application answers company-policy questions using retrieved documents, semantic vector search, cross-encoder reranking, context-aware prompts, conversation memory, and source citations.

## Features

- Document ingestion and text chunking with overlap
- Metadata-aware document storage
- OpenAI text embeddings
- Persistent ChromaDB vector storage
- Semantic retrieval and duplicate-chunk removal
- Cross-encoder reranking
- Context construction from relevant chunks
- LLM-based answer generation
- Source citations for generated answers
- Conversation memory within a running session
- Query rewriting for conversational follow-up questions
- Retrieval evaluation utilities
- Automated tests using pytest
- Error handling for retrieval and answer generation

## Architecture

### Document Ingestion Flow

```text
Policy Documents
       |
       v
Document Loading
       |
       v
Text + Metadata
       |
       v
Chunking with Overlap
       |
       v
Embedding Generation
       |
       v
ChromaDB Vector Store
```

### Query and Answer Flow

```text
User Question
       |
       v
Conversation Memory
       |
       v
Follow-up Query Rewriting
       |
       v
Question Embedding
       |
       v
Vector Search
       |
       v
Candidate Chunks
       |
       v
Duplicate Removal
       |
       v
Cross-Encoder Reranking
       |
       v
Relevant Context
       |
       v
Prompt Construction
       |
       v
OpenAI LLM
       |
       v
Answer + Source Citations
```

## Project Structure

```text
project-2-production-rag/
├── knowledge/          # Source policy documents
├── tests/              # Automated tests
├── app.py              # Application entry point
├── ingestion.py        # Document loading
├── chunking.py         # Text chunking
├── embeddings.py       # Embedding generation
├── vector_store.py     # ChromaDB operations
├── retrieval.py        # Search and duplicate removal
├── reranker.py         # Cross-encoder reranking
├── context_builder.py  # Relevant context construction
├── prompts.py          # Answer and query-rewriting prompts
├── llm.py              # OpenAI answer generation
├── memory.py           # In-session conversation memory
├── citations.py        # Source citation handling
├── evaluation.py       # Retrieval evaluation utilities
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
├── pytest.ini          # Pytest configuration
├── .env                # Local secrets; not committed
└── .gitignore          # Git exclusions
```

## Prerequisites

- Python 3.10 or compatible
- An OpenAI API key
- Internet access for OpenAI API calls and initial model downloads

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure the API key

Create a local `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholder with your own API key. Never commit `.env` or share your API key.

## Run the Application

From the project root, with the virtual environment activated:

```powershell
python app.py
```

Enter a company-policy question when prompted. Ask additional questions in the same session to use conversation history.

Type `exit` to end the session.

## Run Automated Tests

Run the complete test suite:

```powershell
pytest -v
```

The current test suite contains 10 tests covering document ingestion, chunking, reranking, and retrieval behavior.

## Important Notes

- Conversation memory is stored in process memory and resets when the application exits.
- The application requires a valid OpenAI API key for embedding and answer-generation calls.
- The cross-encoder may download model files on its first run.
- The ChromaDB directory contains generated local vector-store data and is excluded from Git.
- Answers depend on the available policy documents and retrieval quality. Always verify important policy decisions against authoritative company documentation.

## Technologies

- Python
- OpenAI API
- ChromaDB
- Sentence Transformers
- pytest
- python-dotenv

## Future Improvements

- Persistent conversation history
- More comprehensive retrieval evaluation
- Improved configuration and logging
- Additional integration and end-to-end tests
- Deployment as a web API or user interface
