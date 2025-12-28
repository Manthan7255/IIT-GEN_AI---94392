from langchain_text_splitters import RecursiveCharacterTextSplitter

raw_text = """
Soccer players train daily to improve stamina, strength, and technique.
Training includes running drills, passing exercises, shooting practice,
and tactical team sessions. Professional players also focus on diet and recovery.
"""

# Recursive chunking (recommended in the PDF)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_text(raw_text)

# Inspect chunks
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}:\n{chunk}\n")
