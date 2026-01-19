# -----------------------------
# UI Helper Functions
# -----------------------------
def show_list(items, icon="•"):
    """Show list like normal readable bullets (not JSON)."""
    if not items:
        st.write("—")
        return
    for x in items:
        st.markdown(f"{icon} {x}")

def show_keyword_chips(items):
    """Show keywords as chip-style tags."""
    if not items:
        st.write("—")
        return
    html = ""
    for x in items:
        html += f"""
        <span style="
            display:inline-block;
            padding:6px 12px;
            margin:4px 6px 4px 0px;
            border-radius:999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            font-size: 13px;
        ">{x}</span>
        """
    st.markdown(html, unsafe_allow_html=True)

def show_kv_cards(data: dict):
    """Display dict as clean key-value rows (instead of JSON)."""
    if not data:
        st.write("—")
        return
    for k, v in data.items():
        st.markdown(f"**{str(k).replace('_',' ').title()}**: {v}")


import streamlit as st
import pandas as pd
import json

from pages_data import dreamit_pages

from seo_audit import audit_page
from scoring import compute_seo_score

from keyword_engine import keyword_strategy_for_page
from ai_optimizer import generate_seo_optimization
from engagement_plan import generate_engagement_boost_plan

from report_generator import generate_html_report


# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="DreamIT AI SEO Optimizer", page_icon="🚀", layout="wide")

st.title("🚀 AI-Powered SEO Optimization Dashboard (DreamIT)")
st.caption("SEO Audit + AI Content Optimization + Keyword Strategy + Engagement Plan")


# -----------------------------
# Helper functions (cache)
# -----------------------------
@st.cache_data(show_spinner=False)
def run_audit(page: dict) -> dict:
    return audit_page(page)


@st.cache_data(show_spinner=False)
def run_score(page: dict, audit: dict) -> dict:
    return compute_seo_score(page, audit)


@st.cache_data(show_spinner=False)
def run_keyword_strategy(page: dict) -> dict:
    return keyword_strategy_for_page(page)


# NOTE: Do not cache AI calls with cache_data permanently unless you want the same results.
# We'll store AI results in session_state instead.
def get_session_key(prefix: str, page_id: str) -> str:
    return f"{prefix}_{page_id}"


# -----------------------------
# Sidebar - Page Selection
# -----------------------------
st.sidebar.header("📌 Select DreamIT Page")

page_names = [p["page_name"] for p in dreamit_pages]
selected_name = st.sidebar.selectbox("Choose Page", page_names)

selected_page = next(p for p in dreamit_pages if p["page_name"] == selected_name)
page_id = selected_page.get("page_id", "unknown")

st.sidebar.write("### Page Info")
st.sidebar.write("**Type:**", selected_page.get("page_type", ""))
st.sidebar.write("**Primary Keyword:**", selected_page.get("primary_keyword", ""))
st.sidebar.write("**URL:**", selected_page.get("url", ""))


# -----------------------------
# Display Original Page Content
# -----------------------------
with st.expander("📄 View Original Page Content", expanded=True):
    st.write("### Title")
    st.write(selected_page.get("title", ""))

    st.write("### Meta Description")
    st.write(selected_page.get("meta_description", ""))

    # st.write("### Headings")

    headings = selected_page.get("headings", {})
    h1 = headings.get("h1", "")
    h2_list = headings.get("h2", [])
    h3_list = headings.get("h3", [])

    # show h1 nicely (no label)
    if h1:
       st.markdown(f"#### {h1}")
    else:
       st.markdown("#### —")

    # combine h2 + h3 and show as bullets (no label)
    sub_headings = []
    if isinstance(h2_list, list):
       sub_headings.extend(h2_list)
    if isinstance(h3_list, list):
       sub_headings.extend(h3_list)

    if sub_headings:
        for sh in sub_headings:
            st.markdown(f"• {sh}")
    else:
        st.write("—")

    st.write("### Content")
    st.write(selected_page.get("content", ""))

    st.write("### CTA")
    st.write(selected_page.get("cta", ""))


# -----------------------------
# Tabs UI
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🧾 SEO Audit",
        "📊 SEO Score",
        "🔍 Keyword Strategy",
        "✨ AI Optimization",
        "🚀 Engagement Boost Plan",
    ]
)


