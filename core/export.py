from typing import List, Dict, Any
from datetime import datetime

def export_to_markdown(briefings: List[Dict[str, Any]], stats: Dict[str, Any], title: str = "Executive PR & Media Briefing") -> str:
    """Formats the synthesized briefing into clean, professional Markdown."""
    now_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    md = []
    md.append(f"# 📢 {title}")
    md.append(f"**Generated:** {now_str} | **Intelligence Engine:** EchoPrism Information Overload Eliminator\n")
    
    # Noise Reduction Metrics Banner
    md.append("## ⚡ Executive Signal Overview")
    md.append(f"- **Articles Analyzed:** {stats.get('filtered_articles', len(briefings))} articles ingested")
    md.append(f"- **Core Developments Identified:** {stats.get('cluster_count', len(briefings))} actionable stories")
    md.append(f"- **Redundant / Syndicated Coverage Eliminated:** {stats.get('duplicates_count', 0)} duplicates")
    md.append(f"- **Signal Efficiency Gain:** **{stats.get('noise_reduction_pct', 0)}% noise eliminated**")
    md.append(f"- **Executive Reading Time Saved:** ~{stats.get('reading_time_saved_min', 0)} minutes\n")
    md.append("---\n")

    # Briefings
    for idx, b in enumerate(briefings, 1):
        signal = b.get("signal_level", "MEDIUM")
        badge = "🔴 HIGH SIGNAL / MATERIAL IMPACT" if signal == "HIGH" else ("🟡 MEDIUM SIGNAL / STRATEGIC" if signal == "MEDIUM" else "🟢 LOW SIGNAL / ROUTINE")
        
        md.append(f"### {idx}. {b.get('headline', 'Industry Development')}")
        md.append(f"**Materiality Rating:** `{badge}` — *{b.get('signal_rationale', '')}*\n")
        
        md.append(f"**Executive Takeaway:**\n> {b.get('executive_summary', '')}\n")
        
        md.append("**What Happened (Verified Timeline):**")
        for fact in b.get("what_happened", []):
            md.append(f"- {fact}")
        md.append("")
        
        md.append(f"**Why It Matters for PR & Corporate Strategy:**\n{b.get('why_it_matters', '')}\n")
        
        # Cross Outlet Framing
        framing = b.get("cross_outlet_framing", [])
        if framing:
            md.append("**Cross-Outlet Framing & Narrative Divergence:**")
            for f in framing:
                md.append(f"- **{f.get('source', 'Outlet')}:** *\"{f.get('headline', '')}\"* — {f.get('framing', '')}")
            md.append("")
            
        # Key Quotes
        quotes = b.get("key_quotes", [])
        if quotes:
            md.append("**Key Stakeholder Quotes:**")
            for q in quotes:
                md.append(f"- *\"{q.get('quote', '')}\"* — **{q.get('attribution', 'Spokesperson')}**")
            md.append("")
            
        # Recommended Action
        if b.get("recommended_action"):
            md.append(f"**Recommended PR / Comms Action:**\n🎯 `{b.get('recommended_action')}`\n")
            
        # Verified Sources
        sources = b.get("sources", [])
        if sources:
            md.append("**Verified Source Links:**")
            for s in sources:
                dup_tag = " *(Syndicated / Duplicate)*" if s.get("is_duplicate") else ""
                url = s.get("url") or "#"
                md.append(f"- [{s.get('source', 'Source')}: {s.get('title', '')}]({url}){dup_tag}")
            md.append("")
            
        md.append("---\n")
        
    md.append("*Confidential Briefing generated via EchoPrism Information Overload Eliminator.*")
    return "\n".join(md)

