# scoring.py
# SEO Score /100 logic

import re


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def score_readability(readability: dict) -> tuple[int, str]:
    """
    20 marks
    Uses:
    - Flesch reading ease
    - Flesch-Kincaid grade
    """
    flesch = readability.get("flesch_reading_ease", 0)
    grade = readability.get("flesch_kincaid_grade", 999)

    score = 0

    # Flesch: 60+ is good readability
    if flesch >= 60:
        score += 10
    elif flesch >= 45:
        score += 6
    elif flesch >= 30:
        score += 3
    else:
        score += 1

    # Grade level: <= 9 is good
    if grade <= 9:
        score += 10
    elif grade <= 12:
        score += 6
    elif grade <= 16:
        score += 3
    else:
        score += 1

    score = int(clamp(score, 0, 20))

    reason = f"Flesch={flesch}, Grade={grade}"
    return score, reason


def score_keyword_match(keyword_audit: dict, primary_keyword: str) -> tuple[int, str]:
    """
    20 marks
    Use keyword density of target keywords; focus on primary keyword.
    Good density range: 0.5% to 2.5%
    """
    densities = keyword_audit.get("keyword_density", {})
    total_words = keyword_audit.get("total_words", 0)

    # If no content
    if total_words == 0:
        return 0, "No content words found"

    primary_info = densities.get(primary_keyword, {"count": 0, "density_percent": 0})
    density = primary_info.get("density_percent", 0)

    # scoring logic
    # Perfect range: 0.5 - 2.5
    if 0.5 <= density <= 2.5:
        score = 20
        msg = f"Primary keyword density ideal ({density}%)"
    elif 0.2 <= density < 0.5:
        score = 12
        msg = f"Primary keyword density low ({density}%)"
    elif 2.5 < density <= 4.0:
        score = 12
        msg = f"Primary keyword density slightly high ({density}%)"
    elif density == 0:
        score = 0
        msg = "Primary keyword not found in content"
    else:
        score = 6
        msg = f"Primary keyword density not optimal ({density}%)"

    return int(clamp(score, 0, 20)), msg


def score_title_appeal(title: str, primary_keyword: str) -> tuple[int, str]:
    """
    20 marks
    10 marks for length (50-65)
    10 marks if primary keyword appears in title
    """
    title_clean = title.strip()
    length = len(title_clean)

    score = 0
    reasons = []

    # Title length
    if 50 <= length <= 65:
        score += 10
        reasons.append(f"Length good ({length})")
    elif 40 <= length < 50 or 65 < length <= 80:
        score += 6
        reasons.append(f"Length acceptable ({length})")
    else:
        score += 2
        reasons.append(f"Length poor ({length})")

    # Keyword in title
    if primary_keyword.lower() in title_clean.lower():
        score += 10
        reasons.append("Primary keyword present")
    else:
        reasons.append("Primary keyword missing")

    return int(clamp(score, 0, 20)), ", ".join(reasons)


def score_meta_length(meta_quality: dict) -> tuple[int, str]:
    """
    15 marks
    Meta description ideal length 120-160.
    """
    meta_len = meta_quality.get("meta_description_length", 0)

    if 120 <= meta_len <= 160:
        return 15, f"Meta length ideal ({meta_len})"
    elif 100 <= meta_len < 120 or 160 < meta_len <= 180:
        return 10, f"Meta length okay ({meta_len})"
    elif meta_len == 0:
        return 0, "Meta description missing"
    else:
        return 5, f"Meta length poor ({meta_len})"


def score_link_structure(content: str) -> tuple[int, str]:
    """
    15 marks
    Count links. (simulated since content is plain text)
    """
    # link signals: http, https, www, /services, /blog etc.
    links = re.findall(r"(https?://\S+|www\.\S+|/services/\S+|/blog/\S+)", content)

    link_count = len(links)

    if link_count >= 3:
        return 15, f"Good links ({link_count})"
    elif link_count == 2:
        return 10, f"Some links ({link_count})"
    elif link_count == 1:
        return 6, f"Low links ({link_count})"
    else:
        return 3, "No links detected (consider adding internal links)"


def score_cta_presence(engagement: dict) -> tuple[int, str]:
    """
    10 marks
    If CTA present => full marks.
    """
    cta_present = engagement.get("cta_present", False)

    if cta_present:
        return 10, "CTA present"
    return 0, "CTA missing"


def compute_seo_score(page: dict, audit: dict) -> dict:
    """
    Final function:
    Takes page dict and audit dict, returns score breakdown + total score.
    """
    title = page.get("title", "")
    content = page.get("content", "")
    primary_keyword = page.get("primary_keyword", "")

    # sub-scores
    readability_score, readability_reason = score_readability(audit.get("readability", {}))
    keyword_score, keyword_reason = score_keyword_match(
        audit.get("keyword_density", {}),
        primary_keyword
    )
    title_score, title_reason = score_title_appeal(title, primary_keyword)
    meta_score, meta_reason = score_meta_length(audit.get("meta_quality", {}))
    link_score, link_reason = score_link_structure(content)
    cta_score, cta_reason = score_cta_presence(audit.get("engagement", {}))

    total = readability_score + keyword_score + title_score + meta_score + link_score + cta_score

    return {
        "total_score": int(clamp(total, 0, 100)),
        "breakdown": {
            "readability": {"score": readability_score, "out_of": 20, "reason": readability_reason},
            "keyword_match": {"score": keyword_score, "out_of": 20, "reason": keyword_reason},
            "title_appeal": {"score": title_score, "out_of": 20, "reason": title_reason},
            "meta_length": {"score": meta_score, "out_of": 15, "reason": meta_reason},
            "link_structure": {"score": link_score, "out_of": 15, "reason": link_reason},
            "cta_presence": {"score": cta_score, "out_of": 10, "reason": cta_reason},
        }
    }
