import re
from typing import List, Dict, Any, Optional, Tuple, Set
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.config import DEFAULT_SIMILARITY_THRESHOLD, DUPLICATE_THRESHOLD

# Common PR & news filler words
ADDITIONAL_STOPWORDS = {
    "said", "says", "inc", "corp", "company", "today", "yesterday", "announced", 
    "reported", "statement", "according", "also", "new", "released", "stated",
    "year", "years", "month", "time", "would", "could", "first", "market",
    "read", "more", "click", "here", "subscribe", "newsletter", "update", "updates",
    "the", "this", "that", "these", "those", "friday", "thursday", "wednesday", "tuesday", "monday"
}

def extract_core_nouns_and_entities(text: str) -> Set[str]:
    """Extracts distinctive proper nouns, model names, brand terms, and compound entities."""
    # Find alphanumeric words with length >= 3
    words = re.findall(r"\b[A-Za-z0-9][A-Za-z0-9\-_]{2,}\b", text)
    tokens = set()
    for w in words:
        low = w.lower()
        if low not in ADDITIONAL_STOPWORDS and not low.isnumeric():
            tokens.add(low)
    return tokens

def filter_by_keywords(articles: List[Dict[str, Any]], keywords: Optional[List[str]]) -> List[Dict[str, Any]]:
    """Filters articles that contain any of the selected keywords in title or content."""
    if not keywords or len(keywords) == 0:
        return articles

    cleaned_keywords = [k.strip().lower() for k in keywords if k.strip()]
    if not cleaned_keywords:
        return articles

    filtered = []
    for art in articles:
        combined = f"{art.get('title', '')} {art.get('content', '')}".lower()
        if any(re.search(r"\b" + re.escape(kw) + r"\b", combined) for kw in cleaned_keywords):
            filtered.append(art)
    return filtered

def extract_top_terms(texts: List[str], top_n: int = 5) -> List[str]:
    """Extracts top representative TF-IDF terms for a group of texts."""
    if not texts:
        return []
    try:
        vec = TfidfVectorizer(
            stop_words="english",
            max_df=0.95,
            min_df=1,
            ngram_range=(1, 2)
        )
        tfidf = vec.fit_transform(texts)
        scores = np.asarray(tfidf.mean(axis=0)).ravel()
        feature_names = vec.get_feature_names_out()
        top_indices = scores.argsort()[::-1]
        
        selected = []
        for i in top_indices:
            term = feature_names[i]
            if term not in ADDITIONAL_STOPWORDS and len(term) > 3:
                selected.append(term)
                if len(selected) >= top_n:
                    break
        return selected
    except Exception:
        return []

