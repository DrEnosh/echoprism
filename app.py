import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from core.datasets import PRESET_DATASETS
from core.ingestion import (
    fetch_article_from_url,
    fetch_articles_from_urls,
    fetch_articles_from_rss,
    parse_raw_text_articles
)
from core.clustering import group_articles_into_clusters
from core.summarizer import generate_full_briefing
from core.export import export_to_markdown, export_to_html
from core.config import DEFAULT_MODEL, GEMINI_API_KEY

app = FastAPI(
    title="EchoPrism - Information Overload Eliminator for PR",
    description="Intelligent news clustering, duplicate elimination, and executive PR briefings.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Request Models
class ProcessRequest(BaseModel):
    articles: List[Dict[str, Any]]
    keywords: Optional[List[str]] = None
    similarity_threshold: Optional[float] = 0.08
    duplicate_threshold: Optional[float] = 0.65
    api_key: Optional[str] = None
    model: Optional[str] = DEFAULT_MODEL

class UrlIngestRequest(BaseModel):
    urls: List[str]

class RssIngestRequest(BaseModel):
    query_or_url: str
    limit: Optional[int] = 15

class RawIngestRequest(BaseModel):
    raw_text: str

class ExportRequest(BaseModel):
    briefings: List[Dict[str, Any]]
    stats: Dict[str, Any]
    title: Optional[str] = "Executive PR & Media Briefing"

# API Endpoints
@app.get("/api/presets")
def get_presets():
    """Returns metadata for all available curated datasets."""
    summary = []
    for key, data in PRESET_DATASETS.items():
        summary.append({
            "id": key,
            "title": data["title"],
            "category": data["category"],
            "description": data["description"],
            "article_count": len(data["articles"]),
            "default_keywords": data.get("default_keywords", [])
        })
    return summary

@app.get("/api/presets/{preset_id}")
def get_preset(preset_id: str):
    """Returns articles for a specific preset dataset."""
    if preset_id not in PRESET_DATASETS:
        raise HTTPException(status_code=404, detail="Preset dataset not found")
    return PRESET_DATASETS[preset_id]

@app.post("/api/ingest/urls")
def ingest_urls(req: UrlIngestRequest):
    """Scrapes and extracts clean articles from a list of URLs."""
    if not req.urls:
        raise HTTPException(status_code=400, detail="No URLs provided")
    articles = fetch_articles_from_urls(req.urls)
    return {"articles": articles, "count": len(articles)}

@app.post("/api/ingest/rss")
def ingest_rss(req: RssIngestRequest):
    """Fetches articles from an RSS feed URL or Google News query."""
    if not req.query_or_url.strip():
        raise HTTPException(status_code=400, detail="Search query or RSS URL required")
    articles = fetch_articles_from_rss(req.query_or_url, limit=req.limit or 15)
    return {"articles": articles, "count": len(articles)}

@app.post("/api/ingest/raw")
def ingest_raw(req: RawIngestRequest):
    """Parses raw text, newsletter dump, or multiple pasted press releases."""
    articles = parse_raw_text_articles(req.raw_text)
    return {"articles": articles, "count": len(articles)}

@app.post("/api/process")
def process_articles(req: ProcessRequest):
    """
    Main pipeline:
    1. Filters articles by keywords (if provided)
    2. Clusters articles covering the same development
    3. Identifies and isolates redundant/syndicated duplicate copies
    4. Computes noise reduction and time saved metrics
    5. Synthesizes an executive PR briefing with Gemini 3.8 Flash (or local NLP fallback)
    """
    if not req.articles:
        raise HTTPException(status_code=400, detail="No articles provided for processing")

    # 1 & 2. Clustering & Deduplication
    clustered_res = group_articles_into_clusters(
        articles=req.articles,
        similarity_threshold=req.similarity_threshold or 0.08,
        duplicate_threshold=req.duplicate_threshold or 0.65,
        keywords=req.keywords
    )

    clusters = clustered_res["clusters"]
    stats = clustered_res["stats"]

    # 3. Summarization & Executive Briefing
    briefings = generate_full_briefing(
        clusters=clusters,
        api_key=req.api_key,
        model_name=req.model or DEFAULT_MODEL
    )

    return {
        "briefings": briefings,
        "clusters": clusters,
        "stats": stats
    }

@app.post("/api/export/markdown")
def export_markdown_endpoint(req: ExportRequest):
    """Exports briefing to clean markdown."""
    md_content = export_to_markdown(req.briefings, req.stats, req.title or "Executive PR Briefing")
    return {"markdown": md_content}

@app.post("/api/export/html")
def export_html_endpoint(req: ExportRequest):
    """Exports briefing to standalone styled HTML."""
    html_content = export_to_html(req.briefings, req.stats, req.title or "Executive PR Briefing")
    return {"html": html_content}

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>EchoPrism API is running</h1>")

if __name__ == "__main__":
    import uvicorn
    print("Starting EchoPrism Server on http://localhost:8000...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
