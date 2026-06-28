from backend.config import GEMINI_API_KEY
from backend.llm_client import LLMClient
import re


class PDFChat:

    def __init__(self, api_key=None):
        self.llm = LLMClient(api_key=api_key or GEMINI_API_KEY)

    def summarize(self, text):
        if self.llm.is_connected():
            answer = self.llm.summarize(text)
            if self._is_usable_answer(answer):
                return answer

        return self._fallback_summary(text)

    def insights(self, text):
        if self.llm.is_connected():
            return self.llm.ask(
                "You are analyzing a financial report. Extract the main financial risks, opportunities, outlook, and a concise investment takeaway. Use bullet points and keep it professional.\n\n" + text
            )

        return self._fallback_summary(text)

    def answer_question(self, text, question):
        if self.llm.is_connected():
            prompt = (
                "You are a financial PDF assistant. Answer the user's question using only the uploaded document context. "
                "Be concise, structured, and finance-focused. If the answer is not in the document, say so clearly.\n\n"
                f"User question: {question}\n\nDocument content:\n{text}"
            )
            answer = self.llm.ask(prompt)
            if self._is_usable_answer(answer):
                return answer

        return self._fallback_question_answer(text, question)

    def _is_usable_answer(self, answer):
        if not isinstance(answer, str) or not answer.strip():
            return False

        lower = answer.lower()
        return not any(
            marker in lower
            for marker in [
                "pdf summary is unavailable",
                "pdf q&a is unavailable",
                "please add your api key",
                "for a better answer",
                "__llm_unavailable__",
            ]
        )

    def _fallback_summary(self, text):
        clean_text = self._clean_text(text)
        if not clean_text:
            return (
                "## PDF Summary\n\n"
                "No readable text was found in this PDF. If it is a scanned document, "
                "please upload an OCR-readable PDF before analysis."
            )

        sentences = self._sentences(clean_text)
        overview = sentences[:5]
        risk_lines = self._matching_sentences(
            sentences,
            ["risk", "uncertain", "liability", "debt", "loss", "decline", "adverse", "volatility"],
            5,
        )
        opportunity_lines = self._matching_sentences(
            sentences,
            ["growth", "increase", "profit", "revenue", "opportunity", "margin", "expansion", "cash"],
            5,
        )

        if not risk_lines:
            risk_lines = ["No explicit risk sentences were found in the extracted text."]

        if not opportunity_lines:
            opportunity_lines = ["No clear opportunity or growth sentences were found in the extracted text."]

        return (
            "## PDF Summary\n\n"
            "### Executive Summary\n\n"
            + self._bullet_list(overview)
            + "\n### Key Financial Signals\n\n"
            + self._bullet_list(opportunity_lines)
            + "\n### Risks\n\n"
            + self._bullet_list(risk_lines)
            + "\n### Investment Outlook\n\n"
            "- Review the original report carefully before taking any decision.\n"
            "- Compare revenue, profitability, debt, cash flow, and management commentary with previous periods.\n"
            "- This summary is educational and should not be treated as financial advice.\n"
        )

    def _fallback_question_answer(self, text, question):
        clean_text = self._clean_text(text)
        clean_question = self._clean_text(question)

        if not clean_text:
            return "No readable text was found in this PDF, so I cannot answer questions from it."

        keywords = [
            word
            for word in re.findall(r"[A-Za-z0-9]+", clean_question.lower())
            if len(word) > 3
        ]

        sentences = self._sentences(clean_text)
        matches = self._matching_sentences(sentences, keywords, 6)

        if not matches:
            return (
                "I could not find a clear answer in the extracted PDF text. "
                "Try asking with a company name, metric, year, section title, or keyword from the report."
            )

        return (
            "## Answer From Uploaded PDF\n\n"
            + self._bullet_list(matches)
            + "\n**Note:** This answer is based only on the readable text extracted from the uploaded PDF."
        )

    def _clean_text(self, text):
        return re.sub(r"\s+", " ", str(text or "")).strip()

    def _sentences(self, text):
        pieces = re.split(r"(?<=[.!?])\s+", text)
        return [
            piece.strip()
            for piece in pieces
            if len(piece.strip()) > 15
        ]

    def _matching_sentences(self, sentences, keywords, limit):
        if not keywords:
            return sentences[:limit]

        matches = []
        lowered_keywords = [keyword.lower() for keyword in keywords]

        for sentence in sentences:
            lower = sentence.lower()
            if any(keyword in lower for keyword in lowered_keywords):
                matches.append(sentence)
            if len(matches) >= limit:
                break

        return matches

    def _bullet_list(self, lines):
        if not lines:
            return "- No readable details found.\n"

        return "".join(f"- {line}\n" for line in lines)
