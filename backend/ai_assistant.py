import datetime
from backend.config import GEMINI_API_KEY
from backend.finance_qa import FinanceQA
from backend.llm_client import LLMClient
from backend.prompt_engine import PromptEngine


class AIAssistant:

    def __init__(self):

        self.qa = FinanceQA()
        self.prompt = PromptEngine()
        self.llm = LLMClient(api_key=GEMINI_API_KEY)

    def greet(self):

        hour = datetime.datetime.now().hour

        if hour < 12:
            return "Good Morning 👋"

        elif hour < 18:
            return "Good Afternoon 👋"

        return "Good Evening 👋"

    def _is_stock_query(self, question):
        q = question.lower()
        return any(keyword in q for keyword in [
            "stock", "stocks", "rsi", "macd", "ema", "atr", "bollinger",
            "portfolio", "buy", "sell", "hold", "risk", "indicator", "technical"
        ]) and "pdf" not in q and "report" not in q and "document" not in q

    def _is_canned_fallback(self, answer):
        if not isinstance(answer, str):
            return True

        text = answer.lower()
        return any(marker in text for marker in [
            "i can help with financial analysis",
            "i can help with finance topics",
            "for a better answer",
            "try asking about",
            "what does rsi mean",
            "how do i read macd",
            "can you summarize this financial document",
            "__llm_unavailable__",
        ])

    def _general_fallback(self, question):
        q = question.strip()
        lower = q.lower()

        if lower in ["hi", "hello", "hey", "hii"]:
            return "Hello. Ask me anything, and I will help as clearly as I can."

        if "write" in lower and ("email" in lower or "message" in lower):
            return (
                "Sure. Tell me the recipient, purpose, tone, and key points, "
                "and I can draft it for you."
            )

        if lower.startswith("explain ") or "what is" in lower or "what are" in lower:
            return (
                f"Here is a simple way to think about it:\n\n"
                f"**{q}**\n\n"
                "This needs a live AI response for a complete answer. "
                "The ChatGPT-style chat area is ready, but the model response is currently unavailable. "
                "Please check your Gemini API key/model connection in `.env`, then ask again."
            )

        return (
            "The ChatGPT-style chat area is ready, but the live AI model did not return a usable response. "
            "Please check your Gemini API key/model connection in `.env` and try again."
        )

    def answer(self, question):

        question = question.strip()

        if question == "":
            return {
                "type": "error",
                "answer": "Please enter a question."
            }

        prompt = self.prompt.build_prompt(question)

        if self.llm.is_connected():
            answer = self.llm.ask(prompt)
            if self._is_canned_fallback(answer):
                answer = self._general_fallback(question)
        else:
            if self._is_stock_query(question):
                answer = self.qa.get_answer(question)
            else:
                answer = self._general_fallback(question)

        if isinstance(answer, str) and answer.strip():
            answer = answer.strip()
        else:
            answer = self._general_fallback(question)

        return {

            "type": "assistant",

            "question": question,

            "prompt": prompt,

            "answer": answer,

            "time": datetime.datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        }

    def stock_recommendation(
        self,
        symbol,
        signal,
        confidence,
        risk
    ):

        if signal == "BUY":

            msg = (
                f"{symbol} currently has a BUY signal.\n\n"
                f"AI Confidence : {confidence}%\n"
                f"Risk Level : {risk}\n\n"
                "Momentum and technical indicators are positive."
            )

        elif signal == "SELL":

            msg = (
                f"{symbol} currently has a SELL signal.\n\n"
                f"AI Confidence : {confidence}%\n"
                f"Risk Level : {risk}\n\n"
                "Technical indicators suggest weakness."
            )

        else:

            msg = (
                f"{symbol} currently has a HOLD signal.\n\n"
                f"AI Confidence : {confidence}%\n"
                f"Risk Level : {risk}\n\n"
                "Wait for stronger confirmation."
            )

        return msg

    def explain_indicator(self, indicator):

        return self.qa.get_answer(indicator)

    def summarize_pdf(self, summary):

        if not summary or not str(summary).strip():
            return "The uploaded report appears empty. Please upload a valid financial PDF."

        return (
            "Financial Report Summary\n\n"
            + str(summary).strip()
        )

    def compare_result(
        self,
        stock1,
        stock2
    ):

        return (
            f"Comparison completed successfully.\n\n"
            f"{stock1} has been compared with {stock2}.\n"
            "Please check the Stock Comparison dashboard."
        )
