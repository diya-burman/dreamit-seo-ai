# 🚀 AI-Powered SEO Optimization Dashboard (DreamIT)

This project is an **AI-driven SEO optimization system** built as part of the DreamIT Round-2 assignment.  
It analyzes, scores, and improves website/blog content using **AI, NLP, and SEO best practices**, and presents everything in an interactive **Streamlit dashboard**.

---

## 🎯 Objective

To use Artificial Intelligence to:
- Audit DreamIT’s digital content
- Improve SEO visibility and engagement
- Generate AI-optimized content
- Suggest keyword strategies
- Propose engagement-boosting content ideas

---

## 🧠 Key Features

### ✅ SEO Audit
- Keyword density analysis
- Meta tag quality check
- Heading structure validation
- Readability analysis
- Engagement signal detection (CTAs, tone)

### 📊 SEO Performance Score
- SEO score out of 100
- Transparent scoring breakdown
- Weighted metrics (readability, keywords, meta, CTA, etc.)

### 🔍 Keyword Strategy Engine
- Keyword extraction using **KeyBERT**
- Long-tail keyword suggestions
- Simulated trending keywords
- Keyword clustering for services like Power BI & AI Integration

### ✨ AI-Based SEO Optimization (Azure OpenAI)
- AI-optimized page titles
- Meta descriptions
- Intro paragraphs
- Long-tail keywords
- High-converting CTAs

### 🚀 Engagement Boost Plan (AI-Powered)
- Topics users are searching for
- Emotional trigger blog titles
- Engagement hooks
- 2-week posting schedule (simulated)

### 📥 Downloadable Report
- Professional HTML report
- Combines audit, score, keywords, AI output, and engagement plan

---

## 🧱 Tech Stack

- **Python**
- **Streamlit** (Dashboard)
- **Azure OpenAI (GPT via Azure AI Foundry)**
- **Azure Key Vault** (Secure secret management)
- **KeyBERT** (Keyword extraction)
- **TextStat** (Readability analysis)
- **Pandas**

---

## 📁 Project Structure

```text
DREAMIT-SEO-AI/
│
├── app.py                  # Streamlit dashboard (main app)
├── pages_data.py           # Simulated DreamIT web/blog pages
├── seo_audit.py            # SEO audit logic
├── scoring.py              # SEO score calculation
├── keyword_engine.py       # Keyword extraction & clustering
├── ai_optimizer.py         # AI-based SEO optimization
├── engagement_plan.py      # AI engagement boost strategy
├── openai_helper.py        # Azure OpenAI + Key Vault integration
├── report_generator.py     # HTML report generation
├── requirements.txt        # Project dependencies
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
