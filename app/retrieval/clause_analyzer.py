import os
from openai import OpenAI
from dotenv import load_dotenv
from app.kb.vector_db import QdrantVectorStore

load_dotenv()


class ClauseAnalyzer:

    def __init__(self, top_k: int = 5):
        self.client      = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.vector_store = QdrantVectorStore()
        self.top_k        = top_k

    def retrieve(self, clause_text: str) -> list[dict]:
        """Search Qdrant for relevant legal chunks."""

        results = self.vector_store.search(
            query=clause_text,
            top_k=self.top_k
        )

        return results

    def _build_context(self, results: list[dict]) -> str:
        """Format retrieved chunks into context for LLM."""

        context = ""

        for i, r in enumerate(results):
            meta = r["metadata"]
            context += f"""
---
REFERENCE {i + 1}:
Act        : {meta.get('act_name', '')} ({meta.get('year', '')})
Chapter    : {meta.get('chapter_number', '')} — {meta.get('chapter_title', '')}
Section    : {meta.get('section_number', '')} — {meta.get('section_title', '')}
Clause     : {meta.get('clause_id', 'N/A')}
Jurisdiction: {meta.get('jurisdiction', '')}
Chunk ID   : {meta.get('chunk_id', '')}

Legal Text:
{r['text']}
---
"""
        return context

    def analyze(self, clause_text: str) -> str:
        """
        Full pipeline:
        1. Retrieve relevant legal chunks
        2. Send to LLM with clause
        3. Get structured analysis back
        """

        print("\n[RETRIEVER] Searching legal knowledge base...")
        results = self.retrieve(clause_text)
        print(f"[RETRIEVER] Found {len(results)} relevant chunks")

        context = self._build_context(results)

        prompt = f"""You are a legal expert assistant helping a common person understand if a contract clause is legally acceptable under Indian law.

You have been provided with:
1. A contract clause that a user is about to sign
2. Relevant sections from the legal knowledge base

Your job is to analyze the clause and answer the following:

---

CONTRACT CLAUSE PROVIDED BY USER:
"{clause_text}"

---

RELEVANT LEGAL KNOWLEDGE BASE:
{context}

---

Now provide your analysis in this exact structure:

## 1. Legal Acceptability
Is this clause legally acceptable under Indian law? Answer clearly YES, NO, or PARTIALLY ACCEPTABLE.
Explain why in simple language. Mention the exact legal provisions that support your answer.

## 2. Risks for the Signer
What are the risks for the person signing this clause?
- List each risk clearly
- Mention which legal provision creates or limits this risk
- Use simple language but highlight important legal terms in **bold**

## 3. Legal References
Cite the exact sources from the knowledge base that are relevant:
- Act name and year
- Chapter number and name
- Section number and name
- Clause id if applicable
- Direct quote or paraphrase of the relevant legal text

## 4. Plain Language Summary
In 3-5 sentences, explain the overall situation to someone with no legal background.
What should they know before signing?

IMPORTANT INSTRUCTIONS:
- Always cite exact references (Section number, Chapter, Act name)
- Use simple English but keep important legal terms with explanation
- Be honest — if the clause is risky, say so clearly
- If the clause contradicts a legal provision, point it out directly
- Only use the information provided in the knowledge base for your analysis. Do not assume anything beyond that.
- Do not use any information that is not in the provided legal knowledge base. If you don't find a relevant provision, say "No direct reference found in the knowledge base." and explain based on general legal principles.
"""

        print("\n[RETRIEVER] Sending to LLM for analysis...")

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=2000,
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal expert assistant. Always cite exact legal references. Be clear, honest and helpful."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()