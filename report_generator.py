# report_generator.py

from datetime import datetime


def generate_html_report(final_report: dict) -> str:
    page = final_report.get("page", {})
    seo_score = final_report.get("seo_score", {})
    audit = final_report.get("seo_audit", {})
    kw = final_report.get("keyword_strategy", {})
    ai = final_report.get("ai_optimization", {})
    engage = final_report.get("engagement_plan", {})

    now = datetime.now().strftime("%d %b %Y, %I:%M %p")

    total_score = seo_score.get("total_score", 0)
    breakdown = seo_score.get("breakdown", {})

    extracted_keywords = kw.get("extracted_keywords", [])
    trending_keywords = kw.get("trending_keywords", [])
    long_tail_keywords = kw.get("long_tail_keywords", [])
    clusters = kw.get("clusters", {})

    # SEO breakdown rows
    breakdown_rows = ""
    for k, v in breakdown.items():
        breakdown_rows += f"""
        <tr>
          <td>{k}</td>
          <td><b>{v.get('score', 0)}</b> / {v.get('out_of', 0)}</td>
          <td>{v.get('reason', '')}</td>
        </tr>
        """

    # extracted keywords rows
    kw_rows = ""
    for item in extracted_keywords:
        kw_rows += f"<tr><td>{item.get('keyword')}</td><td>{item.get('score')}</td></tr>"

    # clusters
    cluster_html = ""
    for cname, items in clusters.items():
        kws = ", ".join([x.get("keyword", "") for x in items]) if items else "—"
        cluster_html += f"<li><b>{cname}</b>: {kws}</li>"

    # posting schedule
    schedule_rows = ""
    for s in engage.get("two_week_posting_schedule", []):
        schedule_rows += f"""
        <tr>
          <td>{s.get("day","")}</td>
          <td>{s.get("time","")}</td>
          <td>{s.get("content_type","")}</td>
          <td>{s.get("title_idea","")}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>DreamIT SEO Optimization Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 30px;
      color: #222;
    }}
    .header {{
      display:flex;
      justify-content:space-between;
      align-items:center;
      border-bottom: 2px solid #eee;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }}
    .badge {{
      display:inline-block;
      padding: 6px 12px;
      border-radius: 999px;
      background:#f4f4f4;
      font-size: 12px;
    }}
    h2 {{
      margin-top: 28px;
      border-left: 4px solid #333;
      padding-left: 10px;
    }}
    .score {{
      font-size: 28px;
      font-weight: 800;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin-top: 10px;
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 10px;
      font-size: 14px;
    }}
    th {{
      background: #fafafa;
      text-align: left;
    }}
    .box {{
      background:#fafafa;
      border: 1px solid #eee;
      padding: 12px;
      border-radius: 10px;
      margin-top: 8px;
    }}
    .grid {{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }}
    ul {{ margin-top: 8px; }}
    .small {{ color:#666; font-size: 13px; }}
  </style>
</head>

<body>

  <div class="header">
    <div>
      <h1>DreamIT – AI Powered SEO Optimization Report</h1>
      <div class="small">Generated on {now}</div>
    </div>
    <div class="badge">Round 2 Assignment</div>
  </div>

  <div class="box">
    <h3>Page Summary</h3>
    <p><b>Page Name:</b> {page.get("page_name","")}</p>
    <p><b>Type:</b> {page.get("page_type","")}</p>
    <p><b>URL:</b> {page.get("url","")}</p>
    <p><b>Primary Keyword:</b> {page.get("primary_keyword","")}</p>
  </div>

  <h2>1) SEO Score</h2>
  <div class="box">
    <div class="score">{total_score} / 100</div>
    <p class="small">Score based on readability, keyword match, title appeal, meta length, link structure and CTA.</p>
  </div>

  <h3>Score Breakdown</h3>
  <table>
    <tr><th>Metric</th><th>Score</th><th>Reason</th></tr>
    {breakdown_rows}
  </table>

  <h2>2) AI Optimized Content</h2>
  <div class="grid">
    <div class="box">
      <h3>Optimized Title</h3>
      <p>{ai.get("optimized_title","—")}</p>

      <h3>Optimized Meta Description</h3>
      <p>{ai.get("optimized_meta_description","—")}</p>
    </div>

    <div class="box">
      <h3>Optimized Intro</h3>
      <p>{ai.get("optimized_intro","—")}</p>

      <h3>High Converting CTAs</h3>
      <ul>
        {''.join([f"<li>{x}</li>" for x in ai.get("ctas", [])]) or "<li>—</li>"}
      </ul>
    </div>
  </div>

  <h2>3) Keyword Strategy</h2>
  <div class="grid">
    <div class="box">
      <h3>Trending Keywords (Simulated)</h3>
      <ul>
        {''.join([f"<li>{x}</li>" for x in trending_keywords]) or "<li>—</li>"}
      </ul>

      <h3>Long-tail Keywords</h3>
      <ul>
        {''.join([f"<li>{x}</li>" for x in long_tail_keywords]) or "<li>—</li>"}
      </ul>
    </div>

    <div class="box">
      <h3>Keyword Clusters</h3>
      <ul>{cluster_html}</ul>
    </div>
  </div>

  <h3>Extracted Keywords (KeyBERT)</h3>
  <table>
    <tr><th>Keyword</th><th>Score</th></tr>
    {kw_rows or "<tr><td colspan='2'>—</td></tr>"}
  </table>

  <h2>4) Engagement Boost Plan</h2>
  <div class="grid">
    <div class="box">
      <h3>Search Topics</h3>
      <ul>
        {''.join([f"<li>{x}</li>" for x in engage.get("search_topics", [])]) or "<li>—</li>"}
      </ul>

      <h3>Engagement Hooks</h3>
      <ul>
        {''.join([f"<li>{x}</li>" for x in engage.get("engagement_hooks", [])]) or "<li>—</li>"}
      </ul>
    </div>

    <div class="box">
      <h3>Emotional Blog Titles</h3>
      <ul>
        {''.join([f"<li>{x}</li>" for x in engage.get("emotional_blog_titles", [])]) or "<li>—</li>"}
      </ul>
    </div>
  </div>

  <h3>2-Week Posting Schedule</h3>
  <table>
    <tr><th>Day</th><th>Time</th><th>Content Type</th><th>Title Idea</th></tr>
    {schedule_rows or "<tr><td colspan='4'>—</td></tr>"}
  </table>

</body>
</html>
"""
    return html
