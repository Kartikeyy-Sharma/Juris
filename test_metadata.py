from app.kb.meta_extractor import MetaExtractor
from app.kb.parser import PDFParser
from app.kb.tree_builder import TreeBuilder
from app.kb.chunking import AdaptiveChunking
import re


# --- TEST 1: MetaExtractor ---
sample_text = """
Code on Wages, 2019
ACT NO. 29 OF 2019

1. Short title, extent and commencement.—(1) This Act may be called 
the Code on Wages, 2019.
(2) It extends to the whole of India.
(3) It shall come into force on such date as the Central Government 
may, by notification in the Official Gazette, appoint.
"""

extractor = MetaExtractor()

print("\n--- TEST 1: extract_from_preliminary ---")
meta = extractor.extract_from_preliminary(sample_text)
print(f"Result: {meta}")

print("\n--- TEST 2: generate_chunk_id ---")
print(extractor.generate_chunk_id())
print(extractor.generate_chunk_id())

print("\n--- TEST 3: get_clause_type ---")
test_clause = '"employee" means any person employed on wages by an establishment.'
print(f"Clause type: {extractor.get_clause_type(test_clause)}")


# --- TEST 4: Full chunk metadata from real PDF ---
print("\n--- TEST 4: Full chunk metadata from PDF ---")

parser       = PDFParser()
tree_builder = TreeBuilder()
chunker      = AdaptiveChunking()

text = parser.extract_text("data/code_on_wages.pdf")
text = text.replace('\r\n', '\n').replace('\r', '\n')

# skip TOC
chapter_one_pattern = re.compile(r'CHAPTER\s+I\b', re.IGNORECASE)
all_chapter_one     = list(chapter_one_pattern.finditer(text))
if all_chapter_one:
    text = text[all_chapter_one[-1].start():]

sections = tree_builder.build_section_nodes(text)

# test first 2 sections
for section in sections[:2]:

    chunks = chunker.chunk_section(section, source="code_on_wages.pdf")

    for chunk in chunks[:2]:   # first 2 chunks per section

        print("\nCHUNK TYPE   :", chunk["chunk_type"])
        print("METADATA:")
        for key, value in chunk["metadata"].items():
            print(f"  {key:20} : {value}")
        print("-" * 50)