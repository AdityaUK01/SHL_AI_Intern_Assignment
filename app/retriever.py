import os
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SHLRetriever:

    def __init__(self, assessments):

        self.assessments = assessments

        self.documents = [
            self.create_document(a)
            for a in assessments
        ]

        self.vectorizer = None
        self.document_vectors = None

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

Behavioral Assessment

Cognitive Ability

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

        print("Building TF-IDF index...")

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.document_vectors = self.vectorizer.fit_transform(
            self.documents
        )

        print(
            f"Indexed {len(self.documents)} assessments."
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

        query_vector = self.vectorizer.transform(
            [query]
        )

        scores = cosine_similarity(
            query_vector,
            self.document_vectors
        ).flatten()

        ranked = np.argsort(scores)[::-1]

        assessments = []

        seen = set()

        for idx in ranked:

            if len(assessments) >= top_k:
                break

            if scores[idx] <= 0:
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

        return (
            assessments,
            self.format_context(
                assessments
            )
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

        return (
            merged,
            self.format_context(
                merged
            )
        )

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

    def compare(
        self,
        assessment_names
    ):
        """
        Compare assessments using exact match first,
        then TF-IDF similarity as fallback.
        """

        results = []

        seen = set()

        for name in assessment_names:

            # -----------------------
            # Exact match
            # -----------------------

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

                if url and url not in seen:

                    seen.add(url)

                    results.append(exact)

                continue

            # -----------------------
            # TF-IDF fallback
            # -----------------------

            assessments, _ = self.search(
                name,
                top_k=1
            )

            for assessment in assessments:

                url = assessment.get(
                    "link",
                    ""
                )

                if url and url not in seen:

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