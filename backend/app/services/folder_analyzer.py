import os

from docx import Document
from pypdf import PdfReader


class FolderAnalyzer:

    def read_txt(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    def read_docx(self, file_path):

        doc = Document(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

        return text

    def read_pdf(self, file_path):

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    def extract_text_from_file(
        self,
        file_path: str
    ):

        try:

            # TXT
            if file_path.lower().endswith(".txt"):

                return self.read_txt(file_path)

            # DOCX
            elif file_path.lower().endswith(".docx"):

                return self.read_docx(file_path)

            # PDF
            elif file_path.lower().endswith(".pdf"):

                return self.read_pdf(file_path)

            else:

                return ""

        except Exception as e:

            print(
                f"Error reading file {file_path}: {e}"
            )

            return ""

    def extract_text_from_folder(
        self,
        folder_path: str
    ):

        combined_text = ""

        for file_name in os.listdir(folder_path):

            file_path = os.path.join(
                folder_path,
                file_name
            )

            try:

                # TXT
                if file_name.lower().endswith(".txt"):

                    combined_text += (
                        self.read_txt(file_path)
                        + "\n"
                    )

                # DOCX
                elif file_name.lower().endswith(".docx"):

                    combined_text += (
                        self.read_docx(file_path)
                        + "\n"
                    )

                # PDF
                elif file_name.lower().endswith(".pdf"):

                    combined_text += (
                        self.read_pdf(file_path)
                        + "\n"
                    )

            except Exception as e:

                print(
                    f"Error reading {file_name}: {e}"
                )

        return combined_text