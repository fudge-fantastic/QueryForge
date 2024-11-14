from fastapi import FastAPI
from fastapi.responses import JSONResponse
from rag import get_answer_and_docs
from qdrant import upload_website

app = FastAPI(
    title="RAG Application",
    description="RAG Application using ReactJS, RemixJS, and FastAPI",
    version="1.0.0",
) 

@app.post("/chat", description="Chat about the website")
async def root(question: str):
    try:
        response = get_answer_and_docs(question)
        response_content = {
            "question": question,
            "answer": response["answer"],
            "document": [doc.dict() for doc in response["context"]]
        }
        return JSONResponse(content=response_content, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.post("/indexing", description="Index the website")
async def root(website_url: str):
    try:
        upload_website(website_url)
        return JSONResponse(content={"message": "Website indexed successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
