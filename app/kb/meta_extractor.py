import re
import json
import os
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class MetaExtractor:

    def __init__(self):
        self.client       = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.act_name     = None
        self.year         = None
        self.jurisdiction = None
        self.act_code     = None

    def _call_llm(self, prompt: str, max_tokens: int = 200) -> str:

        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    def extract_from_preliminary(self, preliminary_text: str):

        prompt = f"""You are a legal metadata extractor. Read the following text from a legal document and extract:
1. act_name: Full name of the Act or Code
2. act_code: A short uppercase abbreviation of the act name, 2-5 letters (e.g. "Code on Wages" -> "COW", "Income Tax Act" -> "ITA", "Factories Act" -> "FA")
3. year: Year the Act was enacted or published
4. jurisdiction: Geographic/political jurisdiction this Act applies to (e.g. "India", "State of Maharashtra")

Respond ONLY in this exact JSON format with no explanation or markdown:
{{"act_name": "...", "act_code": "...", "year": "...", "jurisdiction": "..."}}

Text:
{preliminary_text[:2000]}"""

        raw    = self._call_llm(prompt, max_tokens=200)
        raw    = re.sub(r'^```json|```$', '', raw, flags=re.MULTILINE).strip()
        parsed = json.loads(raw)

        self.act_name     = parsed.get("act_name", "")
        self.act_code     = parsed.get("act_code", "ACT").upper()
        self.year         = parsed.get("year", "")
        self.jurisdiction = parsed.get("jurisdiction", "")

        print(f"[META] Act         : {self.act_name}")
        print(f"[META] Code        : {self.act_code}")
        print(f"[META] Year        : {self.year}")
        print(f"[META] Jurisdiction: {self.jurisdiction}")

        return parsed

    def generate_chunk_id(self) -> str:

        return f"{self.act_code}_{self.year}_{uuid.uuid4()}"

    def get_clause_type(self, clause_text: str) -> str:

        prompt = f"""You are a legal document classifier. Classify the following legal clause into ONE of these types:
- definition
- prohibition
- obligation
- penalty
- procedure
- eligibility
- exemption
- power
- interpretation
- miscellaneous

Respond with ONLY the single word type, nothing else.

Clause:
{clause_text[:1000]}"""

        return self._call_llm(prompt, max_tokens=10).lower()

    def batch_classify_clause_types(self, chunks: list[dict]) -> list[dict]:
        """
        Classify ALL chunks in ONE LLM call.
        Sends all chunk texts together, gets back a JSON list of types.
        Much cheaper than one call per chunk.
        """

        print(f"\n[META] Batch classifying {len(chunks)} chunks in one LLM call...")

        # build numbered list of all chunk texts
        numbered_chunks = ""
        for i, chunk in enumerate(chunks):
            # only send first 300 chars per chunk — enough to classify
            short_text = chunk["text"][:300].replace("\n", " ")
            numbered_chunks += f'{i}: "{short_text}"\n'

        prompt = f"""You are a legal document classifier. Classify each of the following legal chunks into ONE of these types:
- definition
- prohibition
- obligation
- penalty
- procedure
- eligibility
- exemption
- power
- interpretation
- miscellaneous

Respond ONLY with a JSON array of strings in the same order as the input.
Example: ["definition", "obligation", "penalty", ...]
No explanation, no markdown, just the JSON array.

Chunks:
{numbered_chunks}"""

        # max_tokens scales with number of chunks — ~15 tokens per chunk
        max_tokens = min(len(chunks) * 15, 4000)

        raw = self._call_llm(prompt, max_tokens=max_tokens)
        raw = re.sub(r'^```json|```$', '', raw, flags=re.MULTILINE).strip()

        clause_types = json.loads(raw)

        # assign clause_type back to each chunk
        for i, chunk in enumerate(chunks):
            if i < len(clause_types):
                chunk["metadata"]["clause_type"] = clause_types[i].lower()
            else:
                chunk["metadata"]["clause_type"] = "miscellaneous"

        print(f"[META] Batch classification done")

        return chunks