class SHLEvaluator:

    def retrieval_score(
        self,
        recommendations,
        expected_keywords
    ):

        if not recommendations:
            return 0

        score = 0

        for assessment in recommendations:

            name = assessment["name"].lower()

            for keyword in expected_keywords:

                if keyword.lower() in name:
                    score += 1
                    break

        return round(
            score / len(expected_keywords),
            2
        )

    # ---------------------------------------

    def groundedness_score(
        self,
        reply,
        recommendations
    ):

        if not recommendations:
            return 1.0

        reply = reply.lower()

        matches = 0

        for assessment in recommendations:

            if assessment["name"].lower() in reply:
                matches += 1

        return round(
            matches / len(recommendations),
            2
        )

    # ---------------------------------------

    def recommendation_count_score(
        self,
        recommendations
    ):

        count = len(recommendations)

        if 1 <= count <= 10:
            return 1.0

        return 0.0

    # ---------------------------------------

    def evaluate(
        self,
        reply,
        recommendations,
        expected_keywords
    ):

        return {

            "retrieval_quality":
                self.retrieval_score(
                    recommendations,
                    expected_keywords
                ),

            "groundedness":
                self.groundedness_score(
                    reply,
                    recommendations
                ),

            "recommendation_limit":
                self.recommendation_count_score(
                    recommendations
                )

        }