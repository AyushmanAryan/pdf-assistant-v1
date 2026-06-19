import re
from pypdf import PdfReader


def read_pdf_to_list(path):
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            pages.append({
                "page": i,
                "text": page_text,
                "chars": len(page_text),
                "words": len(page_text.split())
            })

    return pages


def pages_to_context(pages):
    context = (
        f"<extracted_document_context "
        f"total_pages=\"{len(pages)}\">\n"
    )

    for page in pages:
        cleaned_text = page["text"].strip()

        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)

        context += f"<page id=\"{page['page']}\">\n{cleaned_text}\n</page>\n"

    context += "</extracted_document_context>"
    return context
