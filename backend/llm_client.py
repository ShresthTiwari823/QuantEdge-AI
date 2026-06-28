import importlib

from backend.finance_qa import FinanceQA


try:
    genai = importlib.import_module("google.genai")
    _USE_NEW_SDK = True
except Exception:
    try:
        genai = importlib.import_module("google.generativeai")
        _USE_NEW_SDK = False
    except Exception:
        genai = None
        _USE_NEW_SDK = False


class LLMClient:

    MODEL_CANDIDATES = [
        "models/gemini-2.5-flash",
        "models/gemini-2.5-pro",
        "models/gemini-2.0-flash",
        "models/gemini-flash-latest",
        "models/gemini-flash-lite-latest",
        "models/gemini-pro-latest"
    ]

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.client = None
        self.chat = None
        self.model_name = None
        self.last_error = None
        self.fallback_qa = FinanceQA()

        if api_key:
            self._initialize()

    def _initialize(self):
        if not self.api_key:
            self.last_error = "No API key provided."
            return

        if genai is None:
            self.last_error = "Gemini SDK is not installed. Install google-generativeai or google-genai."
            return

        try:
            if _USE_NEW_SDK:
                self.client = genai.Client(api_key=self.api_key)
                self.model_name = self._discover_model()
                self.chat = self.client.chats.create(model=self.model_name)
            else:
                genai.configure(api_key=self.api_key)
                self.client = genai
                self.model_name = self._discover_model()
                model = self.client.GenerativeModel(self.model_name)
                self.chat = model.start_chat(history=[])
        except Exception as exc:
            self.last_error = str(exc)
            self.client = None
            self.chat = None
            self.model_name = None

    def _discover_model(self):
        try:
            if _USE_NEW_SDK:
                available = self.client.models.list(config={"page_size": 50})
                for model in getattr(available, "page", []) or []:
                    name = getattr(model, "display_name", None) or getattr(model, "name", None)
                    if not name:
                        continue
                    lower = name.lower()
                    for candidate in self.MODEL_CANDIDATES:
                        if candidate.lower() in lower:
                            return name
            else:
                available = self.client.list_models()
                for model in available:
                    name = getattr(model, "name", None) or getattr(model, "display_name", None)
                    if not name:
                        continue
                    lower = name.lower()
                    for candidate in self.MODEL_CANDIDATES:
                        if candidate.lower() in lower:
                            return name
        except Exception:
            pass

        return self.MODEL_CANDIDATES[0]

    def _extract_text(self, response):
        if response is None:
            return ""

        text = getattr(response, "text", None)
        if text:
            return text

        if hasattr(response, "candidates") and response.candidates:
            try:
                parts = response.candidates[0].content.parts
                pieces = []
                for part in parts:
                    part_text = getattr(part, "text", None)
                    if part_text:
                        pieces.append(part_text)
                if pieces:
                    return "".join(pieces)
            except Exception:
                pass

        return str(response)

    def is_connected(self):
        return self.chat is not None

    def _fallback_answer(self, prompt):
        return (
            "__LLM_UNAVAILABLE__ The live AI model did not return a usable response. "
            "Check the Gemini API key, quota, billing, or model limits."
        )
        return (
            "I’m using the built-in finance knowledge base for now.\n"
            "Please add a valid Gemini API key for full AI responses."
        )

    def ask(self, prompt):
        if self.chat is None:
            return self._fallback_answer(prompt)

        try:
            response = self.chat.send_message(prompt)
            answer = self._extract_text(response)
            if not answer or str(answer).startswith("LLM Error"):
                return self._fallback_answer(prompt)
            return self._format_finance_response(answer, prompt)
        except Exception as e:
            self.last_error = str(e)
            return self._fallback_answer(prompt)

    def _format_finance_response(self, answer, prompt):
        text = str(answer).strip()
        if not text:
            return text

        lower_prompt = (prompt or "").lower()
        is_stock_related = any(keyword in lower_prompt for keyword in ["stock", "rsi", "macd", "indicator", "portfolio", "buy", "sell", "risk", "finance"])
        is_pdf_related = any(keyword in lower_prompt for keyword in ["pdf", "report", "document", "summary", "annual", "financial report"])

        if is_stock_related and not is_pdf_related:
            return text

        if is_pdf_related:
            return text

        return text

    def summarize(self, text):

        prompt = f"""
Summarize the following financial report.

{text}

Provide:

• Executive Summary

• Key Financial Highlights

• Risks

• Opportunities

• Investment Outlook
"""

        return self.ask(prompt)

    def analyze_stock(
        self,
        symbol,
        price,
        rsi,
        macd,
        sentiment,
        risk
    ):

        prompt = f"""
Analyze this stock.

Symbol : {symbol}

Current Price : {price}

RSI : {rsi}

MACD : {macd}

News Sentiment : {sentiment}

Risk Level : {risk}

Explain:

1. Trend

2. Strength

3. Risks

4. Recommendation

5. Educational Disclaimer
"""

        return self.ask(prompt)

    def compare_stocks(
        self,
        stock1,
        stock2
    ):

        prompt = f"""
Compare

{stock1}

vs

{stock2}

Explain

Revenue

Profitability

Risk

Growth

Investment Recommendation
"""

        return self.ask(prompt)

    def explain_indicator(self, indicator):

        prompt = f"""
Explain

{indicator}

Use simple language.

Give one example.

Mention practical usage.
"""

        return self.ask(prompt)
