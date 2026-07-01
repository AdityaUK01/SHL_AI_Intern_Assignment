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

        # personality
        if "personality" in lower:
            state["personality"] = True

        # compare
        if "compare" in lower or "difference" in lower:
            state["comparison"] = True

        # seniority

        for level in self.seniority:
            if level in lower:
                state["seniority"] = level
                break

        # skills

        for skill in self.skills:
            if skill in lower:
                state["skills"].append(skill)

        # role

        match = re.search(
            r"hiring\s+(?:a|an)?\s*(.+?)(?:with|who|actually|$)",
            lower
        )

        if match:
            state["role"] = match.group(1).strip()

        return state