# ============================================================
# TAB 1: SEO Audit
# ============================================================
with tab1:
    st.subheader("🧾 SEO Audit Results")

    audit = run_audit(selected_page)

    meta = audit.get("meta_quality", {})
    readability = audit.get("readability", {})
    engagement = audit.get("engagement", {})
    headings_audit = audit.get("headings_audit", {})

    # -----------------------------
    # KPI Cards (Top Row)
    # -----------------------------
    a, b, c, d = st.columns(4)

    with a:
        st.metric("Title Length", meta.get("title_length", 0))
    with b:
        st.metric("Meta Length", meta.get("meta_description_length", 0))
    with c:
        st.metric("Readability", readability.get("flesch_reading_ease", 0))
    with d:
        st.metric("Grade Level", readability.get("flesch_kincaid_grade", 0))

    col1, col2 = st.columns(2)

    # -----------------------------
    # LEFT COLUMN
    # -----------------------------
    with col1:
        with st.container(border=True):
            st.markdown("### 🏷 Meta Quality")
            st.markdown(f"**Title Good:** {'✅ Yes' if meta.get('title_good') else '❌ No'}")
            st.markdown(f"**Meta Good:** {'✅ Yes' if meta.get('meta_good') else '❌ No'}")
            st.markdown(f"**Title Length:** {meta.get('title_length', 0)}")
            st.markdown(f"**Meta Length:** {meta.get('meta_description_length', 0)}")

        with st.container(border=True):
            st.markdown("### 🧱 Heading Structure")
            st.markdown(f"**H1 Present:** {'✅ Yes' if headings_audit.get('h1_present') else '❌ No'}")
            st.markdown(f"**H2 Count:** {headings_audit.get('h2_count', 0)}")
            st.markdown(f"**H3 Count:** {headings_audit.get('h3_count', 0)}")

    # -----------------------------
    # RIGHT COLUMN
    # -----------------------------
    with col2:
        with st.container(border=True):
            st.markdown("### 📚 Readability")
            st.markdown(f"**Flesch Score:** {readability.get('flesch_reading_ease', 0)}")
            st.markdown(f"**Grade Level:** {readability.get('flesch_kincaid_grade', 0)}")
            st.markdown(f"**Easy to Read:** {'✅ Yes' if readability.get('easy_to_read') else '❌ No'}")

        with st.container(border=True):
            st.markdown("### 🎯 Engagement Signals")
            st.markdown(f"**CTA Present:** {'✅ Yes' if engagement.get('cta_present') else '❌ No'}")

            phrases = engagement.get("cta_phrases_found", [])
            if phrases:
                st.markdown("**CTA phrases found:**")
                for p in phrases:
                    st.markdown(f"✅ {p}")
            else:
                st.markdown("**CTA phrases found:** —")

            st.markdown(f"**Conversational Score:** {engagement.get('conversational_score', 0)}")

    # -----------------------------
    # Keyword Density Table
    # -----------------------------
    st.markdown("### 🔎 Keyword Density")
    kd = audit.get("keyword_density", {})

    st.caption(f"Total Words: {kd.get('total_words', 0)}")

    kd_rows = []
    for kw, info in kd.get("keyword_density", {}).items():
        kd_rows.append({
            "Keyword": kw,
            "Count": info.get("count", 0),
            "Density (%)": info.get("density_percent", 0),
        })

    if kd_rows:
        df_kd = pd.DataFrame(kd_rows)
        st.dataframe(df_kd, use_container_width=True, hide_index=True)
    else:
        st.info("No keyword density data found.")


# ============================================================
# TAB 2: SEO Score
# ============================================================
with tab2:
    st.subheader("📊 SEO Performance Score (Out of 100)")

    audit = run_audit(selected_page)
    score_report = run_score(selected_page, audit)

    total_score = score_report.get("total_score", 0)

    st.metric("SEO Score", f"{total_score} / 100")

    st.progress(total_score / 100)

    st.write("### Score Breakdown")
    breakdown = score_report.get("breakdown", {})

    breakdown_rows = []
    for metric, details in breakdown.items():
        breakdown_rows.append(
            {
                "Metric": metric,
                "Score": details.get("score", 0),
                "Out Of": details.get("out_of", 0),
                "Reason": details.get("reason", ""),
            }
        )

    st.dataframe(pd.DataFrame(breakdown_rows), use_container_width=True)


# ============================================================
# TAB 3: Keyword Strategy
# ============================================================
with tab3:
    st.subheader("🔍 Keyword Strategy Engine (KeyBERT + Trending + Clusters)")
    strategy = run_keyword_strategy(selected_page)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### ✅ Extracted Keywords (KeyBERT)")
            extracted = strategy.get("extracted_keywords", [])
            if extracted:
                st.dataframe(pd.DataFrame(extracted), use_container_width=True, hide_index=True)
            else:
                st.info("No extracted keywords found.")

        with st.container(border=True):
            st.markdown("### 🎯 Long-tail Keywords")
            show_keyword_chips(strategy.get("long_tail_keywords", []))

    with col2:
        with st.container(border=True):
            st.markdown("### 📈 Trending Keywords (Simulated)")
            show_list(strategy.get("trending_keywords", []), icon="🔥")

        with st.container(border=True):
            st.markdown("### 🧩 Keyword Clusters")
            clusters = strategy.get("clusters", {})
            for cluster_name, kws in clusters.items():
                st.markdown(f"**{cluster_name}**")
                if kws:
                    show_keyword_chips([k["keyword"] for k in kws])
                else:
                    st.write("—")


