import re
from app.kb.parser import PDFParser
from app.kb.tree_builder import TreeBuilder
from app.kb.chunking import AdaptiveChunking
from app.kb.vector_db import QdrantVectorStore

SOURCE = "code_on_wages.pdf"

parser       = PDFParser()
tree_builder = TreeBuilder()
chunker      = AdaptiveChunking()
vector_store = QdrantVectorStore()

text = parser.extract_text(f"data/{SOURCE}")
text = text.replace('\r\n', '\n').replace('\r', '\n')

chapter_one_pattern = re.compile(r'CHAPTER\s+I\b', re.IGNORECASE)
all_chapter_one     = list(chapter_one_pattern.finditer(text))

if all_chapter_one:
    text = text[all_chapter_one[-1].start():]

sections   = tree_builder.build_section_nodes(text)
all_chunks = []

for section in sections:
    chunks = chunker.chunk_section(section, source=SOURCE)
    all_chunks.extend(chunks)

print(f"\n[INFO] Total chunks: {len(all_chunks)}")

# ONE LLM call for all clause types — not one per chunk
all_chunks = chunker.meta_extractor.batch_classify_clause_types(all_chunks)

# store in qdrant
vector_store.create_collection()
vector_store.insert_chunks(all_chunks)

print("\nINGESTION COMPLETE")