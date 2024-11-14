import os
import dotenv
from operator import itemgetter
from qdrant import vector_store
from langchain_groq import ChatGroq
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


try:
    # With Ollama
    # model = OllamaLLM(model="llama2")
    # With Groq
    dotenv.load_dotenv()
    groq_api_key = os.environ.get("GROQ_API_KEY")
    model = ChatGroq(temperature=1.4, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
    if model: print("Model loaded successfully")
    else: print("No model found")
except Exception as e:
    print(f"Error while loading the model: {e}")

prompt_template = """
Answer the question based on the context, in a concise manner using bullets where applicable
Context: {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)
retriever = vector_store.as_retriever()

# Create chain
def create_chain():
    try:
        chain = (
            {
                "context": retriever.with_config(top_k=8),
                "question": RunnablePassthrough()
            } | RunnableParallel({
                "response": prompt | model,
                "context": itemgetter("context")
            })
        )
        print("Chain created")
        return chain
    except Exception as e:
        print(f"Eror while creating the chain: {e}")
        
def get_answer_and_docs(question: str):
    try: 
        chain = create_chain()
        response = chain.invoke(question)
        # Remove Suffix '.content' if using Ollama
        answer = response["response"].content
        context = response["context"]
        return {
            "answer": answer, 
            "context": context
        }
    except Exception as e:
        print(f"An erro occured in the get_answer_and_docs function: {e}")
    
# get_answer = get_answer_and_docs("What is the blog about and who is the author?")
# print(get_answer)