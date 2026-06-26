from textblob import TextBlob


class PDFAI:

    def __init__(self, text):

        self.text = text

    def sentiment(self):

        polarity = TextBlob(self.text).sentiment.polarity

        if polarity > 0.15:

            return {

                "Sentiment": "Positive",

                "Score": round(polarity, 2)

            }

        elif polarity < -0.15:

            return {

                "Sentiment": "Negative",

                "Score": round(polarity, 2)

            }

        else:

            return {

                "Sentiment": "Neutral",

                "Score": round(polarity, 2)

            }

    def positive_points(self):

        keywords = [

            "growth",

            "increase",

            "profit",

            "expansion",

            "strong",

            "opportunity",

            "innovation",

            "success",

            "record",

            "improved"

        ]

        found = []

        lower = self.text.lower()

        for word in keywords:

            if word in lower:

                found.append(word)

        return found

    def negative_points(self):

        keywords = [

            "loss",

            "debt",

            "decline",

            "risk",

            "drop",

            "lawsuit",

            "weak",

            "uncertainty",

            "inflation",

            "competition"

        ]

        found = []

        lower = self.text.lower()

        for word in keywords:

            if word in lower:

                found.append(word)

        return found

    def investment_recommendation(self):

        positive = len(self.positive_points())

        negative = len(self.negative_points())

        if positive > negative + 2:

            return "BUY"

        elif negative > positive + 2:

            return "SELL"

        else:

            return "HOLD"

    def confidence(self):

        positive = len(self.positive_points())

        negative = len(self.negative_points())

        total = positive + negative

        if total == 0:

            return 50

        confidence = max(positive, negative) / total

        return round(confidence * 100, 2)

    def risks(self):

        risk_words = [

            "debt",

            "lawsuit",

            "competition",

            "inflation",

            "loss",

            "regulation",

            "uncertainty",

            "volatility"

        ]

        risks = []

        lower = self.text.lower()

        for word in risk_words:

            if word in lower:

                risks.append(word)

        return risks

    def opportunities(self):

        words = [

            "growth",

            "expansion",

            "investment",

            "technology",

            "innovation",

            "digital",

            "market",

            "acquisition"

        ]

        opportunities = []

        lower = self.text.lower()

        for word in words:

            if word in lower:

                opportunities.append(word)

        return opportunities

    def analyze(self):

        return {

            "Sentiment": self.sentiment(),

            "Positive Points": self.positive_points(),

            "Negative Points": self.negative_points(),

            "Risks": self.risks(),

            "Opportunities": self.opportunities(),

            "Recommendation": self.investment_recommendation(),

            "Confidence": self.confidence()

        }