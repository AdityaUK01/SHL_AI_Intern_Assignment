class ConversationAnalyzer:

    def detect_intent(self, messages):

        if not messages:
            return "clarify"

        user_messages = [
            m["content"].lower()
            for m in messages
            if m["role"] == "user"
        ]

        if not user_messages:
            return "clarify"

        latest = user_messages[-1]

        compare_words = [
            "compare",
            "comparison",
            "difference",
            "vs",
            "versus"
        ]

        if any(word in latest for word in compare_words):
            return "compare"

        refine_words = [
            "actually",
            "instead",
            "also",
            "add",
            "remove",
            "change",
            "only",
            "include"
        ]

        if len(user_messages) > 1 and any(word in latest for word in refine_words):
            return "refine"

        clarify_words = [
            "assessment",
            "test",
            "help",
            "recommend"
        ]

        if (
            len(user_messages) == 1
            and len(latest.split()) <= 5
            and any(word in latest for word in clarify_words)
        ):
            return "clarify"

        return "recommend"