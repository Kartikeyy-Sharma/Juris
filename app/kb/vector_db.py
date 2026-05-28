import os
import uuid
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

load_dotenv()


class QdrantVectorStore:

    def __init__(self):

        self.client          = QdrantClient(host="localhost", port=6333)
        self.openai          = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.collection_name = "legal_knowledge_base"

    def create_collection(self):

        existing = [
            c.name for c in self.client.get_collections().collections
        ]

        if self.collection_name not in existing:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,               # text-embedding-3-small
                    distance=Distance.COSINE
                )
            )
            print(f"[QDRANT] Collection created: {self.collection_name}")

        else:
            print(f"[QDRANT] Collection already exists: {self.collection_name}")

    def _embed(self, text: str) -> list[float]:

        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    def insert_chunks(self, chunks: list[dict]):
        """
        Takes chunks list directly from AdaptiveChunking output.
        Each chunk: { chunk_type, text, metadata }
        """

        print(f"\n[QDRANT] Inserting {len(chunks)} chunks...")

        points = []

        for i, chunk in enumerate(chunks):

            text     = chunk["text"]
            metadata = chunk["metadata"]
            vector   = self._embed(text)

            point = PointStruct(
                id      = i + 1,           # integer id for qdrant
                vector  = vector,
                payload = {
                    "text":       text,
                    "chunk_type": chunk["chunk_type"],
                    **metadata             # flat — all metadata fields at top level
                }
            )

            points.append(point)

            if (i + 1) % 10 == 0:
                print(f"[QDRANT] Embedded {i + 1}/{len(chunks)}")

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"[QDRANT] Done — {len(chunks)} chunks stored")

    def search(self, query: str, top_k: int = 5) -> list[dict]:

        query_vector = self._embed(query)

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        output = []

        for r in response.points:
            payload = r.payload or {}
            output.append({
                "score":      round(r.score, 4),
                "text":       payload.get("text", ""),
                "chunk_type": payload.get("chunk_type", ""),
                "metadata": {
                    "chunk_id":       payload.get("chunk_id"),
                    "act_name":       payload.get("act_name"),
                    "year":           payload.get("year"),
                    "jurisdiction":   payload.get("jurisdiction"),
                    "chapter_number": payload.get("chapter_number"),
                    "chapter_title":  payload.get("chapter_title"),
                    "section_number": payload.get("section_number"),
                    "section_title":  payload.get("section_title"),
                    "clause_id":      payload.get("clause_id"),
                    "clause_type":    payload.get("clause_type"),
                }
            })

        return output