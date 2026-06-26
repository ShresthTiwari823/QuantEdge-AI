import re


class PDFInsights:

    def __init__(self, text):

        self.text = text.lower()

    def find_keywords(self, words):

        found = []

        for word in words:

            if word in self.text:

                found.append(word)

        return found

    def financial_highlights(self):

        words = [
            "revenue",
            "profit",
            "income",
            "earnings",
            "cash flow",
            "assets"
        ]

        return self.find_keywords(words)

    def risks(self):

        words = [
            "debt",
            "loss",
            "inflation",
            "competition",
            "lawsuit",
            "risk",
            "decline"
        ]

        return self.find_keywords(words)

    def opportunities(self):

        words = [
            "growth",
            "expansion",
            "innovation",
            "technology",
            "investment",
            "acquisition"
        ]

        return self.find_keywords(words)

    def health_score(self):

        positive = len(self.opportunities())

        negative = len(self.risks())

        score = 50 + (positive * 10) - (negative * 8)

        score = max(0, min(score, 100))

        return score

    def verdict(self):

        score = self.health_score()

        if score >= 75:
            return "🟢 Strong Financial Health"

        elif score >= 55:
            return "🟡 Stable Financial Health"

        else:
            return "🔴 Weak Financial Health"

    def analyze(self):

        return {

            "Highlights": self.financial_highlights(),

            "Risks": self.risks(),

            "Opportunities": self.opportunities(),

            "Health Score": self.health_score(),

            "Verdict": self.verdict()

        }