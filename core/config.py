import os
from typing import Optional
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

DEFAULT_MODEL = "gemini-3.8-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Clustering Defaults
DEFAULT_SIMILARITY_THRESHOLD = 0.32  # Stories with cosine similarity >= this are grouped
DUPLICATE_THRESHOLD = 0.72           # Stories with cosine similarity >= this are flagged as duplicate/syndicated

# PR Specific Stopwords and Boilerplate
PR_BOILERPLATE_PATTERNS = [
    r"(?i)for immediate release",
    r"(?i)safe harbor statement",
    r"(?i)forward-looking statements",
    r"(?i)about [A-Z0-9\s,\.\-]{3,40}(?:inc\.|corp\.|llc|company|technologies)?",
    r"(?i)media contact.*",
    r"(?i)investor relations.*",
    r"(?i)source: [a-z0-9\s\.,\-]+",
    r"(?i)copyright \d{4}.*",
    r"(?i)all rights reserved",
    r"(?i)view original content to download multimedia:.*"
]
