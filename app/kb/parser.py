import fitz


class PDFParser:

    def extract_text(self, pdf_path: str) -> str:
       
        # Extract raw text from PDF file.

        # open PDF
        doc = fitz.open(pdf_path)

        full_text = ""

        # iterate through pages
        for page in doc:

            # extract text
            text = page.get_text()

            full_text += text

        return full_text