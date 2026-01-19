# engagement_plan.py
# AI Powered Engagement Boost Plan

import json
import re
from openai_helper import get_azure_openai_client


# ✅ Simulated traffic data pattern (as required in assignment)
SIMULATED_TRAFFIC_PATTERN = {
    "high_traffic_days": ["Monday", "Wednesday", "Friday"],
    "medium_traffic_days": ["Tuesday", "Thursday"],
    "low_traffic_days": ["Saturday", "Sunday"],
    "peak_time_slots": ["11:00 AM - 02:00 PM", "07:00 PM - 09:00 PM"],
    "note": "Based on simulated analytics: weekdays perform better; weekends lower engagement."
}


def _extract_json(text: str) -> str:
    """Extract JSON safely from model output."""
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    if text.startswith("{") and text.endswith("}"):
        return text

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return text


def generate_engagement_boost_plan(page: dict) -> dict:
    """
    Generates engagement strategy:
    - content topics
    - emotional blog titles
    - posting schedule
    - hooks & CTAs
    """

    client, deployment = get_azure_openai_client()

    page_name = page.get("page_name", "")
    primary_keyword = page.get("primary_keyword", "")
    content = page.get("content", "")

    # Use small snippet only (better prompt)
    content_snippet = content[:1200]

    prompt = f"""
You are a digital marketing + SEO growth strategist for DreamIT (IT consulting services company).

Goal:
Improve customer engagement, increase organic traffic and conversions for DreamIT.

PAGE DETAILS:
- Page Name: {page_name}
- Primary Keyword: {primary_keyword}
- Content Snippet: {content_snippet}

SIMULATED TRAFFIC DATA:
{SIMULATED_TRAFFIC_PATTERN}

TASKS:
1) Suggest 8 content topics users are likely searching for (related to this service/blog).
2) Suggest 10 blog post titles with emotional triggers (fear of missing out, urgency, curiosity, benefits).
3) Recommend a posting schedule for 2 weeks (day + time slot). Use the traffic pattern.
4) Suggest 5 engagement hooks (for intro lines / LinkedIn post opening).
5) Suggest 3 short conversion CTAs.

Return ONLY valid JSON in this exact format:
{{
  "search_topics": [],
  "emotional_blog_titles": [],
  "two_week_posting_schedule": [
    {{
      "day": "",
      "time": "",
      "content_type": "",
      "title_idea": ""
    }}
  ],
  "engagement_hooks": [],
  "conversion_ctas": []
}}
"""

    response = client.chat.completions.create(
        model=deployment,
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You generate actionable engagement and SEO strategies."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = response.choices[0].message.content or ""
    raw_text = _extract_json(raw_text)

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "search_topics": [],
            "emotional_blog_titles": [],
            "two_week_posting_schedule": [],
            "engagement_hooks": [],
            "conversion_ctas": [],
            "error": "Model returned invalid JSON",
            "raw_response": raw_text
        }
