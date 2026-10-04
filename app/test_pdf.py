from app.services import pdf_service

file_path = "uploads/cf60a3b7-39c5-4dcc-8331-284d326fa4e3.pdf"

text = pdf_service.extract_txt(file_path=file_path)

print(text[:500])