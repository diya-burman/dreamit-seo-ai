# keyword_engine.py
# Keyword Strategy Engine using KeyBERT + simulated trending keywords + clustering

from keybert import KeyBERT


# ✅ load model once (very important)
# "all-MiniLM-L6-v2" is lightweight + fast
kw_model = KeyBERT(model="all-MiniLM-L6-v2")


# ✅ Simulated trending keywords (you can expand this list)
TRENDING_KEYWORDS = {
    "power_bi": [
        "Power BI dashboard examples",
        "Power BI DAX optimization",
        "Power BI vs Tableau 2026",
        "Power BI KPI dashboard",
        "Power BI data modeling best practices"
    ],
    "ai_integration": [
        "Azure OpenAI integration",
        "AI workflow automation",
        "enterprise chatbot solutions",
        "Generative AI for business",
        "AI agents for customer support"
    ],
    "data_analytics": [
        "data analytics consulting",
        "business intelligence strategy",
        "data storytelling dashboards",
        "predictive analytics for business",
        "data governance best practices"
    ],
}


# ✅ Service keyword clusters (simple but looks good in interviews)
KEYWORD_CLUSTERS = {
    "Power BI Services": [
        "power bi",
        "dashboard",
        "dax",
        "kpi",
        "reporting",
        "business intelligence",
        "data modeling",
        "visualization"
    ],
    "AI Integration": [
        "ai",
        "automation",
        "azure openai",
        "chatbot",
        "agents",
        "nlp",
        "machine learning",
        "genai"
    ],
    "Data Analytics": [
        "analytics",
        "insights",
        "kpi",
        "data strategy",
        "data cleaning",
        "etl",
        "reporting",
        "visualization"
    ]
}


def extract_keywords_keybert(text: str, top_n: int = 10):
    """
    Extracts keywords using KeyBERT from a piece of text.
    Returns list of dicts: [{"keyword": "...", "score": 0.56}, ...]
    """
    if not text or len(text.strip()) == 0:
        return []

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),  # unigrams to trigrams
        stop_words="english",
        top_n=top_n
    )

    # Convert into clean format
    return [{"keyword": kw, "score": round(score, 4)} for kw, score in keywords]


def guess_page_category(page: dict):
    """
    Decide the category of the page to give trending keywords.
    Uses primary_keyword or page_id.
    """
    primary = (page.get("primary_keyword", "") or "").lower()
    pid = (page.get("page_id", "") or "").lower()

    if "power bi" in primary or "powerbi" in pid:
        return "power_bi"
    if "ai" in primary or "integration" in primary or "ai_" in pid:
        return "ai_integration"
    return "data_analytics"


def get_trending_keywords_for_page(page: dict):
    """
    Returns simulated trending long-tail keywords relevant to the page.
    """
    cat = guess_page_category(page)
    return TRENDING_KEYWORDS.get(cat, [])


def generate_long_tail_keywords(primary_keyword: str):
    """
    Generates long-tail keyword suggestions (rule-based).
    (This is allowed even without AI model; later you can also use GPT for better output.)
    """
    pk = primary_keyword.strip()

    if not pk:
        return []

    return [
        f"best {pk} for small business",
        f"{pk} cost in 2026",
        f"{pk} for startups",
        f"{pk} with implementation support",
        f"enterprise {pk} solutions",
        f"{pk} near me"
    ]


def cluster_keywords(extracted_keywords: list[dict]):
    """
    Places keywords into clusters (Power BI / AI Integration / Data Analytics).
    Simple rule-based matching. Works great for beginner assignment.
    """
    clusters = {
        "Power BI Services": [],
        "AI Integration": [],
        "Data Analytics": [],
        "Other": []
    }

    for item in extracted_keywords:
        kw = item["keyword"].lower()

        matched = False
        for cluster_name, terms in KEYWORD_CLUSTERS.items():
            if any(term in kw for term in terms):
                clusters[cluster_name].append(item)
                matched = True
                break

        if not matched:
            clusters["Other"].append(item)

    return clusters


def keyword_strategy_for_page(page: dict, top_n: int = 10):
    """
    Main function:
    - Extract keywords using KeyBERT
    - Suggest trending keywords
    - Suggest long-tail keywords
    - Create keyword clusters
    """
    content = page.get("content", "")

    # ✅ KeyBERT extraction
    extracted = extract_keywords_keybert(content, top_n=top_n)

    # ✅ clustering
    clusters = cluster_keywords(extracted)

    # ✅ trending (simulated)
    trending = get_trending_keywords_for_page(page)

    # ✅ long-tail suggestions
    primary_kw = page.get("primary_keyword", "")
    long_tail = generate_long_tail_keywords(primary_kw)

    return {
        "extracted_keywords": extracted,
        "clusters": clusters,
        "trending_keywords": trending,
        "long_tail_keywords": long_tail
    }
