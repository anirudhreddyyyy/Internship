import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from search import search_documents


class DummyDoc:
    def __init__(self, content):
        self.content = content

def test_search_documents():
    docs = [DummyDoc("hello world"), DummyDoc("python flask")]
    results = search_documents("flask", docs)
    assert len(results) == 1
