import streamlit as st

from backend.ai_assistant import AIAssistant
from backend.chat_memory import ChatMemory
from backend.pdf_chat import PDFChat
from backend.pdf_reader import PDFReader
from backend.stock_chat import StockChat


assistant = AIAssistant()
memory = ChatMemory()
stock_chat = StockChat()
pdf_chat = PDFChat()


def _is_canned_text(text):
    lower = str(text or "").lower()
    return any(marker in lower for marker in [
        "i can help with financial analysis",
        "i can help with finance topics",
        "for a better answer, ask a specific question",
        "what does rsi mean",
        "how do i read macd",
        "can you summarize this financial document",
        "__llm_unavailable__",
    ])


def _rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


def _apply_assistant_styles():
    st.markdown(
        """
<style>
    .block-container {
        max-width: 1120px;
        padding-top: 3.25rem;
        padding-bottom: 2.5rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid #edf0f5;
    }

    .qe-title {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        color: #303946;
        font-size: 3.05rem;
        font-weight: 800;
        line-height: 1.08;
        margin: 0 0 0.85rem;
    }

    .qe-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.3rem;
        height: 2.3rem;
        border: 3px solid #303946;
        border-radius: 999px;
        font-size: 1.25rem;
        line-height: 1;
    }

    .qe-link {
        display: inline-block;
        color: #8a93a1;
        font-size: 1.2rem;
        margin-left: 0.15rem;
        margin-top: -0.4rem;
        margin-bottom: 1.1rem;
    }

    .qe-subtitle {
        color: #5d6673;
        font-size: 1.1rem;
        margin-bottom: 2.1rem;
    }

    .qe-caption {
        color: #303946;
        font-weight: 650;
        margin-bottom: 0.35rem;
    }

    div[data-testid="stRadio"] {
        margin-bottom: 2.2rem;
    }

    div[data-testid="stRadio"] label {
        font-size: 1rem;
        color: #424b57;
    }

    .qe-section-title {
        color: #303946;
        font-size: 2rem;
        font-weight: 760;
        line-height: 1.2;
        margin: 0.9rem 0 1.2rem;
    }

    .qe-result-title {
        color: #303946;
        font-size: 1.08rem;
        font-weight: 760;
        margin-top: 1.6rem;
        margin-bottom: 0.9rem;
    }

    .qe-analysis {
        color: #303946;
        font-size: 1.03rem;
        line-height: 1.72;
    }

    .qe-analysis h1,
    .qe-analysis h2,
    .qe-analysis h3 {
        color: #303946;
        font-weight: 780;
        margin-top: 2.4rem;
        margin-bottom: 1rem;
    }

    .qe-analysis h1 {
        font-size: 2rem;
    }

    .qe-analysis h2 {
        font-size: 1.75rem;
    }

    .qe-analysis h3 {
        font-size: 1.45rem;
    }

    .qe-analysis strong {
        color: #202834;
    }

    .qe-analysis hr {
        border: none;
        border-top: 1px solid #e8ecf1;
        margin: 2.1rem 0;
    }

    .stTextInput input,
    .stNumberInput input,
    div[data-baseweb="select"] > div {
        background: #f8fafc;
        border-color: #eef1f5;
        min-height: 3rem;
    }

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #dce2ea;
        background: #ffffff;
        color: #303946;
        min-height: 3rem;
        padding-left: 1.15rem;
        padding-right: 1.15rem;
    }

    .stButton > button:hover {
        border-color: #c8d0da;
        color: #101820;
    }

    div[data-testid="stChatInput"] {
        max-width: 1020px;
        margin: 0 auto;
    }

    div[data-testid="stChatMessage"] {
        background: transparent;
    }
</style>
        """,
        unsafe_allow_html=True,
    )


def _render_header():
    st.markdown(
        """
<div class="qe-title">
    <span class="qe-icon">🤖</span>
    <span>QuantEdge AI Financial Assistant</span>
</div>
<div class="qe-link">🔗</div>
<div class="qe-subtitle">
    Ask anything about stocks, technical indicators, portfolio or uploaded financial reports.
</div>
        """,
        unsafe_allow_html=True,
    )


