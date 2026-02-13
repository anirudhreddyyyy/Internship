import os
import io
import pytest
import shutil
from app import app, db
from models import Document

# ----------------------------
# TEST CONFIGURATION
# 000
# ----------------------------

@pytest.fixture
def client():
    # Setup
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["UPLOAD_FOLDER"] = "test_uploads"
    
    # Ensure the test upload directory exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()
    
    # Teardown: Remove the test uploads folder after tests
    if os.path.exists(app.config["UPLOAD_FOLDER"]):
        shutil.rmtree(app.config["UPLOAD_FOLDER"])

# ----------------------------
# TESTS
# ----------------------------

def test_index_page(client):
    """Test if the home page loads correctly."""
    response = client.get("/")
    assert response.status_code == 200

def test_upload_document(client):
    """Test uploading a markdown file."""
    data = {
        "file": (io.BytesIO(b"Test content"), "test.md"),
        "category": "Test Category"
    }

    # Follow_redirects=True helps see the final page after the 302
    response = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert response.status_code == 200 

    with app.app_context():
        doc = Document.query.filter_by(filename="test.md").first()
        assert doc is not None
        assert doc.category == "Test Category"
        assert "Test content" in doc.content

def test_search_functionality(client):
    """Test if the search filter works on the index page."""
    with app.app_context():
        doc1 = Document(filename="python_doc.md", category="Tech", content="Python testing")
        doc2 = Document(filename="finance_doc.md", category="Finance", content="Banking data")
        db.session.add_all([doc1, doc2])
        db.session.commit()

    # Search for Python
    response = client.get("/?q=Python")
    assert b"python_doc.md" in response.data
    assert b"finance_doc.md" not in response.data

def test_extract_md_file(tmp_path):
    """Unit test for the content extraction logic."""
    from app import extract_content
    
    test_file = tmp_path / "sample.md"
    test_file.write_text("Hello Markdown")
    
    content = extract_content(str(test_file))
    assert content == "Hello Markdown"