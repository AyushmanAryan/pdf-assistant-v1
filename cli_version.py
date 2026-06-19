import os
from pdf_reader import read_pdf_to_list, pages_to_context
from llm import summarize_document, ask_document, search_keyword

PDF_PATH = "sample.pdf"

if not os.path.exists(PDF_PATH):
    print(f"Error: The file '{PDF_PATH}' was not found.")
    print("Please place the PDF in the same directory or check the file name.")
    exit(1)

print("Processing PDF document... Please wait.")
pages = read_pdf_to_list(PDF_PATH)

if not pages:
    print("Error: No text could be extracted from this document.")
    print("It might be empty, corrupted, or a scanned image PDF requiring OCR.")
    exit(1)

context = pages_to_context(pages)
print(f"Successfully loaded {len(pages)} pages into context!")

while True:
    print("\n" + "=" * 25)
    print("      PDF Assistant      ")
    print("=" * 25)
    print("1. Summarize PDF")
    print("2. Ask Question")
    print("3. Exact Search")
    print("4. Exit")

    choice = input("\nChoice: ")

    if choice == "1":
        print("\n[Generating Summary...]")
        answer = summarize_document(context)
        print("\n" + answer)

    elif choice == "2":
        question = input("\nQuestion: ")
        if not question.strip():
            print("Question cannot be empty.")
            continue

        print("\n[Searching document and generating answer...]")
        answer = ask_document(context, question)
        print("\n" + answer)

    elif choice == "3":
        keyword = input("\nKeyword to search: ")
        if not keyword.strip():
            print("Keyword cannot be empty.")
            continue

        results = search_keyword(pages, keyword)

        print("\n" + "-" * 30)
        print(f"Search Results for '{keyword}':")
        print("-" * 30)

        if not results:
            print("No matches found in the document.")
        else:
            for match in results:
                print(f"\n📄 Page {match['page']} ({match['chars']} characters):")
                print(f"Snippet: \"...{match['snippet'].strip()}...\"")
        print("-" * 30)

    elif choice == "4":
        print("\nGoodbye.")
        break

    else:
        print("\nInvalid choice. Please enter 1, 2, 3, or 4.")