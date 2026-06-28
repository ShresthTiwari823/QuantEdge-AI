class PromptEngine:

    def __init__(self):

        self.system_prompt = """
You are QuantEdge AI.

You are an AI Financial Assistant.

Your responsibilities include:

• Stock Analysis

• Technical Indicator Explanation

• News Sentiment Analysis

• Portfolio Guidance

• Risk Management

• Financial PDF Analysis

Always answer professionally.

Avoid giving guaranteed investment advice.

Explain concepts in simple language.

Provide educational guidance.
"""

    def build_prompt(self, user_question):

        prompt = f"""

SYSTEM

{self.system_prompt}

----------------------------

USER QUESTION

{user_question}

----------------------------

Instructions

1. Understand the question.

2. Explain in simple English.

3. If related to stocks,

consider

RSI

MACD

EMA

Volatility

News Sentiment

Risk Level.

4. If related to uploaded PDF,

summarize important findings.

5. If comparison is requested,

compare both companies clearly.

6. End with an educational disclaimer.

"""

        return prompt

    def stock_prompt(
        self,
        symbol,
        signal,
        confidence,
        risk
    ):

        return f"""

Analyze Stock

Symbol : {symbol}

AI Signal : {signal}

Confidence : {confidence}%

Risk : {risk}

Explain

• Why AI selected this signal.

• Technical reasoning.

• Possible risks.

• Educational conclusion.

"""

    def pdf_prompt(
        self,
        summary
    ):

        return f"""

Analyze Financial Report

Summary

{summary}

Explain

• Financial Health

• Risks

• Opportunities

• Investment View

"""

    def comparison_prompt(
        self,
        stock1,
        stock2
    ):

        return f"""

Compare

{stock1}

vs

{stock2}

Explain

Revenue

Profit

Risk

Growth

Recommendation

"""

    def indicator_prompt(
        self,
        indicator
    ):

        return f"""

Explain

{indicator}

Use simple language.

Give examples.

Explain practical use for investors.

"""