from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
ak=os.getenv("GOOGLE_API_KEY")
tk=os.getenv("TOKEN")
pdf_path="/Users/shaiv/Documents/langraph/langGraph/The_Psychology_of_Money.pdf"

#loading
loader= PyPDFLoader(pdf_path)
docs=loader.load()

#splitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(docs)

#embedding
embeds = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = [doc.page_content for doc in chunks]
metadatas = [doc.metadata for doc in chunks]

#storing in vector data base
vectorstore = FAISS.from_texts(
    texts=texts,
    embedding=embeds,
    metadatas=metadatas
)

#retriver
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

@tool
def rag_search(query: str) -> str:
    """
    Retrieve relevant information from the pdf document.
    Use this tool when the user asks factual / conceptual questions
    that might be answered from the stored documents.
    """
    docs = retriever.invoke(query)
    return "\n\n".join(d.page_content for d in docs)
