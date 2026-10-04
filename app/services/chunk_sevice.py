def chunk_text(
  text: str,
  chunk_size: int = 1200,
  overlap: int = 200
) -> list[str]:

  paragraphs = [
    paragraph.strip()
    for paragraph in text.split("\n\n")
    if paragraph.strip()
  ]

  chunks = []
  current_chunk = ""

  for paragraph in paragraphs:

    # If adding this paragraph keeps us under the limit i.e 1200
    if len(current_chunk) + len(paragraph) <= chunk_size:
      current_chunk += paragraph + "\n\n"
    else:
      if current_chunk.strip():
        chunks.append(current_chunk.strip())

      # Start the next chunk
      current_chunk = paragraph + "\n\n"

  # Add remaining text
  if current_chunk.strip():
    chunks.append(current_chunk.strip())

  return chunks

def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1200
) -> list[dict]: 

  chunks = []
  chunk_index = 0

  for page in pages:

    text = page["text"]
    page_number = page["page_number"]

    start = 0

    while start < len(text):
      end = start + chunk_size
      chunk = text[start:end].strip()

      if chunk:
        chunks.append({
            "chunk_index": chunk_index,
            "page_number": page_number,
            "content": chunk
        })
        chunk_index += 1

      start = end

  return chunks