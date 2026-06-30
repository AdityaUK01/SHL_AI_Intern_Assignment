from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class SHLRetriever:

    def __init__(self, assessments):
        self.assessments = assessments

        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.documents = []
        self.index = None

        self.build_index()

    def create_document(self, assessment):

        return f"""
Name: {assessment.get("name", "")}

Description:
{assessment.get("description", "")}

Job Levels:
{assessment.get("job_levels_raw", "")}

Languages:
{assessment.get("languages_raw", "")}

Duration:
{assessment.get("duration", "")}

Categories:
{", ".join(assessment.get("keys", []))}
"""

    def build_index(self):

        self.documents = [
            self.create_document(a)
            for a in self.assessments
        ]

        embeddings = self.model.encode(
            self.documents,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        print("FAISS index built!")

    def search(self, query, top_k=5):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        assessments = []
        context = ""

        for i, idx in enumerate(indices[0], start=1):

            assessment = self.assessments[idx]

            assessments.append(assessment)

            context += f"""
Assessment {i}

Name: {assessment.get("name")}

Description:
{assessment.get("description")}

Duration:
{assessment.get("duration")}

Job Levels:
{assessment.get("job_levels_raw")}

Languages:
{assessment.get("languages_raw")}

Categories:
{", ".join(assessment.get("keys", []))}

URL:
{assessment.get("link")}

------------------------------------------------
"""

        return assessments, context