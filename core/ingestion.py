import re
import uuid
import urllib.parse
from typing import List, Dict, Any, Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import feedparser

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def clean_text(text: str) -> str:
    """Removes excessive whitespace and common boilerplate."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_domain(url: str) -> str:
    """Extract clean domain name from URL."""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc or parsed.path
        domain = re.sub(r"^www\.", "", domain)
        return domain
    except Exception:
        return "web-source"

def fetch_article_from_url(url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
    """Fetches and extracts clean article content from a web URL."""
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        html = resp.text

        soup = BeautifulSoup(html, "html.parser")

        # Extract title
        title = ""
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title["content"]
        elif soup.title and soup.title.string:
            title = soup.title.string

        # Extract source / site name
        source = ""
        og_site = soup.find("meta", property="og:site_name")
        if og_site and og_site.get("content"):
            source = og_site["content"]
        else:
            source = extract_domain(url)

        # Extract publication date
        date_str = ""
        date_meta = soup.find("meta", property="article:published_time") or soup.find("meta", attrs={"name": "publication_date"})
        if date_meta and date_meta.get("content"):
            date_str = date_meta["content"][:16].replace("T", " ")
        else:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Extract author
        author = ""
        author_meta = soup.find("meta", attrs={"name": "author"}) or soup.find("meta", property="article:author")
        if author_meta and author_meta.get("content"):
            author = author_meta["content"]
        else:
            author = source

        # Remove script, style, nav, footer, ads
        for tag in soup(["script", "style", "nav", "footer", "aside", "header", "form", "noscript"]):
            tag.decompose()

        # Extract main text
        paragraphs = [p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 30]
        content = " ".join(paragraphs)
        content = clean_text(content)

        if not content or len(content) < 60:
            # Fallback to general body text
            body_text = soup.get_text(separator=" ", strip=True)
            content = clean_text(body_text)[:2500]

        if not title:
            title = content[:80] + "..." if len(content) > 80 else "Article from " + source

        return {
            "id": f"url-{uuid.uuid4().hex[:8]}",
            "title": clean_text(title),
            "source": clean_text(source),
            "url": url,
            "date": date_str,
            "author": clean_text(author) if author else source,
            "content": content
        }

    except Exception as e:
        print(f"Error fetching article from {url}: {e}")
        return None

def fetch_articles_from_urls(urls: List[str]) -> List[Dict[str, Any]]:
    """Fetches articles from a list of URLs."""
    articles = []
    for u in urls:
        u = u.strip()
        if not u:
            continue
        art = fetch_article_from_url(u)
        if art and len(art.get("content", "")) > 40:
            articles.append(art)
    return articles

def fetch_articles_from_rss(feed_url_or_query: str, limit: int = 15) -> List[Dict[str, Any]]:
    """
    Fetches articles from an RSS feed or uses Google News RSS query.
    Example feed_url_or_query: 'https://techcrunch.com/feed/' or 'OpenAI PR' or 'Apple Antitrust'
    """
    feed_url = feed_url_or_query.strip()
    if not (feed_url.startswith("http://") or feed_url.startswith("https://")):
        # Treat as Google News RSS query
        encoded_query = urllib.parse.quote_plus(feed_url)
        feed_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries[:limit]:
        title = entry.get("title", "")
        link = entry.get("link", "")
        published = entry.get("published", "") or entry.get("updated", "")
        summary = entry.get("summary", "") or entry.get("description", "")

        # Clean HTML in summary
        summary_clean = BeautifulSoup(summary, "html.parser").get_text(separator=" ", strip=True)

        # Clean source name from Google News title format (e.g. "Headline - Source Name")
        source = ""
        if " - " in title:
            parts = title.rsplit(" - ", 1)
            title = parts[0].strip()
            source = parts[1].strip()

        if not source:
            source = extract_domain(link) if link else "News Feed"

        # Format date
        date_str = published[:16].replace("T", " ") if published else datetime.now().strftime("%Y-%m-%d %H:%M")

        articles.append({
            "id": f"rss-{uuid.uuid4().hex[:8]}",
            "title": clean_text(title),
            "source": clean_text(source),
            "url": link,
            "date": date_str,
            "author": source,
            "content": clean_text(summary_clean) if len(summary_clean) > 50 else clean_text(title)
        })

    return articles

def parse_raw_text_articles(raw_text: str) -> List[Dict[str, Any]]:
    """
    Parses pasted newsletters, press releases, or raw text blocks.
    Splits by delimiters like '---', 'Article:', 'Title:', or double newlines with header indicators.
    """
    if not raw_text or not raw_text.strip():
        return []

    # Check for explicit separators
    chunks = []
    if "---" in raw_text:
        chunks = [c.strip() for c in raw_text.split("---") if len(c.strip()) > 50]
    elif "\n\n\n" in raw_text:
        chunks = [c.strip() for c in raw_text.split("\n\n\n") if len(c.strip()) > 50]
    elif re.search(r"(?m)^(?:\d+[\.\)]|#+|\bArticle\b|\bStory\b|\bTitle:)", raw_text):
        # Split on section headings
        parts = re.split(r"(?m)(?=^(?:\d+[\.\)]|#+|\bArticle\b|\bStory\b|\bTitle:))", raw_text)
        chunks = [p.strip() for p in parts if len(p.strip()) > 50]
    else:
        # Fallback: treat whole text or split by double newline
        blocks = [b.strip() for b in raw_text.split("\n\n") if len(b.strip()) > 60]
        chunks = blocks if len(blocks) > 1 else [raw_text.strip()]

    articles = []
    for idx, chunk in enumerate(chunks, 1):
        lines = [line.strip() for line in chunk.split("\n") if line.strip()]
        if not lines:
            continue

        # Extract title from first line
        first_line = lines[0]
        first_line = re.sub(r"^(?:\d+[\.\)]|#+|\bArticle\s*\d*:?|\bTitle:?)\s*", "", first_line)
        title = first_line if len(first_line) > 10 else f"Pasted Item #{idx}"

        # Remaining lines as content
        content_lines = lines[1:] if len(lines) > 1 else lines
        content = " ".join(content_lines)

        articles.append({
            "id": f"raw-{uuid.uuid4().hex[:8]}",
            "title": clean_text(title),
            "source": f"Pasted Source #{idx}",
            "url": "",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "author": "Pasted Entry",
            "content": clean_text(content)
        })

    return articles
