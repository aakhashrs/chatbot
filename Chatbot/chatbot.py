import warnings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import json

# Suppress FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

def load_scraped_data():
    """Load scraped data from JSON file."""
    with open('utd_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def initialize_chatbot():
    """Initialize the chatbot with FAISS index and GPT-2 model"""
    # Load scraped data
    scraped_data = load_scraped_data()
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Load vector store
    vector_store = FAISS.load_local(
        "faiss_index", 
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    return scraped_data, vector_store

def get_response(query, scraped_data, vector_store=None):
    """Get a simple response from the chatbot based on the scraped data."""
    # Truncate the query to a maximum length of 1024 characters
    truncated_query = query[:1024].lower()
    print(f"Debug: Truncated query: '{truncated_query}'")  # Debugging output
    
    # Split query into words for better matching
    query_words = set(truncated_query.split())
    
    # Find the best matches in the scraped data
    matches = []
    for entry in scraped_data:
        # Check if 'content' exists and is a list
        if 'content' in entry and isinstance(entry['content'], list):
            for content_item in entry['content']:
                if isinstance(content_item, str):
                    content_lower = content_item.lower()
                    # Count matching words
                    matching_words = sum(1 for word in query_words if word in content_lower)
                    if matching_words > 0:
                        matches.append({
                            "content": content_item,
                            "url": entry.get('url', 'Unknown source'),
                            "score": matching_words
                        })
    
    # Sort matches by score and return top 3
    matches.sort(key=lambda x: x["score"], reverse=True)
    top_matches = matches[:3]
    
    if top_matches:
        response = {
            "answer": "\n\n".join(match["content"] for match in top_matches),
            "sources": list(set(match["url"] for match in top_matches))
        }
    else:
        response = {
            "answer": "I'm sorry, I couldn't find an answer to your question.",
            "sources": []
        }
    
    return response

if __name__ == "__main__":
    # Test the chatbot
    scraped_data, _ = initialize_chatbot()
    while True:
        query = input("\nAsk about UTD (or 'quit' to exit): ")
        if query.lower() in ['quit', 'exit']:
            break
        
        response = get_response(query, scraped_data)
        print("\nAnswer:", response["answer"])
        if response["sources"]:
            print("\nSource:", response["sources"][0])

# from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline
# from langchain_huggingface import HuggingFacePipeline
# from langchain.docstore.document import Document
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings

# warnings.filterwarnings("ignore", category=FutureWarning)

# DATA_PATH = "data/utd_data.json"
# INDEX_PATH = "data/faiss_index"

# def build_faiss_index(json_path=DATA_PATH, index_path=INDEX_PATH):
#     with open(json_path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     documents = [
#         Document(page_content=item["text"], metadata={"url": item.get("url", "")})
#         for item in data
#     ]

#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = FAISS.from_documents(documents, embeddings)
#     vectorstore.save_local(index_path)
#     print(f"✅ FAISS index built and saved at: {index_path}")

# def initialize_chatbot():
#     # Build FAISS index if not exists
#     if not os.path.exists(INDEX_PATH) or not os.path.exists(os.path.join(INDEX_PATH, "index.faiss")):
#         print("🔧 FAISS index not found. Building now...")
#         build_faiss_index()

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2",
#         model_kwargs={'device': 'cpu'}
#     )

#     vector_store = FAISS.load_local(
#         INDEX_PATH,
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

#     tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#     model = GPT2LMHeadModel.from_pretrained("gpt2")
#     pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
#     llm = HuggingFacePipeline(pipeline=pipe)

#     return vector_store, pipe

# def get_response(query, vector_store, pipe):
#     retriever = vector_store.as_retriever(search_kwargs={"k": 3})
#     docs = retriever.invoke(query)

#     if not docs:
#         return {
#             "answer": "I couldn't find relevant information.",
#             "sources": [],
#             "contact_info": []
#         }

#     context = "\n\n".join(doc.page_content[:750] for doc in docs)
#     prompt = f"Use the following context to answer the question.\n\n{context}\n\nQuestion: {query}\nAnswer:"

#     response_text = pipe(prompt, max_new_tokens=150, pad_token_id=50256)[0]["generated_text"]
#     answer = response_text.split("Answer:")[-1].strip()

#     sources = []
#     for doc in docs:
#         if doc.metadata:
#             source = doc.metadata.get("url") or doc.metadata.get("source") or doc.metadata.get("file_path")
#         else:
#             source = None
#         if not source:
#             source = doc.page_content[:60] + "..."
#         sources.append(source)

#     return {
#         "answer": answer,
#         "sources": sources,
#         "contact_info": []
#     }

# def main():
#     vector_store, pipe = initialize_chatbot()
#     while True:
#         query = input("\nAsk about UTD (or 'quit' to exit): ")
#         if query.lower() in ['quit', 'exit']:
#             break
#         response = get_response(query, vector_store, pipe)
#         print("\nAnswer:", response["answer"])
#         if response["sources"]:
#             print("\nSources:", response["sources"])

# if __name__ == "__main__":
#     main()
