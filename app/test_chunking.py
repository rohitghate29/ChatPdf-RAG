from app.services.pdf_service import extract_txt
from app.services.chunk_sevice import chunk_text

file_path = "uploads/cf60a3b7-39c5-4dcc-8331-284d326fa4e3.pdf"

text = extract_txt(file_path)

chunks = chunk_text(text)

print(f"Total characters: {len(text)}")
print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:5]):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)