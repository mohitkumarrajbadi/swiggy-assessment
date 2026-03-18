from app.services.fetcher import fetch_url_content
from app.services.summarizer import summarize
from unittest.mock import patch, MagicMock

# Simulate the user's portfolio HTML (SPA)
# Note: Body is empty other than the root div
MOCK_SPA_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <title>Mohit Kumar Raj Badi Portfolio</title>
    <meta name="description" content="This is the personal portfolio website of Mohit Kumar Raj Badi"/>
    <script src="tracking.js"></script>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>
"""

@patch("app.services.fetcher.requests.get")
@patch("app.services.summarizer.requests.post")
def run_spa_simulation(mock_post, mock_get):
    # 1. Mock Fetcher
    mock_response = MagicMock()
    mock_response.text = MOCK_SPA_HTML
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    print("--- 1. Testing SPA FETCHER ---")
    content = fetch_url_content("https://mohitkumarrajbadi.vercel.app/")
    print(f"Extracted Content:\n{content}\n")
    
    # Check that metadata is present but tech noise is gone
    assert "Mohit Kumar Raj Badi" in content
    assert "personal portfolio website" in content
    assert "tracking.js" not in content
    
    # 2. Mock Summarizer
    mock_llm_response = MagicMock()
    mock_llm_response.status_code = 200
    mock_llm_response.json.return_value = {
        "response": "This is the personal portfolio website of Mohit Kumar Raj Badi. It showcases his professional work and expertise."
    }
    mock_post.return_value = mock_llm_response
    
    print("--- 2. Testing SPA SUMMARIZER ---")
    summary = summarize(content)
    print(f"Generated Summary:\n{summary}\n")
    
    assert "Mohit Kumar Raj Badi" in summary
    assert "JavaScript" not in summary

if __name__ == "__main__":
    run_spa_simulation()
    print("✅ SPA Simulation Passed!")
