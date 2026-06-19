import requests

MODEL = "qwen2.5:1.5b"
OLLAMA_URL = "http://localhost:11434/api/generate"
TIMEOUT = 120
TEMPERATURE = 0.2

def ask_llm(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": TEMPERATURE
                }
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()

        return response.json().get(
            "response",
            "Error: No response returned by model."
        )

    except requests.exceptions.Timeout:
        return "Error: Model took too long to respond."

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama."

    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"

    except Exception as e:
        return f"Error: {e}"

def summarize_document(context):
    prompt = f"""You are a strict PDF summarizer. Analyze the document context below.

Rules:
- Rely ONLY on the clear facts directly mentioned in the context.
- Ground your summary by adding page citations like [Page X] for key facts.
- Keep the entire output strictly under 150 words.

Context:
{context}

Generate your response using this exact structural layout:
1. Title: (Provide a clear title based on the text)
2. Summary: (A short paragraph summarizing the core theme)
3. Key Points: (Bullet points of critical takeaways with citations. Each bullet must be under 20 words)
"""
    return ask_llm(prompt)

def ask_document(context, question):
    prompt = f"""You are a precise document QA assistant.

Rules:
1. Answer ONLY using information explicitly present in the provided document context.
2. Do NOT use outside knowledge, assumptions, guesses, or prior training data.
3. Every factual statement MUST be followed by its source page in brackets, like: [Page X]
4. If a source page cannot be determined with confidence, use: [Page Uncertain]
5. Never invent, estimate, or hallucinate page numbers.
6. If the answer is not explicitly present in the document, reply EXACTLY: "Information not found in document."
7. Keep answers concise and directly relevant to the question.
8. If multiple pages support the same answer, cite all relevant pages: [Page 3, Page 5]
9. Do not mention information that is not supported by the cited pages.
10. When quoting or paraphrasing document content, preserve the original meaning.
11. Prefer exact facts from the document over interpretation.
12. If the question is ambiguous, answer using the most relevant information available in the document and cite the supporting page(s).
13. Never generate fake citations.
14. Your primary objective is factual accuracy and traceability, not creativity.

Context:
{context}

Question: {question}
Assistant:"""
    return ask_llm(prompt)

def search_keyword(pages, keyword):

    results = []
    normalized_keyword = keyword.lower()

    for page in pages:

        text = page["text"]
        lower_text = text.lower()

        if normalized_keyword in lower_text:

            position = lower_text.find(normalized_keyword)

            start = max(0, position - 100)
            end = min(len(text), position + 100)

            snippet = text[start:end]

            results.append({
                "page": page["page"],
                "chars": page["chars"],
                "snippet": snippet
            })

    return results