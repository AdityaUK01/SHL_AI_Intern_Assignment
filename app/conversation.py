class ConversationAnalyzer:

    CLARIFY_KEYWORDS = [
        "assessment",
        "test",
        "help",
        "recommend",
        "hire"
    ]

    REFINE_KEYWORDS = [
        "actually",
        "instead",
        "also",
        "add",
        "remove",
        "include",
        "exclude",
        "change"
    ]

    COMPARE_KEYWORDS = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    def detect_intent(self, messages):

        latest = messages[-1]["content"].lower().strip()

        # Compare
        if any(word in latest for word in self.COMPARE_KEYWORDS):
            return "compare"

        # Refine
        if any(word in latest for word in self.REFINE_KEYWORDS):
            return "refine"

        # Clarify
        if len(latest.split()) <= 4:
            return "clarify"

        if latest in [
            "assessment",
            "test",
            "i need an assessment",
            "recommend a test"
        ]:
            return "clarify"

        return "recommend"