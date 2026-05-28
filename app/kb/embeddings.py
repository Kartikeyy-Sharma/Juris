from sentence_transformers import SentenceTransformer


class LegalEmbedder:

    def __init__(self):

        # load embedding model

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def generate_embedding(self, text: str):

        # Generating embedding vector for legal test

        embedding = self.model.encode(text)

        return embedding.tolist()