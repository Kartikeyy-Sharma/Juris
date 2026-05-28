from app.kb.embeddings import LegalEmbedder


embedder = LegalEmbedder()

sample_text = """
Employee shall receive minimum wages.
"""

embedding = embedder.generate_embedding(
    sample_text
)

print(type(embedding))

print(len(embedding))

print(embedding[:10])