# EchoPrism

A news briefing tool for PR and corporate communications teams. It pulls in coverage from many outlets, groups the articles that are about the same event, drops syndicated copies, and writes one short brief per development with links back to the sources.

Built for the *Research & Learning / PR & Corporate Communications Intelligence* category.

## The problem

When something happens in an industry, thirty outlets cover it and most of them repeat the same press release or wire story. Reading all of it takes hours and tells you very little more than the first article did. EchoPrism cuts that down to the distinct developments and what each one means for communications.

## What it does

- **Story clustering.** Articles are grouped with TF-IDF, title n-grams and overlap of proper nouns and entities. The earliest or most detailed piece in each group is picked as the main story.
- **Duplicate and syndication removal.** Near-identical republished copies are flagged, and the app reports how many articles it analysed, how many distinct developments it found, the share of redundant coverage removed, and the reading time saved.
- **Briefs per development.** Each cluster gets a signal level (high, medium or low) with a short reason, a two-sentence summary, what happened, why it matters for PR and strategy, how different outlet types framed the story, key quotes with attribution, one suggested comms action, and source links with outlet name and time.
- **Several ways to bring in articles.** Three built-in sample sets (a tech and AI news wave, a corporate crisis, a biotech acquisition), a list of article URLs, a search keyword or RSS feed (Google News RSS), or pasted newsletter text.
- **Export.** Copy a Markdown brief for Slack, Teams, Notion or email, or download a styled HTML report.
- **Works without an API key.** With a Gemini key the briefs are written by the model. Without one, a built-in rule-based summarizer is used.

## Getting started

You need a recent Python 3.

```bash
pip install -r requirements.txt
python run.py
```

This starts the FastAPI server and opens `http://localhost:8000`.

To use the Streamlit version instead:

```bash
streamlit run streamlit_app.py
# or
python run.py --streamlit
```

### Gemini API key (optional)

Set `GEMINI_API_KEY` in your environment or in a local `.env` file, or paste the key into the API Settings dialog in the web UI (it stays in your browser's local storage). The default model is set in `core/config.py`.

## Project structure

```
app.py              FastAPI backend and REST endpoints
streamlit_app.py    Streamlit dashboard
run.py              Starts the server and opens the browser
requirements.txt
core/
  config.py         Model name, thresholds, PR boilerplate patterns
  datasets.py       Sample multi-outlet news sets
  ingestion.py      URL scraper, RSS reader, text parser
  clustering.py     TF-IDF and entity clustering, duplicate detection
  summarizer.py     Gemini and rule-based brief writer
  export.py         Markdown and HTML report generators
static/
  index.html        Web UI (Tailwind, Lucide icons)
  style.css
  app.js
```

## API

| Endpoint | Purpose |
| --- | --- |
| `GET /api/presets`, `GET /api/presets/{id}` | List and load the sample sets |
| `POST /api/ingest/urls` | Fetch and clean articles from URLs |
| `POST /api/ingest/rss` | Read an RSS feed or run a news search |
| `POST /api/ingest/raw` | Parse pasted text |
| `POST /api/process` | Cluster, de-duplicate and write briefs |
| `POST /api/export/markdown`, `POST /api/export/html` | Export the result |

## License

See [LICENSE](LICENSE).
