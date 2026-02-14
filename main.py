from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from fastapi.responses import FileResponse
# -------- CONFIG --------




app = FastAPI(title="DocuQuery RAG API")

vectorstore = None
retriever = None

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

# -------- MODELS --------
class Question(BaseModel):
    question: str


# -------- ROUTES --------
@app.get("/health")
def health():
    return {"status": "running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vectorstore, retriever

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    return {"message": "Document uploaded and indexed successfully"}


@app.post("/ask")
def ask_question(data: Question):
    if retriever is None:
        return {"error": "Upload a document first"}

    docs = retriever.invoke(data.question)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {data.question}
    """

    response = llm.invoke(prompt)

    return {"answer": response.content}



@app.get("/")
def home():
    return FileResponse("home.html")

@app.get("/version")
def version():
    return {"version": "1.0"}