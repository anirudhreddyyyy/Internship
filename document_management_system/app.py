import os
from flask import Flask, render_template, request, redirect
from database import db
from models import Document
from search import search_documents
import markdown
import PyPDF2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)

with app.app_context():
    db.create_all()

def extract_content(filepath):
    if filepath.endswith(".pdf"):
        reader = PyPDF2.PdfReader(filepath)
        return " ".join([page.extract_text() or "" for page in reader.pages])
    elif filepath.endswith(".md"):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    return ""

@app.route("/")
def index():
    query = request.args.get("q")
    documents = Document.query.all()
    if query:
        documents = search_documents(query, documents)
    return render_template("index.html", documents=documents)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        category = request.form["category"]

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        content = extract_content(filepath)

        doc = Document(
            filename=file.filename,
            category=category,
            content=content
        )
        db.session.add(doc)
        db.session.commit()

        return redirect("/")
    return render_template("upload.html")

@app.route("/delete/<int:doc_id>", methods=["POST"])
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], doc.filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(doc)
    db.session.commit()

    return redirect("/")

@app.route("/metadata")
def metadata():
    docs = Document.query.all()
    return "<br>".join([f"{d.id} | {d.filename} | {d.category}" for d in docs])


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)

