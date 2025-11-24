from flask import Flask, render_template, request
from checker import process_text, extract_text_from_pdf_bytes

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    corrected_text = ""
    spelling_mistakes = []
    grammar_issues = []
    original_text = ""

    if request.method == "POST":
        original_text = request.form.get("text", "")
        corrected_text, spelling_mistakes, grammar_issues = process_text(original_text)

    return render_template(
        "index.html",
        original_text=original_text,
        corrected_text=corrected_text,
        spelling_count=len(spelling_mistakes),
        spelling_mistakes=", ".join(spelling_mistakes),
        grammar_count=len(grammar_issues),
        corrected_grammar=", ".join(grammar_issues),
        corrected_file_text=None,
    )


@app.route("/grammar", methods=["POST"])
def grammar():
    file = request.files.get("file")
    corrected_file_text = ""
    file_spelling_mistakes = []
    corrected_file_grammar = []
    original_file_name = ""

    if file:
        original_file_name = file.filename
        raw_bytes = file.read()
        text = extract_text_from_pdf_bytes(raw_bytes)
        corrected_file_text, file_spelling_mistakes, corrected_file_grammar = process_text(text)

    return render_template(
        "index.html",
        original_file_name=original_file_name,
        corrected_file_text=corrected_file_text,
        file_spelling_count=len(file_spelling_mistakes),
        file_spelling_mistakes=", ".join(file_spelling_mistakes),
        file_grammar_count=len(corrected_file_grammar),
        corrected_file_grammar=", ".join(corrected_file_grammar),
        corrected_text=None,
        original_text=""
    )

# main
if __name__ == "__main__":
    app.run(debug=True)
