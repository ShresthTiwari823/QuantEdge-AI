import os
import sys

import streamlit as st

ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, ROOT)

from backend.pdf_reader import PDFReader
from backend.pdf_parser import PDFParser
from backend.pdf_ai import PDFAI
from backend.pdf_storage import PDFStorage
from backend.pdf_insights import PDFInsights


def render_pdf_analyzer():
    st.header("📄 QuantEdge AI - Financial PDF Analyzer")

    st.write(
        "Upload Annual Reports, Quarterly Reports, Financial Statements or Investor Presentations."
    )

    uploaded_pdf = st.file_uploader(
        "Upload Financial PDF",
        type=["pdf"]
    )

    if uploaded_pdf is not None:

        reader = PDFReader(uploaded_pdf)

        if reader.load_pdf():

            text = reader.extract_text()

            parser = PDFParser(text)
            parsed = parser.parse()

            ai = PDFAI(text)
            ai_result = ai.analyze()

            insights = PDFInsights(text).analyze()

            storage = PDFStorage()
            filename = uploaded_pdf.name.replace(".pdf", "")

            raw_text_file = storage.save_text(filename, text)
            saved_files = storage.save_all(
                filename,
                {
                    "Parsed": parsed,
                    "AI": ai_result,
                    "Insights": insights
                }
            )

            st.success("✅ PDF analyzed successfully")
            st.divider()

            d1, d2, d3, d4 = st.columns(4)

            with open(saved_files["JSON"], "rb") as f_json:
                d1.download_button(
                    "Download JSON",
                    f_json,
                    file_name=os.path.basename(saved_files["JSON"]),
                    mime="application/json"
                )

            with open(saved_files["CSV"], "rb") as f_csv:
                d2.download_button(
                    "Download CSV",
                    f_csv,
                    file_name=os.path.basename(saved_files["CSV"]),
                    mime="text/csv"
                )

            with open(saved_files["PDF"], "rb") as f_pdf:
                d3.download_button(
                    "Download Report PDF",
                    f_pdf,
                    file_name=os.path.basename(saved_files["PDF"]),
                    mime="application/pdf"
                )

            with open(raw_text_file, "rb") as f_txt:
                d4.download_button(
                    "Download Raw Text",
                    f_txt,
                    file_name=os.path.basename(raw_text_file),
                    mime="text/plain"
                )

            st.divider()

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Pages",
                reader.get_page_count()
            )

            c2.metric(
                "Words",
                reader.word_count()
            )

            c3.metric(
                "Characters",
                reader.character_count()
            )

            st.divider()

            st.header("📋 Executive Summary")
            st.write(parsed["Summary"])

            st.divider()

            st.header("😊 Sentiment")
            st.success(
                f"{ai_result['Sentiment']['Sentiment']} "
                f"({ai_result['Sentiment']['Score']})"
            )

            st.divider()

            st.header("📊 Additional Insights")
            st.metric("Health Score", insights["Health Score"])
            st.metric("Verdict", insights["Verdict"])

            st.write("**Highlights:**")
            if insights["Highlights"]:
                for item in insights["Highlights"]:
                    st.write(f"• {item}")
            else:
                st.info("No financial highlights found.")

            st.write("**Risks:**")
            if insights["Risks"]:
                for item in insights["Risks"]:
                    st.write(f"• {item}")
            else:
                st.success("No major risks detected.")

            st.write("**Opportunities:**")
            if insights["Opportunities"]:
                for item in insights["Opportunities"]:
                    st.write(f"• {item}")
            else:
                st.info("No major opportunities detected.")

            st.divider()

            st.header("⚠ Risks")
            if ai_result["Risks"]:
                for risk in ai_result["Risks"]:
                    st.write(f"• {risk}")
            else:
                st.success("No major risks detected.")

            st.divider()

            st.header("🚀 Opportunities")
            if ai_result["Opportunities"]:
                for item in ai_result["Opportunities"]:
                    st.write(f"• {item}")
            else:
                st.info("No major opportunities detected.")

            st.divider()

            st.header("🤖 AI Recommendation")
            st.metric(
                "Recommendation",
                ai_result["Recommendation"]
            )
            st.metric(
                "Confidence",
                f"{ai_result['Confidence']}%"
            )

            st.divider()

            st.header("💾 Analysis Saved")
            st.write(saved_files["JSON"])
            st.write(saved_files["CSV"])
            st.write(saved_files["PDF"])

            reader.close()
        else:
            st.error("Unable to read PDF.")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Financial PDF Analyzer",
        page_icon="📄",
        layout="wide"
    )
    render_pdf_analyzer()