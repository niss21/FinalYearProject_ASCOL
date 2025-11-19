from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from vectorstore_loader import load_vectorstore
import time

def create_qa_chain(debug=False):
    """Create a high-performance RAG QA chain with local Phi-mini via Ollama."""
    retriever = load_vectorstore(top_k=3)

    if debug:
        print("🔍 Retriever loaded:", retriever)

    # Optimized local LLM
    llm = Ollama(
        model="phi3:mini",
        num_ctx=2048,
        temperature=0.1,
        mirostat=0
    )

    # Prompt optimized for RAG (stateless + no follow-up questions)
    from langchain.prompts import PromptTemplate

    prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a trekking and tourism assistant. "
        "Answer the question using the context below, responding concisely in Markdown format.\n\n"
        "If the question asks about trek details (e.g., duration, budget, permit, itinerary), "
        "list only the relevant details clearly in Markdown.\n"
        "Otherwise, write a short factual answer in 1–2 paragraphs.\n\n"
        "Context:\n{context}\n\n"
        "Question:\n{question}\n\n"
        "### Answer:"
    )
)



    # Create retrieval-augmented QA chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template},
        return_source_documents=True if debug else False,  # show docs if debugging
    )

    if debug:
        print("✅ RAG pipeline ready with Phi-mini.")

    return chain


def run_query(chain, query, debug=False):
    """Helper to run and debug a query."""
    start = time.time()
    result = chain.invoke({"query": query})
    end = time.time()

    print("\n🧭 Question:", query)
    print("\n💬 Answer:\n", result["result"] if isinstance(result, dict) else result)

    if debug and "source_documents" in result:
        print("\n📚 Retrieved Contexts:")
        for i, doc in enumerate(result["source_documents"], 1):
            print(f"\n--- Document {i} ---\n{doc.page_content[:500]}\n")

    print(f"\n⏱️ Response time: {end - start:.2f}s")
