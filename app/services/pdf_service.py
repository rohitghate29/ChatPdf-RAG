import pymupdf

def extract_pages(file_path: str) -> list[dict]:
  document = pymupdf.open(file_path)

  pages = []

  for page_number, page in enumerate(document, start=1):
    text = page.get_text().strip()

    if text:
      pages.append({
        "page_number": page_number,
        "text": text
      })

  document.close()

  return pages