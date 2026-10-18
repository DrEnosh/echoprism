# EchoPrism ⚡ Information Overload Eliminator
### Category: RESEARCH & LEARNING | PR & Corporate Communications Intelligence

> **The Problem:** Important industry developments are buried under repetitive articles, syndicated press releases, newsletter clutter, and media echo chambers. Reading 30 outlets covering the exact same event wastes hours and causes acute cognitive overload.
>
> **The Solution:** **EchoPrism** is an intelligent news briefing and media intelligence platform that ingests multi-source coverage, groups stories discussing the same underlying development, purges duplicate and syndicated wire copy, and synthesizes executive PR briefings with verified source links.

---

## 🌟 Key Features

1. **Intelligent Story Clustering**:
   - Uses hybrid semantic vectorization (TF-IDF + Title n-grams + Entity / Proper Noun overlap) to group disparate articles discussing the same real-world development.
   - Automatically identifies the **Primary Story Anchor** (e.g. original press wire or in-depth investigative scoop).

2. **Syndicated Duplicate & Noise Purging**:
   - Detects near-verbatim republishing across wire syndicates, automated bots, and content aggregators.
   - Quantifies **Noise Elimination Metrics**:
     - *Articles Analyzed vs. Core Developments Identified*
     - *% Redundant Noise Eliminated* (e.g., 85% noise reduction)
     - *Executive Reading Time Saved* (e.g., 47 minutes saved down to a 2-minute brief).

3. **Executive PR Briefing & Signal Synthesis**:
   - Powered by **Google Gemini 3.8 Flash** (`gemini-3.8-flash`) via the modern `google-genai` SDK.
   - **Zero-Config Local NLP Engine Fallback**: Works offline out-of-the-box without requiring an API key.
   - For every clustered development:
     - 🔴 / 🟡 / 🟢 **Signal Level & Materiality Rationale** (High/Medium/Low impact ranking).
     - **Executive TL;DR**: 2-sentence crisp takeaway.
     - **What Happened**: Objective timeline of verified facts.
     - **Why It Matters (PR & Strategy)**: Reputational, messaging, and competitive ramifications.
     - **Cross-Outlet Framing Analysis**: Direct comparison of how company PR spin vs. tech press vs. financial media framed the story.
     - **Key Quotes & Spokespeople**: Extracted pull quotes with attribution.
     - **Actionable PR Takeaway**: Concrete comms recommendation.
     - **Verified Source Links**: Direct clickable links with publication name and timestamp.

4. **Multi-Source Ingestion**:
   - **Curated Real-World Presets**:
     - *Tech & AI Ecosystem Wave* (20 articles covering frontier models, semiconductor export bans, publisher copyright suits).
     - *Corporate Crisis Comms* (10 articles covering global cloud authentication outage & executive resignation).
     - *Biotech & Pharma M&A* (5 articles covering a $14B oncology acquisition).
   - **Live URL Ingestion**: Paste any list of article URLs; scrapes and cleans article text automatically.
   - **Live RSS & Search**: Enter any search keyword (via Google News RSS) or custom RSS feed URL.
   - **Raw Text / Newsletter Parsing**: Paste email newsletters, Substack posts, or multi-article text dumps.

5. **Multi-Format Export**:
   - One-click copy formatted Markdown brief to clipboard (ready for Slack, Teams, Notion, or internal email).
   - Download standalone, styled executive HTML report.

---

## 🚀 Quickstart

### 1. Launch the Modern Web Application (Recommended)
From the project folder, run:
```bash
python run.py
```
This automatically starts the local FastAPI server and opens your browser at `http://localhost:8000`.

### 2. Launch the Streamlit Dashboard (Alternative)
If you prefer a Streamlit data app experience:
```bash
streamlit run streamlit_app.py
```
or:
```bash
python run.py --streamlit
```

---

## 📁 Project Architecture

```
c:\Users\enosh\Desktop\AI for PR\
├── app.py                  # FastAPI application backend and REST endpoints
├── streamlit_app.py        # Interactive Streamlit dashboard
├── run.py                  # One-command browser launcher
├── requirements.txt        # Python dependency manifest
├── README.md               # Product documentation & guide
│
├── core/
│   ├── config.py           # Configuration, models, and thresholds
│   ├── datasets.py         # Curated realistic multi-outlet PR news waves
│   ├── ingestion.py        # URL scraper, RSS feed reader & text parser
│   ├── clustering.py       # Hybrid TF-IDF + Entity clustering & deduplication engine
│   ├── summarizer.py       # Gemini 3.8 Flash & Local NLP synthesis engine
│   └── export.py           # Markdown & styled HTML report generators
│
└── static/
    ├── index.html          # Modern, responsive UI with Tailwind & Lucide icons
    ├── style.css           # Glassmorphism styling and custom animations
    └── app.js              # Client state management, filtering & reactive views
```

---

## 🔑 AI Configuration

- **Default Model:** `gemini-3.8-flash`
- **API Key:** Can be set in your environment as `GEMINI_API_KEY`, or entered directly in the UI via the **API Settings** modal in the header (stored securely in your local browser storage).
- **Offline / Local Mode:** If no API key is provided, EchoPrism seamlessly falls back to its built-in rule-based NLP engine, ensuring 100% functionality without any external dependencies or costs.
