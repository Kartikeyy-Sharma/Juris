import re


class TOCRemover:

    # TOC lines end with dots then a page number: "Some Title .......... 12"
    TOC_LINE_PATTERN = re.compile(
        r'\.{3,}\s*\d+\s*$',
        re.MULTILINE
    )

    # Chapter heading on its own line: "CHAPTER I" or "CHAPTER 1"
    CHAPTER_HEADING_PATTERN = re.compile(
        r'^(CHAPTER\s+(?:[IVXLCDM]+|\d+))\s*$',
        re.IGNORECASE | re.MULTILINE
    )

    # Real section line: "1. Short title.—" or "2. Definitions.—"
    SECTION_PATTERN = re.compile(
        r'^\d+\.\s+[A-Z][a-zA-Z\s,]+[.—]',
        re.MULTILINE
    )

    def remove_toc(self, text: str) -> str:

        chapter_matches = list(
            self.CHAPTER_HEADING_PATTERN.finditer(text)
        )

        # no chapter headings found — return full text
        if not chapter_matches:
            return text

        for match in chapter_matches:

            # inspect 500 chars after this chapter heading
            lookahead_start = match.end()
            lookahead_text = text[lookahead_start: lookahead_start + 500]

            is_toc_block = bool(
                self.TOC_LINE_PATTERN.search(lookahead_text)
            )
            has_real_sections = bool(
                self.SECTION_PATTERN.search(lookahead_text)
            )

            # real chapter: no dot-lines, has actual section content
            if not is_toc_block and has_real_sections:
                return text[match.start():]

        # fallback — start from last chapter match
        return text[chapter_matches[-1].start():]