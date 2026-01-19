# ai_optimizer.py

import json
import re
from openai_helper import get_azure_openai_client


def _extract_json(text: str) -> str:
    """
    Extract JSON object from a string safely.
    Handles cases where model returns extra text around JSON.
    """
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    # Try direct JSON first
    if text.startswith("{") and text.endswith("}"):
        return text

    # Extract JSON object using regex
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return text  # fallback


def generate_seo_optimization(page: dict) -> dict:
    """
    Uses Azure OpenAI to generate SEO improved versions for:
    - title
    - intro
    - meta description
    - long-tail keywords
    - CTA
    """

    client, deployment = get_azure_openai_client()

    page_name = page.get("page_name", "")
    primary_keyword = page.get("primary_keyword", "")
    content = page.get("content", "")

    prompt = f"""
You are an SEO expert and conversion copywriter for an IT services company called DreamIT.

Page Name: {page_name}
Primary Keyword: {primary_keyword}

Existing Content:
{content}

TASKS:
1) Rewrite a better SEO-friendly Title (max 65 characters).
2) Write a better Meta Description (120-160 characters).
3) Write a strong Intro paragraph (70-90 words).
4) Suggest 8 long-tail keywords relevant to the page.
5) Generate 3 high-converting CTAs (short).

Return ONLY valid JSON (no explanation, no extra text) in this format:
{{
  "optimized_title": "",
  "optimized_meta_description": "",
  "optimized_intro": "",
  "long_tail_keywords": [],
  "ctas": []
}}
"""

    response = client.chat.completions.create(
        model=deployment,
        temperature=0.6,
        messages=[
            {"role": "system", "content": "You are a helpful AI SEO assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = response.choices[0].message.content or ""
    raw_text = _extract_json(raw_text)

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # fallback output so Streamlit doesn't crash
        return {
            "optimized_title": "",
            "optimized_meta_description": "",
            "optimized_intro": "",
            "long_tail_keywords": [],
            "ctas": [],
            "error": "Model did not return valid JSON",
            "raw_response": raw_text
        }
