from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pathlib import Path
import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Document, DocumentChunk
from app.services.pdf_service import extract_pages
from app.services.chunk_sevice import chunk_pages
from app.services.embedding_service import generate_embeddings

app = FastAPI(title="ChatPDF API")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def root():
  return {
    "message": "ChatPDF is running"
  }

@app.get("/health")
def health():
  return {
    "status": "healthy"
  }

@app.post("/document/upload")
async def upload_document(file: UploadFile = File(...)):

  # check file type
  if file.content_type != "application/pdf":
    raise HTTPException(
      status_code=400,
      detail="Only PDF files are allowed"
    )

  # 2. Generate unique document ID
  document_id = str(uuid.uuid4())

  # 3. create file path
  file_path = UPLOAD_DIR / f"{document_id}.pdf"

  # 4. save file
  contents = await file.read()
  file_path.write_bytes(contents)

  # 5. Return information
  return {
    "document_id": document_id,
    "filename": file.filename,
    "message": "PDF uploaded successfully"
  }

@app.get("/health/db")
def database_health(db: Session = Depends(get_db)):
  result = db.execute(text("SELECT 1"))

  return {
      "database": result.scalar()
  }


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1. Validate file type
    if file.content_type != "application/pdf":
      raise HTTPException(
          status_code=400,
          detail="Only PDF files are allowed"
      )

    # 2. Generate document ID
    document_id = uuid.uuid4()

    # 3. Create file path
    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    # 4. Read and save PDF
    contents = await file.read()
    file_path.write_bytes(contents)

    # 5. Create database record
    document = Document(
      id=document_id,
      filename=file.filename,
      file_path=str(file_path),
      file_size=len(contents),
      status="processing"
    )

    # 6. Save record to database
    db.add(document)
    db.commit()
    # db.refresh(document)

    # Extract pages
    pages = extract_pages(str(file_path))

    # create chunks
    chunks = chunk_pages(pages)

    texts = [chunk["content"] for chunk in chunks]

    embeddings = generate_embeddings(texts)

    # save chunks + embeddings
    for chunk, embedding in zip(chunks, embeddings):
      document_chunk = DocumentChunk(
        document_id=document_id,
        chunk_index=chunk["chunk_index"],
        content=chunk["content"],
        page_number=chunk["page_number"],
        embedding=embedding
      )

      db.add(document_chunk)

    # Mark doc as completed
    document.status = "completed"

    db.commit()

    return {
      "document_id": str(document_id),
      "filename": file.filename,
      "chunks_created": len(chunks),
      "status": document.status,
      "message": "PDF processed successfully"
    }