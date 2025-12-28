import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# Sample text
raw_text = """
Soccer players train daily to improve stamina, strength, and technique.
Training includes running drills, passing exercises, shooting practice,
and tactical team sessions. Professional players also focus on diet and recovery.
"""

# Embedding model
embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_text(raw_text)

# Chroma client (auto-persistent)
client = chromadb.Client(
    Settings(
        persist_directory="./chroma_db",
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(name="demo")

embeddings = embed_model.embed_documents(chunks)

ids = [f"doc_{i}" for i in range(len(chunks))]
metadatas = [{"source": "example.txt", "chunk_id": i} for i in range(len(chunks))]

collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas
)

print("CREATE: Data inserted into ChromaDB")

