from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load PDF
loader = PyPDFLoader("C:\\test_git\\IIT-GEN_AI---94392\\Day08\\fake-resumes\\resume-001.pdf")
docs = loader.load()

# Inspect raw pages
for page in docs:
    print(page.page_content[:200])
    print(page.metadata)

# Chunk the documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(docs)

# Inspect chunks
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}")
    print("Metadata:", chunk.metadata)
    print("Content:", chunk.page_content[:200])
