import os
import streamlit as st
from datetime import datetime
from core.datasets import PRESET_DATASETS
from core.ingestion import (
    fetch_articles_from_urls,
    fetch_articles_from_rss,
    parse_raw_text_articles
)
from core.clustering import group_articles_into_clusters
from core.summarizer import generate_full_briefing
from core.export import export_to_markdown, export_to_html
from core.config import DEFAULT_MODEL, GEMINI_API_KEY

st.set_page_config(
    page_title="EchoPrism | Information Overload Eliminator",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 800; color: #0284c7; margin-bottom: 0px; }
    .sub-header { font-size: 0.95rem; color: #64748b; margin-bottom: 20px; }
    .metric-box { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; }
    .metric-value { font-size: 1.8rem; font-weight: 800; color: #38bdf8; }
    .metric-label { font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; }
    .badge-high { background-color: #7f1d1d; color: #fca5a5; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; }
    .badge-med { background-color: #78350f; color: #fde68a; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; }
    .badge-low { background-color: #064e3b; color: #a7f3d0; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📢 EchoPrism: Information Overload Eliminator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Personalized PR & Media Intelligence: Group similar stories, eliminate duplicate coverage, and extract high-signal briefings with verified source links.</div>', unsafe_allow_html=True)

# Sidebar: Controls & Settings
with st.sidebar:
    st.header("⚙️ Engine Settings")
    api_key_input = st.text_input("Gemini API Key (Optional)", type="password", value=GEMINI_API_KEY, help="Leave blank to use the high-precision Local NLP Engine")
    model_choice = st.selectbox("Model", [DEFAULT_MODEL, "gemini-3.5-flash-lite"])
    threshold_slider = st.slider("Clustering Similarity Threshold", min_value=0.04, max_value=0.20, value=0.08, step=0.01, help="Lower values group broader industry topics")

    st.markdown("---")
    st.header("📂 Data Ingestion Mode")
    mode = st.radio("Select Ingestion Mode", ["Curated PR Presets", "Paste Article URLs", "Live RSS / Search", "Raw Text Dump"])

# Ingestion Handling
articles = []
default_keywords = []

if mode == "Curated PR Presets":
    preset_choice = st.selectbox(
        "Choose Curated Industry Wave",
        list(PRESET_DATASETS.keys()),
        format_func=lambda k: f"{PRESET_DATASETS[k]['title']} ({len(PRESET_DATASETS[k]['articles'])} articles)"
    )
    dataset = PRESET_DATASETS[preset_choice]
    st.info(f"**Scenario:** {dataset['description']}")
    articles = dataset["articles"]
    default_keywords = dataset.get("default_keywords", [])

elif mode == "Paste Article URLs":
    urls_text = st.text_area("Paste Article URLs (one per line):", height=130, placeholder="https://techcrunch.com/...\nhttps://reuters.com/...")
    if st.button("Fetch & Ingest URLs", type="primary"):
        with st.spinner("Scraping and parsing articles..."):
            urls = [u.strip() for u in urls_text.split("\n") if u.strip()]
            articles = fetch_articles_from_urls(urls)
            st.session_state["custom_articles"] = articles
    articles = st.session_state.get("custom_articles", [])

elif mode == "Live RSS / Search":
    query = st.text_input("Enter Topic or RSS URL", value="OpenAI PR", placeholder="e.g. 'Apple Antitrust' or 'https://techcrunch.com/feed/'")
    if st.button("Fetch Live Feed", type="primary"):
        with st.spinner("Querying feed..."):
            articles = fetch_articles_from_rss(query, limit=15)
            st.session_state["rss_articles"] = articles
    articles = st.session_state.get("rss_articles", [])

elif mode == "Raw Text Dump":
    raw_text = st.text_area("Paste Newsletter or Press Release dump:", height=150, placeholder="Paste articles separated by '---'...")
    if st.button("Parse Text", type="primary"):
        articles = parse_raw_text_articles(raw_text)
        st.session_state["raw_articles"] = articles
    articles = st.session_state.get("raw_articles", [])

if not articles:
    st.warning("Please select a preset or ingest articles to generate the briefing.")
    st.stop()

# Keyword Filtering
st.markdown("### 🔍 Step 2: Topic & Keyword Filter")
all_kw = default_keywords
if not all_kw:
    all_kw = list(set(w.lower() for a in articles for w in a.get("title", "").split() if len(w) > 4))[:8]

selected_keywords = st.multiselect("Filter by keywords (optional - leave empty for all topics):", options=all_kw, default=[])

# Process Button & Pipeline
col_proc, col_stats = st.columns([1, 4])
with col_proc:
    generate_clicked = st.button("⚡ Synthesize Signal", type="primary", use_container_width=True)

# Run clustering
clustering_result = group_articles_into_clusters(
    articles=articles,
    similarity_threshold=threshold_slider,
    duplicate_threshold=0.65,
    keywords=selected_keywords if selected_keywords else None
)
clusters = clustering_result["clusters"]
stats = clustering_result["stats"]

# Display KPI Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-box"><div class="metric-value">{stats["filtered_articles"]}</div><div class="metric-label">Articles Ingested</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-box"><div class="metric-value">{stats["cluster_count"]}</div><div class="metric-label">Core Developments</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-box"><div class="metric-value" style="color:#4ade80;">{stats["noise_reduction_pct"]}%</div><div class="metric-label">Noise Purged ({stats["duplicates_count"]} duplicates)</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-box"><div class="metric-value">{stats["reading_time_saved_min"]}m</div><div class="metric-label">Reading Time Saved</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Generate Briefing
with st.spinner("Synthesizing Executive Briefing..."):
    briefings = generate_full_briefing(
        clusters=clusters,
        api_key=api_key_input,
        model_name=model_choice
    )

# Views
tab_briefing, tab_matrix, tab_raw = st.tabs(["📋 Executive Briefing", "🕸️ Cluster Tree & Deduplication", "📑 Raw Articles"])

with tab_briefing:
    # Export buttons
    c_md, c_html = st.columns(2)
    with c_md:
        md_text = export_to_markdown(briefings, stats)
        st.download_button("📥 Download Markdown Briefing", data=md_text, file_name="Executive_PR_Briefing.md", mime="text/markdown")
    with c_html:
        html_text = export_to_html(briefings, stats)
        st.download_button("🌐 Download HTML Report", data=html_text, file_name="Executive_PR_Briefing.html", mime="text/html")

    st.markdown("### 📢 High-Signal Developments")
    for idx, b in enumerate(briefings, 1):
        signal = b.get("signal_level", "MEDIUM")
        badge_class = "badge-high" if signal == "HIGH" else ("badge-med" if signal == "MEDIUM" else "badge-low")
        
        with st.container(border=True):
            st.markdown(f'<span class="{badge_class}">{signal} SIGNAL</span> &nbsp; **Development #{idx}: {b.get("headline")}**', unsafe_allow_html=True)
            st.caption(f"**Materiality:** {b.get('signal_rationale')}")
            
            st.info(f"**Executive TL;DR:** {b.get('executive_summary')}")
            
            c_facts, c_why = st.columns(2)
            with c_facts:
                st.markdown("**What Happened (Verified Timeline):**")
                for fact in b.get("what_happened", []):
                    st.markdown(f"- {fact}")
            with c_why:
                st.markdown("**Why It Matters for PR & Strategy:**")
                st.write(b.get("why_it_matters"))
                
            # Cross-outlet framing
            if b.get("cross_outlet_framing"):
                st.markdown("**Cross-Outlet Framing & Narrative Differences:**")
                for f in b.get("cross_outlet_framing"):
                    st.markdown(f"- **{f.get('source')}**: *\"{f.get('headline')}\"* &mdash; {f.get('framing')}")
                    
            # Quotes
            if b.get("key_quotes"):
                st.markdown("**Key Quotes:**")
                for q in b.get("key_quotes"):
                    st.markdown(f"> *\"{q.get('quote')}\"* &mdash; **{q.get('attribution')}**")

            # Action
            if b.get("recommended_action"):
                st.success(f"🎯 **Recommended Action:** {b.get('recommended_action')}")

            # Sources
            with st.expander(f"Verified Source Links ({len(b.get('sources', []))} outlets)"):
                for s in b.get("sources", []):
                    dup_tag = " *(Syndicated Repost)*" if s.get("is_duplicate") else ""
                    st.markdown(f"- [{s.get('source')}: {s.get('title')}]({s.get('url', '#')}){dup_tag}")

with tab_matrix:
    st.markdown("### 🕸️ Story Clustering & Deduplication Tree")
    for idx, c in enumerate(clusters, 1):
        with st.expander(f"Cluster #{idx}: {c['headline']} ({c['articles_count']} articles)", expanded=True):
            st.markdown(f"**Primary Story Anchor:** [{c['anchor_article'].get('source')}] {c['anchor_article'].get('title')}")
            st.markdown(f"**Keywords:** {', '.join(c.get('top_keywords', []))}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Unique Perspectives ({len(c['unique_angles'])}):**")
                for a in c["unique_angles"]:
                    st.markdown(f"- [{a.get('source')}] {a.get('title')}")
            with c2:
                st.markdown(f"**Redundant Syndications Purged ({len(c['duplicate_coverage'])}):**")
                for d in c["duplicate_coverage"]:
                    st.markdown(f"- ~[{d.get('source')}] {d.get('title')}~ *(Duplicate)*")

with tab_raw:
    st.markdown("### 📑 All Ingested Raw Articles")
    for art in articles:
        with st.expander(f"[{art.get('source')}] {art.get('title')}"):
            st.write(art.get("content"))
            if art.get("url"):
                st.markdown(f"[Original Link]({art.get('url')})")
