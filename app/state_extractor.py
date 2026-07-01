import re


class ConversationStateExtractor:

    def __init__(self):

        self.skills = [
            "java",
            "python",
            "sql",
            "javascript",
            "react",
            "node",
            "aws",
            "azure",
            "docker",
            "kubernetes",
            "c++",
            "c#"
        ]

        self.seniority = [
            "intern",
            "entry",
            "junior",
            "mid",
            "senior",
            "lead",
            "manager"
        ]

    def extract(self, messages):

        state = {
            "role": "",
            "skills": [],
            "seniority": "",
            "personality": False,
            "comparison": False,
            "compare_items": [],
            "raw_query": ""
        }

        text = " ".join(
            m["content"]
            for m in messages
            if m["role"] == "user"
        )

        state["raw_query"] = text

        lower = text.lower()

        # -------------------------
        # Personality
        # -------------------------

        personality_keywords = [
            "personality",
            "behavior",
            "behaviour",
            "opq"
        ]

        if any(word in lower for word in personality_keywords):
            state["personality"] = True

        # -------------------------
        # Comparison
        # -------------------------

        comparison_keywords = [
            "compare",
            "comparison",
            "difference",
            "vs",
            "versus"
        ]

        if any(word in lower for word in comparison_keywords):
            state["comparison"] = True

        # -------------------------
        # Seniority
        # -------------------------

        for level in self.seniority:
            if level in lower:
                state["seniority"] = level
                break

        # -------------------------
        # Skills
        # -------------------------

        for skill in self.skills:
            if skill in lower:
                state["skills"].append(skill)

        # -------------------------
        # Role
        # -------------------------

        role_match = re.search(
            r"hiring\s+(?:a|an)?\s*(.+?)(?:with|who|actually|$)",
            lower
        )

        if role_match:
            state["role"] = role_match.group(1).strip()

        # -------------------------
        # Compare Items
        # -------------------------

        if state["comparison"]:

            compare_match = re.search(
                r"compare\s+(.+?)\s+(?:and|vs|versus)\s+(.+)",
                text,
                re.IGNORECASE
            )

            if compare_match:

                first = compare_match.group(1).strip()

                second = compare_match.group(2).strip()

                state["compare_items"] = [
                    first,
                    second
                ]

        return state