def _render_general_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.messages = [
        msg
        for msg in st.session_state.messages
        if not _is_canned_text(msg.get("content", ""))
    ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask your financial question...")

    if not question:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    result = assistant.answer(question)
    answer = result["answer"]

    memory.save_message(question, answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)


def _render_stock_analysis():
    st.markdown(
        '<div class="qe-section-title">Stock Analysis with Gemini / fallback reasoning</div>',
        unsafe_allow_html=True,
    )

    symbols_text = st.text_input(
        "Stock Symbol",
        value="TCS.NS",
        help="Enter one symbol or multiple symbols separated by commas, for example: TCS.NS, INFY.NS, AAPL.",
    )
    use_market_data = st.checkbox(
        "Use latest market data when available",
        value=True,
    )

    if not use_market_data:
        price = st.number_input("Current Price", value=100.0, min_value=0.0, step=1.0)
        rsi = st.number_input("RSI", value=50.0, min_value=0.0, max_value=100.0, step=1.0)
        macd = st.number_input("MACD", value=0.0, step=0.1)
    else:
        price = 100.0
        rsi = 50.0
        macd = 0.0

    sentiment = st.selectbox(
        "News Sentiment",
        ["Positive", "Neutral", "Negative"],
    )
    risk = st.selectbox(
        "Risk Level",
        ["Low", "Medium", "High"],
        index=2,
    )

    if not st.button("Analyze Stock"):
        return

    symbols = [
        item.strip().upper()
        for item in symbols_text.split(",")
        if item.strip()
    ]

    if not symbols:
        st.error("Please enter at least one stock symbol.")
        return

    for cleaned_symbol in symbols:
        if use_market_data:
            result = stock_chat.analyze_symbol(
                symbol=cleaned_symbol,
                sentiment=sentiment,
                risk=risk,
            )
            response = result["analysis"]
            market_data = result["market_data"]

            if market_data["ok"]:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Current Price", f"{market_data['price']:.2f}")
                c2.metric("RSI", f"{market_data['rsi']:.2f}")
                c3.metric("MACD", f"{market_data['macd']:.2f}")
                c4.metric("Data Rows", market_data["rows"])
            else:
                st.warning(market_data["error"])
        else:
            response = stock_chat.analyze(
                symbol=cleaned_symbol,
                price=price,
                rsi=rsi,
                macd=macd,
                sentiment=sentiment,
                risk=risk,
            )

        st.markdown(
            f'<div class="qe-result-title">Analysis for {cleaned_symbol}:</div>',
            unsafe_allow_html=True,
        )
        st.markdown(response)
        st.divider()

        memory.save_message(
            f"Analyze stock {cleaned_symbol}",
            response,
        )


def _render_pdf_summarizer():
    st.markdown(
        '<div class="qe-section-title">Financial PDF Summarizer</div>',
        unsafe_allow_html=True,
    )

    uploaded_pdf = st.file_uploader(
        "Upload Financial PDF",
        type=["pdf"],
    )

    if uploaded_pdf is None:
        return

    if (
        st.session_state.get("pdf_name") != uploaded_pdf.name
        or "pdf_text" not in st.session_state
    ):
        st.session_state.pop("pdf_summary", None)
        st.session_state.pop("pdf_messages", None)

    reader = PDFReader(uploaded_pdf)

    if not reader.load_pdf():
        st.error("Unable to read the uploaded PDF.")
        return

    text = reader.extract_text()
    st.session_state.pdf_name = uploaded_pdf.name
    st.session_state.pdf_text = text

    if "pdf_summary" not in st.session_state:
        st.session_state.pdf_summary = pdf_chat.summarize(text)
        memory.save_message(
            f"Summarize PDF {uploaded_pdf.name}",
            st.session_state.pdf_summary,
        )

    st.markdown("**PDF Summary:**")
    st.markdown(st.session_state.pdf_summary)

    metadata = reader.get_metadata()
    if metadata:
        st.markdown("**Document Metadata:**")
        st.json(metadata)

    st.divider()
    st.subheader("Ask a Question About This PDF")

    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []

    for msg in st.session_state.pdf_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pdf_question = st.chat_input("Ask a question about the uploaded PDF...")

    if pdf_question:
        st.session_state.pdf_messages.append(
            {
                "role": "user",
                "content": pdf_question,
            }
        )
        answer = pdf_chat.answer_question(text, pdf_question)
        st.session_state.pdf_messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
        memory.save_message(
            f"PDF Q&A: {pdf_question}",
            answer,
        )
        _rerun()

    reader.close()


def _render_footer():
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            memory.clear_history()
            st.success("Chat history cleared.")
            _rerun()

    with col2:
        st.metric(
            "Total Messages",
            memory.total_messages(),
        )

    with st.expander("Previous Conversations"):
        history = memory.export_history()

        if not history:
            st.info("No conversations yet.")
            return

        for chat in reversed(history):
            if _is_canned_text(chat.get("assistant", "")):
                continue

            st.markdown(f"**{chat['timestamp']}**")
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**AI:** {chat['assistant']}")
            st.divider()


def ai_chat():
    _apply_assistant_styles()
    _render_header()

    st.markdown('<div class="qe-caption">Choose assistant mode:</div>', unsafe_allow_html=True)

    mode = st.radio(
        "Choose assistant mode:",
        ["General Chat", "Stock Analysis", "PDF Summarizer"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if mode == "General Chat":
        _render_general_chat()
    elif mode == "Stock Analysis":
        _render_stock_analysis()
    else:
        _render_pdf_summarizer()

    _render_footer()
