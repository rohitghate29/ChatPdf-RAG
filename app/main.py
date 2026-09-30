from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from sqlalchemy import text

from app.database import engine

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
def database_health():
  with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    return {
      "database": result.scalar()
    }