import re
from app.kb.parser import PDFParser
from app.kb.tree_builder import TreeBuilder
from app.kb.chunking import AdaptiveChunking
import logging

logger = logging.getLogger(__name__)

# initialize
parser = PDFParser()
tree_builder = TreeBuilder()
chunker = AdaptiveChunking()

# extract PDF text
text = parser.extract_text("data/code_on_wages.pdf")

# normalize line endings
text = text.replace('\r\n', '\n').replace('\r', '\n')

# ----------------------------------------------------------------
# The PDF has a long TOC listing all chapters + sections.
# Real content starts at the LAST occurrence of "CHAPTER I"
# because TOC mentions it once, actual content is the final one.
# ----------------------------------------------------------------

chapter_one_pattern = re.compile(
    r'CHAPTER\s+I\b',   # "CHAPTER I" but not "CHAPTER II", "CHAPTER III" etc.
    re.IGNORECASE
)

all_chapter_one = list(chapter_one_pattern.finditer(text))
print(f"Found {len(all_chapter_one)} occurrences of 'CHAPTER I'")
print(all_chapter_one)

if all_chapter_one:
    # last occurrence = real content, not TOC
    text = text[all_chapter_one[1].start():]
    print(f"[INFO] Starting from last CHAPTER I at char {all_chapter_one[-1].start()}")
else:
    print("[WARN] CHAPTER I not found — using full text")

# DEBUG
print("=== RAW TEXT SAMPLE (first 500 chars) ===")
print(repr(text[:500]))
print("==========================================")

# build sections
sections = tree_builder.build_section_nodes(text)

for section in sections[:5]:

    chunks = chunker.chunk_section(section)

    print(f"\nTotal Chunks: {len(chunks)}")

    for chunk in chunks:

        print("\nCHUNK TYPE:")
        print(chunk["chunk_type"])

        print("\nTEXT:")
        print(chunk["text"][:10000])

        print("\n" + "=" * 50)