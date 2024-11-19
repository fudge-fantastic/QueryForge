# Run this one time only 
import os
import dotenv
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient, models
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import warnings
warnings.filterwarnings("ignore")

try:
    dotenv.load_dotenv()
    api_key = os.environ.get("QDRANT_API_KEY")
    url_key = os.environ.get("QDRANT_URL")
    collection_name = os.environ.get("QDRANT_COLLECTION_NAME")
    print("All API keys loaded successfully") 
except Exception as e:
    print(f"An error occured while loading environment variables: {e}")

try:
    client = QdrantClient(url=url_key, api_key=api_key)
    print("Connected to Qdrant")
except Exception as e:
    print(f"An error occured with connecting to Qdrant: {e}")

try:
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    print("HuggingFace embeddings model loaded successfully.")
except Exception as e:
    print(f"Error loading HuggingFace embeddings model: {e}")

vector_store = Qdrant(client=client, collection_name=collection_name, embeddings=embeddings_model)

# Creating collection
def create_collection(collection_name):
    try:    
        if collection_name in [collection.name for collection in client.get_collections().collections]:
            print(f"Collection {collection_name} already exists. Skipping creation.")
        else:
            # Create the collection if it doesn't exist
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=768,
                    distance=models.Distance.COSINE
                )
            )
            
            print(f"Collection {collection_name} created")
    except Exception as e:
        print(f"An error occured while creating collection: {e}")
    
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20, length_function=len)
    
# Upload website to collection
def upload_website(website_url: str):
    try:
        loader = WebBaseLoader(website_url)
        docs = loader.load_and_split(text_splitter)
        print(f"Successfully loaded {len(docs)} documents from {website_url}")

        for i in docs: i.metadata = {"source": website_url}
        try:
            vector_store.add_documents(documents=docs)
            print(f"Successfully added {len(docs)} documents to collection {collection_name}")
            return {"message": f"Successfully indexed {len(docs)} documents from {website_url}"}
        except Exception as e:
            error_message = f"An error occurred while adding documents to the collection: {e}"
            print(error_message)
            return {"error": error_message}
    except Exception as e:
        error_message = f"An error occurred while loading the website: {e}"
        print(error_message)
        return {"error": error_message}


# create_collection(collection_name)
# upload_website("https://research.ibm.com/blog/what-is-generative-AI")