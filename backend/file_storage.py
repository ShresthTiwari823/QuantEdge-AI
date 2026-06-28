import os
import json
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class FileStorage:

    def __init__(self, folder="analysis"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def _normalize_value(self, value):
        if isinstance(value, list):
            return "; ".join(str(v) for v in value)
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
        return value

    def save_json(self, filename, data):
        path = os.path.join(self.folder, filename + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return path

    def save_csv(self, filename, data):
        path = os.path.join(self.folder, filename + ".csv")
        flat_data = {
            key: self._normalize_value(value)
            for key, value in data.items()
        }
        df = pd.DataFrame([flat_data])
        df.to_csv(path, index=False)
        return path

    def save_text(self, filename, text):
        path = os.path.join(self.folder, filename + ".txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def save_pdf(self, filename, data):
        path = os.path.join(self.folder, filename + ".pdf")
        doc = SimpleDocTemplate(path)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("<b>QuantEdge AI Analysis Report</b>", styles["Title"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Generated: {datetime.now().isoformat(timespec='seconds')}", styles["Normal"]))
        story.append(Spacer(1, 12))

        for key, value in data.items():
            story.append(Paragraph(f"<b>{key}</b>", styles["Heading2"]))
            story.append(Paragraph(str(self._normalize_value(value)), styles["BodyText"]))
            story.append(Spacer(1, 12))

        doc.build(story)
        return path

    def save_all(self, filename, data, raw_text=None, save_pdf=True):
        json_file = self.save_json(filename, data)
        csv_file = self.save_csv(filename, data)
        text_file = None
        pdf_file = None
        if raw_text is not None:
            text_file = self.save_text(filename, raw_text)
        if save_pdf:
            pdf_file = self.save_pdf(filename, data)
        return {
            "JSON": json_file,
            "CSV": csv_file,
            "Text": text_file,
            "PDF": pdf_file
        }
