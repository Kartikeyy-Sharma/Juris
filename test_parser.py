from app.kb.parser import PDFParser


# initialize parser
parser = PDFParser()

# extract text
text = parser.extract_text(
    "data/code_on_wages.pdf"
)
parts = text.split("CHAPTER I")

print(len(parts))
# print first 10000 characters
print(text[:100000])