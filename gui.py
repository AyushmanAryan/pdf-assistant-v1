from pdf_reader import read_pdf_to_list, pages_to_context
import customtkinter as ctk
import requests
import os
from tkinter import filedialog
from llm import summarize_document
from llm import ask_document
from llm import search_keyword

pages = None
context = None
current_file_path = None

current_mode = "dark"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("PDF Assistant")
app.geometry("1000x700")

selected_pdf = ctk.StringVar(value="No PDF Selected")

def toggle_theme():
    global current_mode

    if current_mode == "dark":
        ctk.set_appearance_mode("light")
        theme_button.configure(text="🌙")
        current_mode = "light"

    else:
        ctk.set_appearance_mode("dark")
        theme_button.configure(text="☀️")
        current_mode = "dark"

def check_ollama():
    try:
        requests.get("http://localhost:11434")
        return True
    except:
        return False

def browse_pdf():
    global pages, context,current_file_path

    file_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    try:
        loaded_pages = read_pdf_to_list(file_path)

        if not loaded_pages:
            status_label.configure(
                text="Failed to load PDF"
            )
            return

        loaded_context = pages_to_context(
            loaded_pages
        )

        pages = loaded_pages
        context = loaded_context

        current_file_path = file_path
        selected_pdf.set(os.path.basename(file_path))

        status_label.configure(
            text=f"Loaded {len(pages)} pages"
        )

    except Exception as e:
        status_label.configure(
            text="Failed to load PDF"
        )

        print("ERROR:", e)

theme_button = ctk.CTkButton(
    app,
    text="☀️",
    width=40,
    command=toggle_theme
)

theme_button.place(
    relx=0.95,
    rely=0.03,
    anchor="ne"
)

title_label = ctk.CTkLabel(
    app,
    text="PDF Assistant",
    font=("Arial", 28, "bold")
)

title_label.pack(pady=20)

browse_button = ctk.CTkButton(
    app,
    text="Browse PDF",
    command=browse_pdf
)

browse_button.pack(pady=10)

pdf_label = ctk.CTkLabel(
    app,
    textvariable=selected_pdf
)

pdf_label.pack(pady=10)

status_label = ctk.CTkLabel(
    app,
    text="No PDF Loaded"
)

status_label.pack(pady=10)

ollama_status_label = ctk.CTkLabel(
    app,
    text="Checking Ollama..."
)
ollama_status_label.pack(pady=5)

output_box = ctk.CTkTextbox(
    app,
    width=800,
    height=300
)

def summarize_pdf():
    output_box.configure(state="normal")

    if context is None:
        output_box.delete("1.0", "end")
        output_box.insert(
            "1.0",
            "Please load a PDF first."
        )
        return

    output_box.delete("1.0", "end")

    output_box.insert(
        "1.0",
        "Generating summary...\n"
    )

    app.update()

    summary = summarize_document(context)

    output_box.delete("1.0", "end")

    output_box.insert(
        "1.0",
        summary
    )
    output_box.configure(state="disabled")


summarize_button = ctk.CTkButton(
    app,
    text="Summarize PDF",
    command=summarize_pdf
)

summarize_button.pack(pady=10)

def ask_question():
    output_box.configure(state="normal")

    if context is None:
        output_box.delete("1.0", "end")
        output_box.insert(
            "1.0",
            "Please load a PDF first."
        )
        return

    question = question_entry.get().strip()

    if not question:
        output_box.delete("1.0", "end")
        output_box.insert(
            "1.0",
            "Please enter a question."
        )
        return

    output_box.delete("1.0", "end")
    output_box.insert(
        "1.0",
        "Searching document...\n"
    )

    app.update()

    answer = ask_document(
        context,
        question
    )

    output_box.delete("1.0", "end")
    output_box.insert(
        "1.0",
        answer
    )
    output_box.configure(state="disabled")

question_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Ask a question..."
)
question_entry.pack(pady=5)

ask_button = ctk.CTkButton(
    app,
    text="Ask Question",
    command=ask_question
)

ask_button.pack(pady=5)
search_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Search keyword..."
)

search_entry.pack(pady=5)

def exact_search():

    if pages is None:
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", "Please load a PDF first.")
        output_box.configure(state="disabled")
        return

    keyword = search_entry.get().strip()

    if not keyword:
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", "Please enter a keyword.")
        output_box.configure(state="disabled")
        return

    results = search_keyword(pages, keyword)

    output_box.configure(state="normal")
    output_box.delete("1.0", "end")

    if not results:
        output_box.insert("1.0", "No matches found.")
    else:
        for result in results:
            output_box.insert(
                "end",
                f"\nPage {result['page']}\n"
            )
            output_box.insert(
                "end",
                f"{result['snippet']}\n"
            )

    output_box.configure(state="disabled")

search_button = ctk.CTkButton(
    app,
    text="Exact Search",
    command=exact_search
)

search_button.pack(pady=5)

output_box.pack(pady=20)
output_box.insert(
    "1.0",
    "Welcome to PDF Assistant"
)

output_box.configure(state="disabled")

if check_ollama():
    ollama_status_label.configure(text="🟢 Ollama Online", text_color="green")
else:
    ollama_status_label.configure(text="🔴 Ollama Offline", text_color="red")

app.mainloop()