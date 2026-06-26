import fitz
import os


class PDFReader:

    def __init__(self, uploaded_file):

        self.uploaded_file = uploaded_file

        self.document = None

    def load_pdf(self):

        try:

            pdf_bytes = self.uploaded_file.read()

            self.document = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            return True

        except Exception as e:

            print(f"Error loading PDF: {e}")

            return False

    def get_page_count(self):

        if self.document:

            return self.document.page_count

        return 0

    def extract_text(self):

        if self.document is None:

            return ""

        text = ""

        for page in self.document:

            text += page.get_text()

            text += "\n"

        return text

    def extract_pages(self):

        if self.document is None:

            return []

        pages = []

        for i, page in enumerate(self.document):

            pages.append({

                "page": i + 1,

                "text": page.get_text()

            })

        return pages

    def get_metadata(self):

        if self.document is None:

            return {}

        meta = self.document.metadata

        return {

            "Title": meta.get("title"),

            "Author": meta.get("author"),

            "Subject": meta.get("subject"),

            "Keywords": meta.get("keywords"),

            "Creator": meta.get("creator"),

            "Producer": meta.get("producer"),

            "Pages": self.document.page_count

        }

    def word_count(self):

        text = self.extract_text()

        return len(text.split())

    def character_count(self):

        text = self.extract_text()

        return len(text)

    def close(self):

        if self.document:

            self.document.close()