import re


class PDFParser:

    def __init__(self, text):

        self.text = text

    def clean_text(self):

        cleaned = re.sub(r"\s+", " ", self.text)

        cleaned = cleaned.replace("\n", " ")

        return cleaned.strip()

    def sentence_count(self):

        return len(re.findall(r"[.!?]", self.text))

    def extract_numbers(self):

        return re.findall(r"\d[\d,]*\.?\d*", self.text)

    def find_currency_values(self):

        pattern = r"(₹\s?[\d,]+(?:\.\d+)?)|(\$\s?[\d,]+(?:\.\d+)?)"

        matches = re.findall(pattern, self.text)

        values = []

        for item in matches:

            for value in item:

                if value:
                    values.append(value)

        return values

    def keyword_frequency(self):

        keywords = [
            "revenue",
            "profit",
            "loss",
            "growth",
            "debt",
            "cash",
            "assets",
            "liabilities",
            "equity",
            "dividend",
            "earnings",
            "income"
        ]

        freq = {}

        lower_text = self.text.lower()

        for word in keywords:

            freq[word] = lower_text.count(word)

        return freq

    def extract_summary(self):

        sentences = re.split(r"(?<=[.!?])\s+", self.clean_text())

        return " ".join(sentences[:10])

    def detect_sections(self):

        sections = [
            "Management Discussion",
            "Risk Factors",
            "Financial Statements",
            "Business Overview",
            "Corporate Governance",
            "Auditor Report"
        ]

        found = []

        lower = self.text.lower()

        for section in sections:

            if section.lower() in lower:

                found.append(section)

        return found

    def parse(self):

        return {

            "Word Count": len(self.clean_text().split()),

            "Sentence Count": self.sentence_count(),

            "Numbers": self.extract_numbers(),

            "Currency Values": self.find_currency_values(),

            "Keyword Frequency": self.keyword_frequency(),

            "Detected Sections": self.detect_sections(),

            "Summary": self.extract_summary()

        }