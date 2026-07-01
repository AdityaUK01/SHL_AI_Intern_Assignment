class QueryBuilder:

    def build_query(self, state):

        query_parts = []

        # ------------------------
        # Role
        # ------------------------

        if state["role"]:
            query_parts.append(state["role"])

        # ------------------------
        # Skills
        # ------------------------

        if state["skills"]:
            query_parts.extend(state["skills"])

        # ------------------------
        # Seniority
        # ------------------------

        if state["seniority"]:
            query_parts.append(state["seniority"])

        # ------------------------
        # Personality
        # ------------------------

        if state["personality"]:
            query_parts.append("personality assessment")

        # ------------------------
        # Fallback
        # ------------------------

        if not query_parts:
            query_parts.append(state["raw_query"])

        return " ".join(query_parts)