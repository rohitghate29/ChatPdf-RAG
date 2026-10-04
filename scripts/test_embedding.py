from app.services.embedding_service import generate_embeddings


texts = [
    "Customers can receive their money back within 30 days.",
    "The company offers technical support from Monday to Friday.",
    "Orders can be cancelled before they are shipped.",
]

embeddings = generate_embeddings(texts)

print("Number of embeddings:", len(embeddings))

for i, embedding in enumerate(embeddings):
    print(f"Embedding {i}: {len(embedding)} dimensions")