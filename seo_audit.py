import re
import textstat

# CTA phrases (you can add more)
CTA_PHRASES = [
    "contact us",
    "book a demo",
    "book demo",
    "get started",
    "talk to an expert",
    "schedule a call",
    "request a demo",
    "free consultation",
    "download",
    "reach out"
]


def clean_text(text: str) -> str:
    """Lowercase + remove extra spaces."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def word_count(text: str) -> int:
    words = re.findall(r"\b\w+\b", text.lower())
    return len(words)


def keyword_density(content: str, keywords: list[str]) -> dict:
    """
    Returns density % for each keyword in the content.
    """
    content_clean = clean_text(content)
    total_words = word_count(content_clean)

    densities = {}
    for kw in keywords:
        kw_clean = clean_text(kw)
        # count occurrences of the exact keyword phrase
        count = len(re.findall(rf"\b{re.escape(kw_clean)}\b", content_clean))
        density = (count / total_words * 100) if total_words > 0 else 0
        densities[kw] = {
            "count": count,
            "density_percent": round(density, 2)
        }

    return {
        "total_words": total_words,
        "keyword_density": densities
    }


def meta_quality(title: str, meta_description: str) -> dict:
    """
    Simple scoring for SEO meta tags.
    """
    title_len = len(title.strip())
    meta_len = len(meta_description.strip())

    # Ideal SEO ranges
    title_ok = 50 <= title_len <= 65
    meta_ok = 120 <= meta_len <= 160

    return {
        "title_length": title_len,
        "meta_description_length": meta_len,
        "title_good": title_ok,
        "meta_good": meta_ok
    }


def headings_audit(headings: dict) -> dict:
    """
    Checks heading counts.
    headings dict example:
        {"h1": "...", "h2": [...], "h3": [...]}
    """
    h1 = headings.get("h1", "")
    h2 = headings.get("h2", [])
    h3 = headings.get("h3", [])

    h1_present = True if isinstance(h1, str) and len(h1.strip()) > 0 else False
    h2_count = len(h2) if isinstance(h2, list) else 0
    h3_count = len(h3) if isinstance(h3, list) else 0

    return {
        "h1_present": h1_present,
        "h2_count": h2_count,
        "h3_count": h3_count
    }


def readability_audit(content: str) -> dict:
    """
    Uses textstat for readability scoring.
    """
    # Some useful metrics
    flesch = textstat.flesch_reading_ease(content)
    grade_level = textstat.flesch_kincaid_grade(content)

    # Good readability rules (simple)
    # Higher flesch is easier
    # Grade level <= 9 is good for general audience
    return {
        "flesch_reading_ease": round(flesch, 2),
        "flesch_kincaid_grade": round(grade_level, 2),
        "easy_to_read": flesch >= 60 and grade_level <= 9
    }


def engagement_audit(content: str, cta: str = "") -> dict:
    """
    Engagement indicators: CTA presence, conversational tone hints etc.
    """
    content_clean = clean_text(content)
    cta_clean = clean_text(cta)

    # Check CTA phrases inside content + provided CTA field
    found_phrases = []
    for phrase in CTA_PHRASES:
        if phrase in content_clean or phrase in cta_clean:
            found_phrases.append(phrase)

    cta_present = len(found_phrases) > 0

    # Simple tone check: looking for "you/your" (conversational)
    conversational_score = 0
    for w in ["you", "your", "we", "us"]:
        conversational_score += len(re.findall(rf"\b{w}\b", content_clean))

    return {
        "cta_present": cta_present,
        "cta_phrases_found": found_phrases,
        "conversational_score": conversational_score
    }


def audit_page(page: dict) -> dict:
    """
    Full audit for a given page dict from pages_data.py
    """
    content = page.get("content", "")
    title = page.get("title", "")
    meta = page.get("meta_description", "")
    headings = page.get("headings", {})
    keywords = page.get("target_keywords", [])
    cta = page.get("cta", "")

    audit = {}

    audit["keyword_density"] = keyword_density(content, keywords)
    audit["meta_quality"] = meta_quality(title, meta)
    audit["headings_audit"] = headings_audit(headings)
    audit["readability"] = readability_audit(content)
    audit["engagement"] = engagement_audit(content, cta)

    return audit
