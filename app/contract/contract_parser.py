import pdfplumber

class ContractParser:

    def extract_text(self, pdf_path: str) -> str:
        """Extract raw text from the contract PDF."""

        full_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        
        print(f"[PARSER] Extracted {len(full_text)} characters from {pdf_path}")

        return full_text.strip()
    