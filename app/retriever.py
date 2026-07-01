from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os


class SHLRetriever:

    def __init__(self, assessments):

        self.assessments = assessments

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.documents = [
            self.create_document(a)
            for a in assessments
        ]

        self.index = None
        self.embeddings = None

        self.load_or_build()

    # ----------------------------------------------------

    def load_or_build(self):

        index_path = "data/faiss.index"
        embedding_path = "data/embeddings.npy"

        if os.path.exists(index_path) and os.path.exists(embedding_path):

            print("Loading pre-built FAISS index...")

            self.index = faiss.read_index(index_path)

            self.embeddings = np.load(
                embedding_path
            ).astype("float32")

            print(
                f"Loaded {self.index.ntotal} vectors."
            )

        else:

            print(
                "Pre-built index not found."
            )

            self.build_index()

    # ----------------------------------------------------
    def create_document(self, assessment):
        name = assessment.get("name", "")
        description = assessment.get("description", "")
        duration = assessment.get("duration", "")
        job_levels = assessment.get("job_levels_raw", "")
        languages = assessment.get("languages_raw", "")
        url = assessment.get("link", "")
        categories = ", ".join(
            assessment.get("keys", [])
        )
        searchable = f"""
Assessment Name:
{name}
Description:
{description}
Categories:
{categories}
Duration:
{duration}
Job Levels:
{job_levels}
Languages:
{languages}
URL:
{url}
Search Keywords:
{name}
{categories}
{description}
Assessment
Hiring
Recruitment
Knowledge Test
Personality Assessment
Cognitive Ability
Behavioral Assessment
Programming
Developer
Software Engineer
Java
Python
SQL
Leadership
Communication
Problem Solving
Critical Thinking
"""
        return searchable

    # ----------------------------------------------------

    def build_index(self):

        os.makedirs("data", exist_ok=True)

        print("Generating embeddings...")

        self.embeddings = self.model.encode(

            self.documents,

            convert_to_numpy=True,

            normalize_embeddings=True,

            show_progress_bar=True,

            batch_size=16

        ).astype("float32")

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(
            self.embeddings
        )

        faiss.write_index(
            self.index,
            "data/faiss.index"
        )

        np.save(
            "data/embeddings.npy",
            self.embeddings
        )

        print(
            f"Saved {len(self.documents)} embeddings."
        )

    # ----------------------------------------------------

    def format_context(
        self,
        assessments
    ):

        context = ""

        for i, assessment in enumerate(
            assessments,
            start=1
        ):

            context += f"""
Assessment {i}

Name:
{assessment.get("name")}

Description:
{assessment.get("description")}

Categories:
{", ".join(assessment.get("keys", []))}

Duration:
{assessment.get("duration")}

Job Levels:
{assessment.get("job_levels_raw")}

Languages:
{assessment.get("languages_raw")}

URL:
{assessment.get("link")}

----------------------------------------------------------
"""

        return context

    # ----------------------------------------------------

    def search(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        assessments = []

        seen = set()

        for idx in indices[0]:

            if idx < 0:
                continue

            assessment = self.assessments[idx]

            url = assessment.get(
                "link",
                ""
            )

            if url and url in seen:
                continue

            if url:
                seen.add(url)

            assessments.append(
                assessment
            )

        context = self.format_context(
            assessments
        )

        return assessments, context

    # ----------------------------------------------------

    def search_by_category(
        self,
        category,
        top_k=5
    ):

        return self.search(
            category,
            top_k
        )

    # ----------------------------------------------------

    def search_multiple(
        self,
        queries,
        top_k_each=3
    ):

        merged = []

        seen = set()

        for query in queries:

            assessments, _ = self.search(
                query,
                top_k_each
            )

            for assessment in assessments:

                url = assessment.get(
                    "link",
                    ""
                )

                if url and url in seen:
                    continue

                if url:
                    seen.add(url)

                merged.append(
                    assessment
                )

        merged = merged[:10]

        context = self.format_context(
            merged
        )

        return merged, context

    # ----------------------------------------------------

    def compare(
        self,
        assessment_names
    ):
        """
        Compare assessments using exact match first,
        then semantic search as fallback.
        """

        results = []

        seen = set()

        for name in assessment_names:

            # -----------------------------
            # Exact match
            # -----------------------------

            exact = None

            for assessment in self.assessments:

                if assessment.get(
                    "name",
                    ""
                ).lower() == name.lower():

                    exact = assessment

                    break

            if exact:

                url = exact.get(
                    "link",
                    ""
                )

                if url and url in seen:
                    continue

                if url:
                    seen.add(url)

                results.append(
                    exact
                )

                continue

            # -----------------------------
            # Semantic fallback
            # -----------------------------

            assessments, _ = self.search(
                name,
                top_k=1
            )

            for assessment in assessments:

                url = assessment.get(
                    "link",
                    ""
                )

                if url and url in seen:

                    continue

                if url:

                    seen.add(url)

                results.append(
                    assessment
                )

        return (
            results,
            self.format_context(
                results
            )
        )