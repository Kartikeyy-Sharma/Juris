from app.kb.parser import PDFParser
from app.kb.tree_builder import TreeBuilder


# initialize parser
parser = PDFParser()

# extract PDF text
text = parser.extract_text(
    "data/code_on_wages.pdf"
)

# initialize tree builder
tree_builder = TreeBuilder()

# build section nodes
sections = tree_builder.build_section_nodes(text)

# print first 10 sections
for section in sections[:10]:

    print(section.title)

    print(section.text[:1000])

    print("-" * 50)