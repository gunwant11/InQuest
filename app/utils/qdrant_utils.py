from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import Qdrant
from app.config import settings
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

def save_to_qdrant(file_path: str, user_id: str, session_id: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200, separators=["\n\n", "\n", "."])
    splits = text_splitter.split_documents(pages)

    for page in splits:
        page.metadata["id"] = user_id
    
    qdrant = Qdrant.from_documents(
        splits,
        embeddings,
        url=settings.QDRANT_URL,
        prefer_grpc=True,
        force_recreate=True,
        collection_name=f"resume_{session_id}",
    )
    print("Saved to Qdrant")
