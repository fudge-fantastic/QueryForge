## RAG Application

### Install Python Dependencies
```shell
python -m venv venv
source venv/bin/activate
pip install langchain langchain_community qdrant-client fastapi uvicorn beautifulsoup4
pip install -U langchain-qdrant
pip install -U langchain-huggingface
pip install langchain-groq
```

### Run Application

```python
# main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="RAG Application",
    description="RAG Application using ReactJS, RemixJS, and FastAPI",
    version="1.0.0",
) 

@app.post("/", description="Demo Endpoint")
async def root(name: str):
    return JSONResponse(content={"message": "Hello " + name}, status_code=200)

```
```shell
uviorn main:app --reload
```

---

### Qdrant
__Ensure to create a cluster on Qdrant Cloud before proceeding.__

### [Ollama Setup + LangChain](https://python.langchain.com/docs/integrations/llms/ollama/), 
1. [Model EndPoints](https://github.com/ollama/ollama/blob/main/docs/api.md)
2. [Huggingface + Langchian](https://python.langchain.com/docs/integrations/text_embedding/huggingfacehub/)
3. [Groq + Langchain Setup](https://python.langchain.com/v0.1/docs/integrations/chat/groq/)
4. [Available models in Groq](https://console.groq.com/docs/models)

```shell
# To check if ollama is installed, 
ollama 
# To list the models YOU have
ollama list
```
```shell
# Try this on Thunder Client or Postman
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt":"I need recipe for chocolate fudge in JSON format",
  "stream":false,
  "format":"json"
}'
```

### Others
1. [WebBaseLoader](https://python.langchain.com/docs/integrations/document_loaders/web_base/) - This loader can be used to load all text from HTML webpages into a document format that we can use downstream. For more custom logic for loading webpages look at some child class examples such as IMSDbLoader, AZLyricsLoader, and CollegeConfidentialLoader. __If you don't want to worry about website crawling, bypassing JS-blocking sites, and data cleaning, consider using FireCrawlLoader or the faster option SpiderLoader.__

2. HTTP response [Status Code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) indicate whether a specific HTTP request has been successfully completed. Responses are grouped in five classes:
    - Informational responses (100 – 199)
    - Successful responses (200 – 299)
    - Redirection messages (300 – 399)
    - Client error responses (400 – 499)
    - Server error responses (500 – 599)


