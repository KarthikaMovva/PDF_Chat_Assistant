import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build_index(self, embeddings, chunks):
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype("float32"))
        self.chunks = chunks

    def search(self, query_embedding, top_k=3):
        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"),
            top_k
        )

        results = [self.chunks[i] for i in indices[0]]
        return results