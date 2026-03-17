import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.job import Job

client = TestClient(app)

@pytest.fixture
def mock_db():
    with patch("app.api.routes.SessionLocal") as mock:
        yield mock

@pytest.fixture
def mock_celery():
    with patch("app.api.routes.process_job.delay") as mock:
        yield mock

@pytest.fixture
def mock_cache():
    with patch("app.api.routes.get_cached") as mock:
        yield mock

def test_submit_text_success(mock_db, mock_celery, mock_cache):
    mock_cache.return_value = None
    mock_session = mock_db.return_value
    
    response = client.post("/submit", json={"text": "Test text"})
    
    assert response.status_code == 200
    assert "job_id" in response.json()
    assert response.json()["status"] == "queued"
    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_celery.called

def test_submit_url_success(mock_db, mock_celery, mock_cache):
    mock_cache.return_value = None
    
    response = client.post("/submit", json={"url": "https://example.com"})
    
    assert response.status_code == 200
    assert response.json()["status"] == "queued"

def test_submit_no_data(mock_db):
    response = client.post("/submit", json={})
    assert response.status_code == 400
    assert "Either 'text' or 'url' must be provided" in response.json()["detail"]

def test_submit_cached(mock_db, mock_cache):
    mock_cache.return_value = b"Cached Summary"
    mock_session = mock_db.return_value
    
    response = client.post("/submit", json={"text": "Test text"})
    
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert "job_id" in response.json()
    assert mock_session.add.called

def test_get_status_success(mock_db):
    mock_session = mock_db.return_value
    mock_job = Job(id="test-id", status="processing")
    mock_session.query.return_value.filter.return_value.first.return_value = mock_job
    
    response = client.get("/status/test-id")
    
    assert response.status_code == 200
    assert response.json()["job_id"] == "test-id"
    assert response.json()["status"] == "processing"

def test_get_result_not_found(mock_db):
    mock_session = mock_db.return_value
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    response = client.get("/result/non-existent")
    assert response.status_code == 404