# ============================================================
# TAB 4: AI Optimization
# ============================================================
with tab4:
    st.subheader("✨ AI-Based SEO Optimization (Azure OpenAI)")
    st.caption("Generate SEO-enhanced content: title, meta description, intro, long-tail keywords and CTAs.")

    ai_key = get_session_key("ai_opt", page_id)

    # Generate button
    if st.button("✨ Generate AI SEO Optimization"):
        with st.spinner("Generating optimized content..."):
            st.session_state[ai_key] = generate_seo_optimization(selected_page)
        st.success("AI optimization generated ✅")

    # Display
    if ai_key in st.session_state:
        ai_result = st.session_state[ai_key]

        if "error" in ai_result:
            st.error(ai_result["error"])
            st.write(ai_result.get("raw_response", ""))

        else:
            col1, col2 = st.columns([1.2, 1])

            # LEFT column: Title + Meta + Intro
            with col1:
                with st.container(border=True):
                    st.markdown("### 🏷 Optimized Title")
                    st.markdown(f"**{ai_result.get('optimized_title', '—')}**")

                with st.container(border=True):
                    st.markdown("### 📝 Optimized Meta Description")
                    st.write(ai_result.get("optimized_meta_description", "—"))

                with st.container(border=True):
                    st.markdown("### 📌 Optimized Intro Paragraph")
                    st.write(ai_result.get("optimized_intro", "—"))

            # RIGHT column: Keywords + CTA
            with col2:
                with st.container(border=True):
                    st.markdown("### 🔑 Long-tail Keyword Suggestions")
                    show_keyword_chips(ai_result.get("long_tail_keywords", []))

                with st.container(border=True):
                    st.markdown("### 🎯 High Converting CTAs")
                    ctas = ai_result.get("ctas", [])
                    if ctas:
                        for cta in ctas:
                            st.button(cta)
                    else:
                        st.write("—")

    else:
        st.info("Click **Generate AI SEO Optimization** to see updated content here.")



# ============================================================
# TAB 5: Engagement Boost Plan
# ============================================================
with tab5:
    st.subheader("🚀 AI-Powered Engagement Boost Plan")
    st.caption("AI suggests content ideas, emotional titles and posting schedule to increase engagement.")

    engage_key = get_session_key("eng_plan", page_id)

    if st.button("🔥 Generate Engagement Plan"):
        with st.spinner("Generating engagement plan..."):
            st.session_state[engage_key] = generate_engagement_boost_plan(selected_page)

    if engage_key in st.session_state:
        plan = st.session_state[engage_key]

        if "error" in plan:
            st.error(plan["error"])
            st.write(plan.get("raw_response", ""))
        else:
            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.markdown("### 🔎 Topics users are searching for")
                    show_list(plan.get("search_topics", []), icon="🔍")

                with st.container(border=True):
                    st.markdown("### 🎣 Engagement Hooks")
                    hooks = plan.get("engagement_hooks", [])
                    if hooks:
                        for h in hooks:
                            st.info(h)     # gives card look
                    else:
                        st.write("—")

                with st.container(border=True):
                    st.markdown("### ✅ Conversion CTAs")
                    ctas = plan.get("conversion_ctas", [])
                    if ctas:
                        for cta in ctas:
                            st.button(cta)
                    else:
                        st.write("—")

            with col2:
                with st.container(border=True):
                    st.markdown("### 🧠 Emotional Trigger Blog Titles")
                    titles = plan.get("emotional_blog_titles", [])
                    if titles:
                        for t in titles:
                            st.markdown(f"🧠 **{t}**")
                    else:
                        st.write("—")

            st.markdown("### 📅 2-Week Posting Schedule")
            schedule = plan.get("two_week_posting_schedule", [])
            if schedule:
                df = pd.DataFrame(schedule)
                df = df.rename(columns={
                    "day": "Day",
                    "time": "Time Slot",
                    "content_type": "Content Type",
                    "title_idea": "Title Idea"
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No schedule generated.")


# -----------------------------
# Download Report (Full JSON)
# -----------------------------
st.divider()
st.subheader("📥 Download Full Report")

audit = run_audit(selected_page)
score_report = run_score(selected_page, audit)
keyword_strategy = run_keyword_strategy(selected_page)

ai_result = st.session_state.get(get_session_key("ai_opt", page_id), {})
eng_result = st.session_state.get(get_session_key("eng_plan", page_id), {})

final_report = {
    "page": selected_page,
    "seo_audit": audit,
    "seo_score": score_report,
    "keyword_strategy": keyword_strategy,
    "ai_optimization": ai_result,
    "engagement_plan": eng_result,
}

html_report = generate_html_report(final_report)

st.download_button(
    label="⬇️ Download Report",
    data=html_report,
    file_name=f"dreamit_seo_report_{page_id}.html",
    mime="text/html",
)
