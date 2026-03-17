import requests
from bs4 import BeautifulSoup

def fetch_url_content(url: str):
    try:
        # We use verify=False to bypass SSL issues during development.
        # User-Agent is set to a common browser to avoid basic blocking by some sites.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, timeout=10, headers=headers, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Pull metadata first, which is useful for Single Page Apps (SPAs)
        title = soup.title.string if soup.title else ""
        meta_desc = ""
        desc_tag = soup.find("meta", attrs={"name": "description"}) or \
                    soup.find("meta", attrs={"property": "og:description"}) or \
                    soup.find("meta", attrs={"name": "twitter:description"})
        if desc_tag:
            meta_desc = desc_tag.get("content", "")

        # Clean up the HTML by removing non-content tags
        blacklist = ["script", "style", "nav", "footer", "form", "button", "svg", "path", "iframe", "noscript", "canvas"]
        for tag in soup(blacklist):
            tag.decompose()
            
        # Focus on the body content
        body_node = soup.find("body") or soup
        body_text = body_node.get_text(separator=" ")
            
        # Merge titles and descriptions with the main body text
        combined_content = f"Title: {title}\nDescription: {meta_desc}\nBody Content: {body_text}"
        
        # Normalize whitespace and line breaks
        lines = (line.strip() for line in combined_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        # If we couldn't find much text, at least return the metadata
        if len(clean_text.strip()) < 30:
            return f"Website Metadata: {title} {meta_desc}"
            
        return clean_text[:10000]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        raise Exception(f"Failed to fetch content from URL: {str(e)}")