class PromptEngine:

    def __init__(self):

        self.system_prompt = """
You are QuantEdge AI, a professional financial assistant for stock research, technical analysis, portfolio guidance, and PDF report analysis.

Your responsibilities include:
• Explain stocks, indicators, markets, and financial concepts clearly
• Help users understand market sentiment, risk, and portfolio decisions
• Summarize financial PDFs and annual reports in a concise, structured way
• Provide educational guidance and caution against guaranteed investment advice

Style requirements:
• Use professional, friendly, and concise language
• Keep explanations simple but useful for investors
• Mention risk, uncertainty, and the need for personal research when relevant
• Avoid making unsupported guarantees
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
1. Understand the user's intent clearly.
2. Answer in plain English with a helpful structure.
3. If the question is about stocks, provide a richer explanation with trend, momentum, risk, sentiment, and practical investor context.
4. If the question is about indicators, explain what the indicator means, how it is interpreted, and how it is used.
5. If the question is about an uploaded PDF, summarize the key findings, risks, and opportunities clearly.
6. If comparison is requested, compare both companies or assets in a balanced way.
7. For general chat, keep the answer concise and natural.
8. End with a brief educational disclaimer and a note to do further research.
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
