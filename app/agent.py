from app.prompts import SYSTEM_PROMPT
from app.gemini_client import ask_gemini
from app.conversation import ConversationAnalyzer
from app.state_extractor import ConversationStateExtractor
from app.query_builder import QueryBuilder
from app.comparison import AssessmentComparer


class SHLAgent:
    """
    Main conversational agent for the SHL Assessment Recommender.
    """

    def __init__(self, retriever):

        self.retriever = retriever

        self.analyzer = ConversationAnalyzer()

        self.state_extractor = ConversationStateExtractor()

        self.query_builder = QueryBuilder()

        self.comparer = AssessmentComparer()

    # --------------------------------------------------------

    def build_recommendations(self, assessments):

        recommendations = []

        seen = set()

        for assessment in assessments:

            url = assessment.get("link", "")

            # FIX: only treat as duplicate if url is non-empty AND already seen.
            # Previously, multiple assessments with no link (url == "") were
            # all collapsed into a single entry because "" was being treated
            # as a real dedup key.
            if url and url in seen:
                continue

            if url:
                seen.add(url)

            recommendations.append({

                "name": assessment.get("name"),

                "url": url,

                "test_type": ", ".join(
                    assessment.get("keys", [])
                )

            })

        return recommendations[:10]

    # --------------------------------------------------------

    def log_state(self, title, value):

        print("\n" + "=" * 60)

        print(title)

        print("=" * 60)

        print(value)

    # --------------------------------------------------------

    def chat(self, messages):

        conversation = "\n".join(

            f"{m['role']}: {m['content']}"

            for m in messages

        )

        intent = self.analyzer.detect_intent(messages)

        self.log_state(
            "Intent",
            intent
        )

        # ----------------------------------------------------
        # Clarification
        # ----------------------------------------------------

        if intent == "clarify":

            return {

                "reply":
                    (
                        "I'd be happy to help.\n\n"
                        "Please tell me:\n"
                        "• Job Role\n"
                        "• Experience Level\n"
                        "• Skills Required\n"
                        "• Hiring Goal\n\n"
                        "Then I'll recommend the most suitable SHL assessments."
                    ),

                "recommendations": [],

                "end_of_conversation": False

            }

        # ----------------------------------------------------
        # Build Conversation State
        # ----------------------------------------------------

        state = self.state_extractor.extract(
            messages
        )

        self.log_state(
            "Conversation State",
            state
        )

        search_query = self.query_builder.build_query(
            state
        )

        self.log_state(
            "Search Query",
            search_query
        )

        blocked = [
            "ignore your instructions",
            "ignore previous instructions",
            "system prompt",
            "jailbreak"
        ]

        if any(x in state["raw_query"].lower() for x in blocked):
            return {
                "reply": "I can only recommend assessments that exist in the SHL catalog.",
                "recommendations": [],
                "end_of_conversation": False
            }


        # ----------------------------------------------------
        # Retrieve Assessments
        # ----------------------------------------------------

        if state["comparison"] and state["compare_items"]:

            assessments, context = self.retriever.compare(
                state["compare_items"]
            )

        elif state["personality"]:

            assessments, context = self.retriever.search_multiple(
                [
                    search_query,
                    "personality assessment"
                ],
                top_k_each=5
            )

        else:

            assessments, context = self.retriever.search(
                search_query,
                top_k=10
            )

        self.log_state(
            "Retrieved Assessments",
            len(assessments)
        )

        # ----------------------------------------------------
        # Compare Intent
        # ----------------------------------------------------

        if intent == "compare":

            # NOTE: unchanged — comparer.compare() is only given `assessments`,
            # not `conversation` or `state`. I have not seen comparison.py's
            # signature, so I have not guessed a fix here. If compare() needs
            # to know WHICH assessments the user is comparing (vs the full
            # retrieved list), this needs a real fix once that file is shared.
            reply = self.comparer.compare(
                assessments
            )

        else:

            prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Conversation History

{conversation}

Structured Conversation State

{state}

Relevant SHL Catalog

{context}

Rules:

- Recommend ONLY assessments from the supplied catalog.
- Never invent assessment names.
- Never invent URLs.
- Explain WHY each recommendation fits.
- Mention important details like:
  • Duration
  • Job Level
  • Category
- If personality=True, include personality assessments if available.
- If comparison=True, compare ONLY using the supplied catalog.
- If there are no suitable assessments, explicitly state that no exact SHL assessment exists and recommend the closest relevant assessments.
- Keep the answer concise.
"""

            reply = ask_gemini(
                SYSTEM_PROMPT,
                prompt
            )

        # ----------------------------------------------------
        # Build Recommendation List
        # ----------------------------------------------------

        recommendations = self.build_recommendations(
            assessments
        )

        self.log_state(
            "Recommendations",
            len(recommendations)
        )

        for recommendation in recommendations:

            print(
                recommendation["name"]
            )

        # ----------------------------------------------------
        # Build API Response
        # ----------------------------------------------------

        response = {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False
        }

        self.log_state(
            "Response Ready",
            f"{len(recommendations)} recommendations"
        )

        return response