import json


def format_markdown(title, text):
    formatted = f"### {title}\n\n{text.strip()}"
    return formatted


def format_json(question, answer, metadata=None):
    payload = {
        "question": question,
        "answer": answer,
        "metadata": metadata or {}
    }
    return json.dumps(payload, indent=2)


def format_summary(summary_text):
    return f"**Executive Summary**\n\n{summary_text.strip()}"
