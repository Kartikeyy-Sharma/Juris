import re
from app.models.legal_node import LegalNode


class TreeBuilder:

    def build_section_nodes(self, text: str):

        # normalize
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\n{3,}', '\n\n', text)

        # chapter pattern: "CHAPTER I" or "CHAPTER II" followed by chapter name
        chapter_pattern = re.compile(
            r'CHAPTER\s+([IVXLCDM\d]+)\s*\n([A-Z][A-Z\s]+)',
            re.MULTILINE
        )

        # section pattern: "1. Short title..."
        section_pattern = re.compile(
            r'^(\d+)\.\s+([A-Z][^\n]+)$',
            re.MULTILINE
        )

        # build chapter map — position to chapter info
        chapter_map = []
        for m in chapter_pattern.finditer(text):
            chapter_map.append({
                "start":  m.start(),
                "number": m.group(1).strip(),
                "title":  m.group(2).strip()
            })

        print(f"[TREE] Chapters found: {len(chapter_map)}")
        for c in chapter_map:
            print(f"       Chapter {c['number']} — {c['title']} at pos {c['start']}")

        def get_chapter_for_pos(pos):
            """Return chapter that appears before this position."""
            current = {"number": "", "title": ""}
            for chapter in chapter_map:
                if chapter["start"] <= pos:
                    current = chapter
                else:
                    break
            return current

        matches       = list(section_pattern.finditer(text))
        section_nodes = []

        for i, current_match in enumerate(matches):

            section_number = current_match.group(1)
            section_title  = current_match.group(2).strip()

            # clean trailing ".—" or "—" or "."
            section_title = re.sub(r'[.—].*$', '', section_title).strip()

            start = current_match.start()
            end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)

            section_body = text[start:end].strip()

            # get chapter this section belongs to
            chapter = get_chapter_for_pos(start)

            node = LegalNode(
                node_type="section",
                title=f"Section {section_number}",
                text=section_body,
                metadata={                               # 👈 yeh missing tha
                    "section_number": section_number,
                    "section_title":  section_title,
                    "chapter_number": chapter["number"],
                    "chapter_title":  chapter["title"],
                }
            )

            section_nodes.append(node)

        return section_nodes