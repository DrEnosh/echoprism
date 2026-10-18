import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from google import genai
from core.config import DEFAULT_MODEL, GEMINI_API_KEY

def extract_quotes(text: str) -> List[str]:
    """Extracts quoted statements from article text."""
    matches = re.findall(r'["“]([^"”]{20,200})["”]', text)
    return matches[:3]

def score_signal_level(text: str) -> Tuple[str, str]:
    """Heuristic signal scoring based on corporate/regulatory materiality indicators."""
    lower = text.lower()
    high_impact_tokens = [
        "acquisition", "antitrust", "lawsuit", "investigation", "resigns",
        "whistleblower", "outage", "doj", "ftc", "sec", "patent", "billions",
        "class-action", "breach", "zero-click", "sanctions"
    ]
    med_impact_tokens = [
        "benchmark", "pricing", "enterprise", "cloud", "partnership", "revenue",
        "expansion", "curbs", "interconnect", "licensing", "clinical trial"
    ]

    high_matches = [t for t in high_impact_tokens if t in lower]
    med_matches = [t for t in med_impact_tokens if t in lower]

    if len(high_matches) >= 2 or any(k in lower for k in ["class-action", "antitrust", "breach", "whistleblower"]):
        return "HIGH", f"High material risk / market movement detected ({', '.join(high_matches[:3])})"
    elif len(high_matches) >= 1 or len(med_matches) >= 2:
        return "MEDIUM", f"Substantive strategic development ({', '.join((high_matches + med_matches)[:3])})"
    else:
        return "LOW", "Routine promotional announcement or syndicated update"

def summarize_cluster_local(cluster: Dict[str, Any]) -> Dict[str, Any]:
    """
    Robust local heuristic summarizer for zero-config / offline operation.
    Extracts key facts, identifies outlet framing differences, and ranks signal.
    """
    anchor = cluster.get("anchor_article", {})
    all_articles = cluster.get("all_articles", [])
    unique_angles = cluster.get("unique_angles", [])
    duplicates = cluster.get("duplicate_coverage", [])

    title = anchor.get("title", "Development Update")
    content = anchor.get("content", "")

    # Clean sentences
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", content) if len(s.strip()) > 25]

    # Executive Summary: first 2 substantive sentences
    exec_summary = " ".join(sentences[:2]) if len(sentences) >= 2 else content[:200]

    # Key Facts
    what_happened = sentences[1:4] if len(sentences) > 3 else sentences[:2]
    if not what_happened:
        what_happened = [f"{anchor.get('source', 'Primary source')} reported on {title}."]

    # Materiality & Signal
    full_cluster_text = " ".join(a.get("title", "") + " " + a.get("content", "") for a in all_articles)
    signal_level, signal_rationale = score_signal_level(full_cluster_text)

    # Cross-outlet framing analysis
    framing_list = []
    for art in unique_angles[:5]:
        src = art.get("source", "Outlet")
        art_title = art.get("title", "")
        # Heuristic perspective note
        if "wire" in src.lower() or "press" in src.lower() or "status" in src.lower() or "official" in src.lower():
            angle = f"Official Position: Framed as standard rollout / procedural disclosure."
        elif any(w in art_title.lower() for w in ["pricing", "cost", "stock", "shares", "revenue", "wall street", "investor"]):
            angle = f"Financial & Enterprise Impact: Focused on commercial viability, customer budget reaction, and market valuation."
        elif any(w in art_title.lower() for w in ["lawsuit", "sue", "probe", "scrutiny", "skeptical", "whistleblower", "rumors"]):
            angle = f"Critical Scrutiny: Highlighted legal vulnerabilities, governance risks, or methodology concerns."
        else:
            angle = f"General Industry Analysis: Synthesized broader technological implications for the sector."

        framing_list.append({
            "source": src,
            "headline": art_title,
            "framing": angle
        })

    # Pull Quotes
    quotes = []
    for art in all_articles:
        extracted = extract_quotes(art.get("content", ""))
        for q in extracted:
            quotes.append({"quote": q, "attribution": art.get("source", "Source")})
            if len(quotes) >= 3:
                break
        if len(quotes) >= 3:
            break

    # Sources formatted
    source_links = []
    for art in all_articles:
        source_links.append({
            "id": art.get("id"),
            "source": art.get("source", "Media Outlet"),
            "title": art.get("title", ""),
            "url": art.get("url", "#"),
            "date": art.get("date", ""),
            "is_duplicate": art in duplicates
        })

    # Strategic Action
    action = "Monitor ongoing media traction and evaluate if client/competitor response statement is warranted."
    if signal_level == "HIGH":
        action = "High urgency: Prepare defensive Q&A narrative, monitor regulator/court dockets, and align crisis response team."
    elif signal_level == "MEDIUM":
        action = "Moderate urgency: Track key customer reception, benchmark pricing shifts, and brief leadership on industry trajectory."

    return {
        "cluster_id": cluster.get("cluster_id"),
        "headline": title,
        "signal_level": signal_level,
        "signal_rationale": signal_rationale,
        "executive_summary": exec_summary,
        "what_happened": what_happened,
        "why_it_matters": f"Significantly impacts media narrative and strategic positioning. Cross-outlet coverage reveals key fault lines between corporate PR framing and investigative scrutiny.",
        "cross_outlet_framing": framing_list,
        "key_quotes": quotes,
        "recommended_action": action,
        "sources": source_links,
        "stats": {
            "total_articles": len(all_articles),
            "unique_perspectives": len(unique_angles),
            "duplicate_count": len(duplicates)
        }
    }

