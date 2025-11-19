from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

PERSIST_DIR = "persist"

def load_vectorstore(top_k: int = 3):
    """Load the persisted Chroma vector DB with optimized HuggingFace embeddings."""
    print("✅ Loading existing Chroma vector store...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": top_k})
    return retriever
