import pytest
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch):
    async def mock_pdf_parser(file):
        print("✅ mock_pdf_parser was called")
        return "This is a test pdf file."
    
    monkeypatch.setattr("app.services.documents.parser.parse_pdf", mock_pdf_parser)

def test_upload_pdf():
# when I upload a pdf file I should get 200 status and recieve the number of chunks and embeddings created.
    content = b"This is a test pdf."
    file = {"file": ("test.pdf", io.BytesIO(content), "application/pdf")}

    response = client.post("/api/v1/document_upload/upload/", files=file)

    assert response.status_code == 200
    assert response.json() == {
        "chunks": 1,
        "embeddings": 1
    }


def test_upload_non_pdf():
# when I upload a file that is not a pdf, I should get 400 response
    content = b"This is a test pdf."
    file = {"file": ("test.text", io.BytesIO(content), "text")}

    response = client.post("/api/v1/document_upload/upload/", files=file)

    assert response.status_code == 400