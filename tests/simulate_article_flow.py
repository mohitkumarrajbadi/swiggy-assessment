from app.services.fetcher import fetch_url_content
from app.services.summarizer import summarize
from unittest.mock import patch, MagicMock

# Simulate a portfolio website HTML
MOCK_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Mohit's Portfolio</title>
    <script>console.log('tracking...');</script>
    <style>body { background: #f0f0f0; }</style>
</head>
<body>
    <header>
        <h1>Mohit Kumar Raj Badi</h1>
        <p>Expert Full Stack Developer & AI Enthusiast</p>
    </header>
    <nav>
        <ul><li>Home</li><li>About</li></ul>
    </nav>
    <main>
        <article>
            <h2>About Me</h2>
            <p>I build high-performance web applications and scalable AI systems. 
            I have deep expertise in Python, FastAPI, and React. 
            My mission is to solve complex problems with elegant code.</p>
        </article>
    </main>
    <footer>
        <p>Contact: mohit@example.com</p>
    </footer>
</body>
</html>
"""

@patch("app.services.fetcher.requests.get")
@patch("app.services.summarizer.requests.post")
def run_simulation(mock_post, mock_get):
    # 1. Mock Fetcher
    mock_response = MagicMock()
    mock_response.text = MOCK_HTML
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    print("--- 1. Testing FETCHER ---")
    content = fetch_url_content("https://mohit.com")
    print(f"Extracted Content:\n{content}\n")
    
    # Check that technical tags are gone but content is there
    assert "Mohit Kumar Raj Badi" in content
    assert "Full Stack Developer" in content
    assert "<script>" not in content
    assert "<style>" not in content
    assert "Home" not in content # from <nav> which is blacklisted
    
    # 2. Mock Summarizer
    mock_llm_response = MagicMock()
    mock_llm_response.status_code = 200
    mock_llm_response.json.return_value = {
        "response": "This is the personal portfolio of Mohit Kumar Raj Badi, an expert full-stack developer and AI enthusiast who specializes in building high-performance web applications and scalable AI systems."
    }
    mock_post.return_value = mock_llm_response
    
    print("--- 2. Testing SUMMARIZER ---")
    summary = summarize(content)
    print(f"Generated Summary:\n{summary}\n")
    
    assert "Mohit Kumar Raj Badi" in summary
    assert "HTML" not in summary.upper()
    assert "STRUCTURE" not in summary.upper()

if __name__ == "__main__":
    run_simulation()
    print("✅ Simulation Passed!")
