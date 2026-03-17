import pytest
from unittest.mock import patch, MagicMock
from app.services.fetcher import fetch_url_content
from app.services.summarizer import summarize

def test_fetch_url_content_success(requests_mock):
    url = "https://test.com"
    requests_mock.get(url, text="Test Content", status_code=200)
    
    content = fetch_url_content(url)
    assert content == "Test Content"

def test_fetch_url_content_failure(requests_mock):
    url = "https://fail.com"
    requests_mock.get(url, status_code=404)
    
    with pytest.raises(Exception) as excinfo:
        fetch_url_content(url)
    assert "Failed to fetch content from URL" in str(excinfo.value)

@patch("app.services.summarizer.requests.post")
def test_summarize_success(mock_post):
    # Mock successful response from Ollama
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "This is a summary."}
    mock_post.return_value = mock_response
    
    result = summarize("Some long text to summarize.")
    assert result == "This is a summary."

@patch("app.services.summarizer.requests.post")
def test_summarize_error_status(mock_post):
    # Mock error response from Ollama
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response
    
    result = summarize("Text")
    assert "Error: Inference failed with status 500" in result