def summarize_cluster_with_gemini(
    cluster: Dict[str, Any],
    api_key: str,
    model_name: str = DEFAULT_MODEL
) -> Dict[str, Any]:
    """
    Uses Google GenAI SDK (gemini-3.8-flash) with specialized PR intelligence prompt
    to synthesize multi-outlet coverage into an executive briefing.
    """
    try:
        client = genai.Client(api_key=api_key)

        anchor = cluster.get("anchor_article", {})
        all_articles = cluster.get("all_articles", [])
        unique_angles = cluster.get("unique_angles", [])
        duplicates = cluster.get("duplicate_coverage", [])

        # Build clean prompt context with all articles
        articles_context = []
        for idx, art in enumerate(all_articles, 1):
            is_dup = art in duplicates
            articles_context.append(
                f"[Article {idx}] Source: {art.get('source')} | Title: {art.get('title')} | Date: {art.get('date')} | Duplicate/Syndicated: {is_dup}\n"
                f"Content: {art.get('content', '')[:1200]}\n"
            )

        prompt = f"""You are an elite Public Relations & Media Intelligence Strategist.
Analyze the following cluster of {len(all_articles)} media articles covering the SAME core industry development.
Deduplicate the coverage, eliminate PR boilerplate noise, and produce an executive-ready PR briefing.

ARTICLES:
{chr(10).join(articles_context)}

Your response MUST be a valid JSON object matching EXACTLY this JSON structure:
{{
  "headline": "Crisp, factual, high-signal headline describing the core development",
  "signal_level": "HIGH", // Or "MEDIUM" or "LOW"
  "signal_rationale": "Clear 1-sentence justification for why this matters to leadership",
  "executive_summary": "Concise 2-sentence bottom line for busy executives",
  "what_happened": [
    "Factual bullet point 1",
    "Factual bullet point 2",
    "Factual bullet point 3"
  ],
  "why_it_matters": "2-3 sentences explaining PR, reputational, regulatory, or business ramifications",
  "cross_outlet_framing": [
    {{
      "source": "Outlet name",
      "headline": "Article title",
      "framing": "How this specific outlet framed the story (e.g. corporate cheerleading, critical investigation, enterprise cost concern, market reaction)"
    }}
  ],
  "key_quotes": [
    {{
      "quote": "Exact quoted sentence from spokesperson or key stakeholder",
      "attribution": "Name, title or organization"
    }}
  ],
  "recommended_action": "Actionable recommendation for communications, PR, or executive leadership"
}}

Strict rules:
1. Return ONLY the JSON object. Do not wrap in backticks or markdown if possible.
2. Focus strictly on Signal over Noise.
3. Call out contrasting angles between official PR statements vs investigative/tech press.
"""

        # Call Gemini 3.8 Flash
        interaction = client.interactions.create(
            model=model_name,
            input=prompt
        )

        response_text = interaction.output_text or ""
        response_text = response_text.strip()

        # Clean potential markdown fences
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        parsed = json.loads(response_text)

        # Assemble full result
        source_links = []
        for art in all_articles:
            source_links.append({
                "id": art.get("id"),
                "source": art.get("source", "Media Outlet"),
                "title": art.get("title", ""),
                "url": art.get("url", "#"),
                "date": art.get("date", ""),
                "is_duplicate": art in duplicates
            })

        return {
            "cluster_id": cluster.get("cluster_id"),
            "headline": parsed.get("headline", anchor.get("title", "")),
            "signal_level": parsed.get("signal_level", "MEDIUM").upper(),
            "signal_rationale": parsed.get("signal_rationale", "Key industry development"),
            "executive_summary": parsed.get("executive_summary", ""),
            "what_happened": parsed.get("what_happened", []),
            "why_it_matters": parsed.get("why_it_matters", ""),
            "cross_outlet_framing": parsed.get("cross_outlet_framing", []),
            "key_quotes": parsed.get("key_quotes", []),
            "recommended_action": parsed.get("recommended_action", ""),
            "sources": source_links,
            "stats": {
                "total_articles": len(all_articles),
                "unique_perspectives": len(unique_angles),
                "duplicate_count": len(duplicates)
            }
        }

    except Exception as e:
        print(f"Gemini API summarization failed or fell back: {e}. Using local summarizer.")
        return summarize_cluster_local(cluster)

def generate_full_briefing(
    clusters: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    model_name: str = DEFAULT_MODEL
) -> List[Dict[str, Any]]:
    """
    Generates briefings for all clusters. If API key is available, leverages Gemini 3.8 Flash;
    otherwise seamlessly uses the local NLP engine.
    """
    effective_key = (api_key or "").strip() or (GEMINI_API_KEY or "").strip()
    briefings = []

    for cluster in clusters:
        if effective_key:
            brief = summarize_cluster_with_gemini(cluster, api_key=effective_key, model_name=model_name)
        else:
            brief = summarize_cluster_local(cluster)
        briefings.append(brief)

    # Sort briefings by Signal Priority (HIGH first, then MEDIUM, then LOW)
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    briefings.sort(key=lambda b: priority_order.get(b.get("signal_level", "LOW"), 3))

    return briefings
