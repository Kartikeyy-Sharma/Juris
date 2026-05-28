import re
from app.kb.tokenizer import count_tokens
from app.kb.meta_extractor import MetaExtractor


class AdaptiveChunking:

    def __init__(self, max_tokens=500):
        self.max_tokens     = max_tokens
        self.meta_extractor = MetaExtractor()
        self.doc_meta       = None

    def chunk_section(self, section_node, source=""):

        section_text = section_node.text
        tokens       = count_tokens(section_text)

        print(f"\n{section_node.title}")
        print(f"Token Count: {tokens}")

        # ONCE per document
        if self.doc_meta is None:
            print("[META] Extracting document metadata...")
            self.doc_meta = self.meta_extractor.extract_from_preliminary(section_text)

        chapter_number = section_node.metadata.get("chapter_number", "")
        chapter_title  = section_node.metadata.get("chapter_title", "")
        section_number = section_node.metadata.get("section_number", "")
        section_title  = section_node.metadata.get("section_title", "")

        print(f"[META] Chapter : {chapter_number} — {chapter_title}")
        print(f"[META] Section : {section_number} — {section_title}")

        base_metadata = {
            "source":         source,
            "act_name":       self.doc_meta.get("act_name", ""),
            "year":           self.doc_meta.get("year", ""),
            "jurisdiction":   self.doc_meta.get("jurisdiction", ""),
            "chapter_number": chapter_number,
            "chapter_title":  chapter_title,
            "section_number": section_number,
            "section_title":  section_title,
        }

        if tokens <= self.max_tokens:

            return [
                {
                    "chunk_type": "section",
                    "text":       section_text,
                    "metadata":   {
                        **base_metadata,
                        "chunk_id":    self.meta_extractor.generate_chunk_id(),
                        "clause_id":   None,
                        "clause_type": None    # batch mein set hoga baad mein
                    }
                }
            ]

        else:
            return self.clause_wise_chunking(
                section_text,
                parent_context=section_node.title,
                base_metadata=base_metadata
            )

    def clause_wise_chunking(self, text, parent_context="", base_metadata=None):

        base_metadata  = base_metadata or {}
        clause_pattern = r'\(([a-z]+)\)'
        matches        = list(re.finditer(clause_pattern, text))

        if len(matches) == 0:

            return [
                {
                    "chunk_type": "section",
                    "text":       text,
                    "metadata":   {
                        **base_metadata,
                        "chunk_id":    self.meta_extractor.generate_chunk_id(),
                        "clause_id":   None,
                        "clause_type": None    # batch mein set hoga
                    }
                }
            ]

        valid_matches   = []
        expected_letter = "a"

        for match in matches:
            clause_id = match.group(1)
            if len(clause_id) != 1:
                continue
            if clause_id == expected_letter:
                valid_matches.append(match)
                expected_letter = chr(ord(expected_letter) + 1)

        preamble            = text[:valid_matches[0].start()].strip() if valid_matches else ""
        full_parent_context = f"{parent_context}\n{preamble}" if preamble else parent_context

        chunks = []

        for i, current_match in enumerate(valid_matches):

            clause_id   = current_match.group(1)
            start       = current_match.start()
            end         = valid_matches[i + 1].start() if i + 1 < len(valid_matches) else len(text)
            clause_text = text[start:end].strip()

            enriched_text = f"{full_parent_context}\n{clause_text}" if full_parent_context else clause_text

            chunks.append(
                {
                    "chunk_type": "clause",
                    "text":       enriched_text,
                    "metadata":   {
                        **base_metadata,
                        "chunk_id":    self.meta_extractor.generate_chunk_id(),
                        "clause_id":   clause_id,
                        "clause_type": None    # batch mein set hoga
                    }
                }
            )

        return chunks