def group_articles_into_clusters(
    articles: List[Dict[str, Any]],
    similarity_threshold: float = 0.08,
    duplicate_threshold: float = 0.65,
    keywords: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Groups articles covering the same development using hybrid TF-IDF + Entity/Keyword overlap,
    detects syndicated / verbatim duplicate coverage, and computes noise elimination metrics.
    """
    # 1. Apply keyword filtering if provided
    active_articles = filter_by_keywords(articles, keywords)
    total_active = len(active_articles)

    if total_active == 0:
        return {
            "clusters": [],
            "stats": {
                "total_articles": len(articles),
                "filtered_articles": 0,
                "cluster_count": 0,
                "duplicates_count": 0,
                "unique_perspectives_count": 0,
                "noise_reduction_pct": 0.0,
                "reading_time_saved_min": 0.0
            }
        }

    if total_active == 1:
        single = active_articles[0]
        return {
            "clusters": [{
                "cluster_id": "cluster-1",
                "headline": single.get("title", "Industry Update"),
                "anchor_article": single,
                "all_articles": [single],
                "unique_angles": [single],
                "duplicate_coverage": [],
                "sources": [single.get("source", "Unknown")],
                "top_keywords": [w for w in single.get("title", "").split() if len(w) > 3][:4],
                "articles_count": 1,
                "duplicates_count": 0
            }],
            "stats": {
                "total_articles": len(articles),
                "filtered_articles": 1,
                "cluster_count": 1,
                "duplicates_count": 0,
                "unique_perspectives_count": 1,
                "noise_reduction_pct": 0.0,
                "reading_time_saved_min": 0.0
            }
        }

    # 2. Extract features
    corpus = [f"{a.get('title', '')}. {a.get('content', '')}" for a in active_articles]
    titles = [a.get("title", "") for a in active_articles]

    vec_body = TfidfVectorizer(stop_words="english", min_df=1, ngram_range=(1, 2), sublinear_tf=True)
    sim_body = cosine_similarity(vec_body.fit_transform(corpus))

    vec_title = TfidfVectorizer(stop_words="english", min_df=1, ngram_range=(1, 2))
    sim_title = cosine_similarity(vec_title.fit_transform(titles))

    entities = [extract_core_nouns_and_entities(f"{a.get('title', '')} {a.get('content', '')}") for a in active_articles]

    # 3. Calculate Hybrid Similarity Matrix
    hybrid_sim = np.zeros((total_active, total_active))
    for i in range(total_active):
        for j in range(i, total_active):
            if i == j:
                hybrid_sim[i][j] = 1.0
                continue
            common = entities[i] & entities[j]
            total_ent = len(entities[i] | entities[j])
            ent_jaccard = (len(common) / total_ent) if total_ent > 0 else 0.0

            # Weight body, title, and entity overlap
            score = 0.45 * sim_body[i][j] + 0.35 * sim_title[i][j] + 0.20 * ent_jaccard
            
            # Boost score if they share distinctive non-generic terms
            distinctive_shared = [w for w in common if len(w) >= 4 and not w.endswith("ing")]
            if len(distinctive_shared) >= 2:
                score += 0.05
            if len(distinctive_shared) >= 4:
                score += 0.08

            hybrid_sim[i][j] = score
            hybrid_sim[j][i] = score

    # 4. Connected Components Clustering
    visited = [False] * total_active
    raw_clusters: List[List[int]] = []

    for i in range(total_active):
        if not visited[i]:
            cluster_indices = []
            queue = [i]
            visited[i] = True

            while queue:
                curr = queue.pop(0)
                cluster_indices.append(curr)
                for j in range(total_active):
                    if not visited[j] and hybrid_sim[curr][j] >= similarity_threshold:
                        visited[j] = True
                        queue.append(j)

            raw_clusters.append(cluster_indices)

    # Sort clusters by size descending (biggest news developments first)
    raw_clusters.sort(key=len, reverse=True)

    # 5. Process each cluster: distinguish Anchor, Unique Angles, and Duplicates
    formatted_clusters = []
    total_duplicates = 0
    total_unique_perspectives = 0

    for idx, indices in enumerate(raw_clusters, start=1):
        cluster_articles = [active_articles[i] for i in indices]

        # Duplicate detection within cluster
        dup_flags = [False] * len(indices)
        for i_sub in range(len(indices)):
            if dup_flags[i_sub]:
                continue
            for j_sub in range(i_sub + 1, len(indices)):
                if not dup_flags[j_sub]:
                    orig_i = indices[i_sub]
                    orig_j = indices[j_sub]
                    body_sim = sim_body[orig_i][orig_j]
                    title_sim = sim_title[orig_i][orig_j]
                    # Flag as duplicate if content is highly identical or title is nearly identical
                    if body_sim >= duplicate_threshold or title_sim >= 0.82:
                        dup_flags[j_sub] = True

        # Assign Anchor (prefer article with longest content or official wire source)
        best_score = -1
        anchor_idx = 0
        for sub_idx, art in enumerate(cluster_articles):
            score = len(art.get("content", ""))
            src = art.get("source", "").lower()
            if any(k in src for k in ["official", "wire", "press", "pr newswire", "business wire", "status"]):
                score += 800  # bonus for primary source
            if score > best_score:
                best_score = score
                anchor_idx = sub_idx

        anchor = cluster_articles[anchor_idx]

        unique_angles = []
        duplicate_coverage = []

        for sub_idx, art in enumerate(cluster_articles):
            if sub_idx == anchor_idx:
                unique_angles.append(art)
            elif dup_flags[sub_idx]:
                duplicate_coverage.append(art)
                total_duplicates += 1
            else:
                unique_angles.append(art)
                total_unique_perspectives += 1

        # Sources list
        sources = list(dict.fromkeys(art.get("source", "Unknown") for art in cluster_articles))

        # Cluster keywords
        cluster_texts = [f"{a.get('title', '')} {a.get('content', '')}" for a in cluster_articles]
        top_kw = extract_top_terms(cluster_texts, top_n=6)

        formatted_clusters.append({
            "cluster_id": f"dev-{idx}",
            "headline": anchor.get("title", f"Development #{idx}"),
            "anchor_article": anchor,
            "all_articles": cluster_articles,
            "unique_angles": unique_angles,
            "duplicate_coverage": duplicate_coverage,
            "sources": sources,
            "top_keywords": top_kw,
            "articles_count": len(cluster_articles),
            "duplicates_count": len(duplicate_coverage)
        })

    # 6. Noise Reduction Metrics
    cluster_count = len(formatted_clusters)
    noise_reduction_pct = 0.0
    if total_active > 1:
        noise_reduction_pct = round(((total_active - cluster_count) / total_active) * 100, 1)

    original_reading_time = total_active * 2.5
    briefing_reading_time = cluster_count * 1.0
    time_saved_min = round(max(0.0, original_reading_time - briefing_reading_time), 1)

    stats = {
        "total_articles": len(articles),
        "filtered_articles": total_active,
        "cluster_count": cluster_count,
        "duplicates_count": total_duplicates,
        "unique_perspectives_count": len(articles) - total_duplicates,
        "noise_reduction_pct": noise_reduction_pct,
        "reading_time_saved_min": time_saved_min
    }

    return {
        "clusters": formatted_clusters,
        "stats": stats
    }