def export_to_html(briefings: List[Dict[str, Any]], stats: Dict[str, Any], title: str = "Executive PR & Media Briefing") -> str:
    """Generates a standalone, beautifully styled HTML briefing document."""
    now_str = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    
    cards_html = []
    for idx, b in enumerate(briefings, 1):
        signal = b.get("signal_level", "MEDIUM")
        badge_class = "badge-high" if signal == "HIGH" else ("badge-med" if signal == "MEDIUM" else "badge-low")
        
        framing_items = "".join(
            f"<li><strong>{f.get('source')}:</strong> <em>\"{f.get('headline')}\"</em> &mdash; {f.get('framing')}</li>"
            for f in b.get("cross_outlet_framing", [])
        )
        
        facts_items = "".join(f"<li>{fact}</li>" for fact in b.get("what_happened", []))
        
        quotes_items = "".join(
            f"<blockquote>\"{q.get('quote')}\" &mdash; <strong>{q.get('attribution')}</strong></blockquote>"
            for q in b.get("key_quotes", [])
        )
        
        sources_items = "".join(
            f"<li><a href='{s.get('url', '#')}' target='_blank'>{s.get('source')}: {s.get('title')}</a> "
            f"{'<span class=\"pill-dup\">Syndicated Repost</span>' if s.get('is_duplicate') else ''}</li>"
            for s in b.get("sources", [])
        )
        
        card = f"""
        <div class="brief-card">
            <div class="card-header">
                <span class="badge {badge_class}">{signal} SIGNAL</span>
                <span class="card-num">#{idx}</span>
            </div>
            <h2>{b.get('headline')}</h2>
            <p class="rationale"><strong>Materiality:</strong> {b.get('signal_rationale')}</p>
            
            <div class="summary-box">
                <strong>Executive Takeaway:</strong> {b.get('executive_summary')}
            </div>
            
            <div class="section">
                <h3>What Happened</h3>
                <ul>{facts_items}</ul>
            </div>
            
            <div class="section">
                <h3>Why It Matters (PR & Strategic Angle)</h3>
                <p>{b.get('why_it_matters')}</p>
            </div>
            
            {f'<div class="section"><h3>Cross-Outlet Framing Analysis</h3><ul>{framing_items}</ul></div>' if framing_items else ''}
            {f'<div class="section"><h3>Key Quotes</h3>{quotes_items}</div>' if quotes_items else ''}
            
            <div class="action-box">
                <strong>🎯 Recommended Action:</strong> {b.get('recommended_action')}
            </div>
            
            <div class="section sources-section">
                <h4>Verified Source Links ({len(b.get('sources', []))})</h4>
                <ul>{sources_items}</ul>
            </div>
        </div>
        """
        cards_html.append(card)
        
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 32px 16px; line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .header {{ background: #0f172a; color: white; padding: 32px; border-radius: 12px; margin-bottom: 24px; }}
        .header h1 {{ margin: 0 0 8px 0; font-size: 28px; }}
        .header p {{ margin: 0; color: #94a3b8; font-size: 14px; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .metric-card {{ background: white; padding: 18px; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center; }}
        .metric-val {{ font-size: 24px; font-weight: 800; color: #0284c7; margin-bottom: 4px; }}
        .metric-lbl {{ font-size: 12px; font-weight: 600; text-transform: uppercase; color: #64748b; }}
        .brief-card {{ background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 28px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .badge {{ font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 999px; letter-spacing: 0.5px; }}
        .badge-high {{ background: #fee2e2; color: #991b1b; }}
        .badge-med {{ background: #fef3c7; color: #92400e; }}
        .badge-low {{ background: #ecfdf5; color: #065f46; }}
        .card-num {{ color: #94a3b8; font-weight: 700; font-size: 14px; }}
        h2 {{ margin: 0 0 8px 0; font-size: 20px; color: #0f172a; }}
        .rationale {{ color: #64748b; font-size: 13px; margin-bottom: 16px; }}
        .summary-box {{ background: #f0f9ff; border-left: 4px solid #0284c7; padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 20px; font-size: 15px; color: #0369a1; }}
        .action-box {{ background: #fefce8; border: 1px solid #fef08a; padding: 12px 16px; border-radius: 8px; margin: 20px 0; color: #854d0e; font-size: 14px; }}
        .section {{ margin-bottom: 18px; }}
        .section h3 {{ font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; margin: 0 0 8px 0; }}
        .section h4 {{ font-size: 13px; color: #64748b; margin: 0 0 6px 0; }}
        ul {{ margin: 0; padding-left: 20px; }}
        li {{ margin-bottom: 6px; }}
        blockquote {{ margin: 8px 0; padding-left: 14px; border-left: 3px solid #cbd5e1; font-style: italic; color: #475569; }}
        a {{ color: #0284c7; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .pill-dup {{ font-size: 10px; background: #f1f5f9; color: #64748b; padding: 2px 6px; border-radius: 4px; margin-left: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📢 {title}</h1>
            <p>Generated: {now_str} &bull; Powered by EchoPrism AI for PR</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-val">{stats.get('filtered_articles', len(briefings))}</div>
                <div class="metric-lbl">Articles Ingested</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{stats.get('cluster_count', len(briefings))}</div>
                <div class="metric-lbl">Core Developments</div>
            </div>
            <div class="metric-card">
                <div class="metric-val" style="color: #16a34a;">{stats.get('noise_reduction_pct', 0)}%</div>
                <div class="metric-lbl">Noise Eliminated</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{stats.get('reading_time_saved_min', 0)}m</div>
                <div class="metric-lbl">Reading Time Saved</div>
            </div>
        </div>
        
        {"".join(cards_html)}
    </div>
</body>
</html>
"""
    return html
