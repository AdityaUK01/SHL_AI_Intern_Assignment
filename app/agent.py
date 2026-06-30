from app.prompts import SYSTEM_PROMPT
from app.gemini_client import ask_gemini


class SHLAgent:

    def __init__(self, retriever):
        self.retriever = retriever

    def chat(self, messages):

        conversation = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in messages
        )

        latest = messages[-1]["content"]

        results, context = self.retriever.search(latest)

        prompt = f"""
Conversation History:

{conversation}

Relevant SHL Catalog Entries:

{context}

Task:

1. Read the whole conversation.
2. If information is missing, ask ONE clarifying question.
3. Otherwise recommend relevant assessments.
4. If user asks to compare, compare ONLY using the supplied catalog.
5. Never invent assessment names or URLs.
"""

        reply = ask_gemini(
            SYSTEM_PROMPT,
            prompt
        )

        recommendations = []

        for assessment in results:

            recommendations.append(
                {
                    "name": assessment["name"],
                    "url": assessment["link"],
                    "test_type": ", ".join(
                        assessment.get("keys", [])
                    )
                }
            )

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False
        }