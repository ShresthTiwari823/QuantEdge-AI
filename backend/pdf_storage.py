import os
import json
import pandas as pd
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


class PDFStorage:

    def __init__(self):

        self.analysis_folder = "analysis"

        os.makedirs(
            self.analysis_folder,
            exist_ok=True
        )

    def save_json(
        self,
        filename,
        data
    ):

        path = os.path.join(
            self.analysis_folder,
            filename + ".json"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return path

    def _normalize_value(self, value):

        if isinstance(value, list):
            return "; ".join(str(v) for v in value)

        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)

        return value

    def save_csv(
        self,
        filename,
        data
    ):

        path = os.path.join(
            self.analysis_folder,
            filename + ".csv"
        )

        flat_data = {
            key: self._normalize_value(value)
            for key, value in data.items()
        }

        df = pd.DataFrame(
            [flat_data]
        )

        df.to_csv(
            path,
            index=False
        )

        return path

    def save_text(
        self,
        filename,
        text
    ):

        path = os.path.join(
            self.analysis_folder,
            filename + ".txt"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(text)

        return path

    def save_pdf(
        self,
        filename,
        data
    ):

        path = os.path.join(
            self.analysis_folder,
            filename + ".pdf"
        )

        doc = SimpleDocTemplate(path)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>QuantEdge AI Financial Report</b>",
                styles["Title"]
            )
        )

        story.append(
            Spacer(
                1,
                20
            )
        )

        story.append(
            Paragraph(
                f"Generated : {datetime.now()}",
                styles["Normal"]
            )
        )

        story.append(
            Spacer(
                1,
                20
            )
        )

        for key, value in data.items():

            story.append(
                Paragraph(
                    f"<b>{key}</b>",
                    styles["Heading2"]
                )
            )

            story.append(
                Paragraph(
                    str(value),
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(
                    1,
                    10
                )
            )

        doc.build(story)

        return path

    def save_all(
        self,
        filename,
        data
    ):

        json_file = self.save_json(
            filename,
            data
        )

        csv_file = self.save_csv(
            filename,
            data
        )

        pdf_file = self.save_pdf(
            filename,
            data
        )

        return {

            "JSON": json_file,

            "CSV": csv_file,

            "PDF": pdf_file

        }