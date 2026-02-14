# DocuQuery RAG API

A FastAPI app that lets you upload PDFs and ask questions about them using retrieval-augmented generation (RAG). Documents are chunked, embedded with OpenAI, stored in FAISS, and answers are generated with GPT-3.5 using the retrieved context.

## Features

- **Upload PDF** – Index a document for question-answering
- **Ask** – Get answers based only on the uploaded document content
- **OpenAPI docs** – Interactive API at `/docs`

## Requirements

- Python 3.10+
- [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

### 1. Clone or navigate to the project

```bash
cd doc_query
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

**Option A – environment variable (recommended):**

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "your-api-key-here"
```

```bash
# Linux/macOS
export OPENAI_API_KEY="your-api-key-here"
```

**Option B – `.env` file (if you add python-dotenv):**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-api-key-here
```

## Run the app

```bash
uvicorn app:app --reload
```

- API: **http://127.0.0.1:8000**
- Interactive docs: **http://127.0.0.1:8000/docs**

## API

| Method | Endpoint   | Description                          |
|--------|------------|--------------------------------------|
| GET    | `/health`  | Health check                         |
| POST   | `/upload`  | Upload a PDF (form field: `file`)    |
| POST   | `/ask`     | Ask a question (body: `{"question": "..."}`) |

### Example flow

1. **Upload a PDF**  
   - In `/docs`, use **POST /upload** and attach a PDF file.

2. **Ask a question**  
   - Use **POST /ask** with JSON body, e.g.  
     `{"question": "What is the main topic of the document?"}`  
   - Response: `{"answer": "..."}`

You must upload a document before calling `/ask`; otherwise you’ll get an error.

## Tech stack

- **FastAPI** – Web framework
- **LangChain** – Document loading, splitting, retrieval
- **OpenAI** – Embeddings (`text-embedding-3-small`) and chat (`gpt-3.5-turbo`)
- **FAISS** – In-memory vector store
- **PyPDF** – PDF parsing

## License

Use and modify as you like.
