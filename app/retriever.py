from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class SHLRetriever:

    def __init__(self, assessments):

        self.assessments = assessments

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.documents = []
        self.embeddings = None
        self.index = None

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

        print("Creating searchable documents...")

        self.documents = [
            self.create_document(a)
            for a in self.assessments
        ]

        print("Generating embeddings...")
        self.embeddings = self.model.encode(
            self.documents,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        self.embeddings = np.array(
            self.embeddings
        ).astype("float32")

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(
            self.embeddings
        )

        print(
            f"FAISS index built with {len(self.documents)} assessments!"
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
        )

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        assessments = []

        seen = set()

        for idx in indices[0]:

            assessment = self.assessments[idx]

            url = assessment.get(
                "link",
                ""
            )

            if url in seen:
                continue

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
        """
        Search assessments using a specific category
        such as:
        - personality assessment
        - cognitive ability
        - programming
        """

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
        """
        Search multiple queries and merge results.

        Example:
        [
            "java developer",
            "personality assessment"
        ]
        """

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

                if url in seen:
                    continue

                seen.add(url)

                merged.append(
                    assessment
                )

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
        Retrieve assessments for comparison.
        Uses exact-name matching first, then falls back to semantic search.
        """

        results = []
        seen = set()

        for name in assessment_names:

            exact = None

            for assessment in self.assessments:
                if assessment.get("name", "").lower() == name.lower():
                    exact = assessment
                    break

            if exact:
                url = exact.get("link", "")
                if url not in seen:
                    seen.add(url)
                    results.append(exact)
                continue

            assessments, _ = self.search(name, top_k=1)

            for assessment in assessments:
                url = assessment.get("link", "")
                if url not in seen:
                    seen.add(url)
                    results.append(assessment)

        return results, self.format_context(results)
