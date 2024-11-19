from fastapi import FastAPI
from fastapi.responses import JSONResponse
from rag import get_answer_and_docs
from qdrant import upload_website
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware # type: ignore

app = FastAPI(
    title="RAG Application",
    description="RAG Application using ReactJS, RemixJS, and FastAPI",
    version="1.0.0",
)


origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebsiteRequest(BaseModel): website_url: str
class Message(BaseModel): message: str

@app.post("/ask_question", description="Chat about the website")
async def root(question: Message):
    try:
        question_text = question.message
        response = get_answer_and_docs(question_text)
        response_content = {
            "question": question_text,
            "answer": response["answer"],
            "documents": [doc.dict() for doc in response["context"]]
        }
        return JSONResponse(content=response_content, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.post("/index_website", description="Index the website")
async def root(request: WebsiteRequest):
    try:
        response = upload_website(request.website_url)
        if "error" in response:
            return JSONResponse(content=response, status_code=500)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    