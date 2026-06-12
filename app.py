import streamlit as st
import requests

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Essay Evaluator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body { font-family: 'Inter', sans-serif; }
.stApp { background: #0f1117; color: #e2e8f0; }

section[data-testid="stSidebar"] {
    background: #131720 !important;
    border-right: 1px solid #2d3748;
}

.hero {
    background: #1e1b4b;
    border: 1px solid #4338ca55;
    border-radius: 16px;
    padding: 2rem 2rem 1.75rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.hero h1 { font-size: 2rem; font-weight: 700; color: #c4b5fd; margin: 0 0 .4rem; }
.hero p  { font-size: 1rem; color: #94a3b8; margin: 0; }

.score-card {
    background: #1e2030;
    border: 1px solid #2d3748;
    border-radius: 14px;
    padding: 1.25rem .75rem;
    text-align: center;
}
.score-ring {
    width: 82px; height: 82px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.75rem; font-weight: 700;
    margin: 0 auto .6rem;
}
.score-label { font-size: .75rem; font-weight: 600; letter-spacing: .05em; color: #94a3b8; text-transform: uppercase; }
.score-title { font-size: .95rem; font-weight: 600; color: #e2e8f0; margin-bottom: .2rem; }

.feedback-card {
    background: #1a1f2e;
    border-left: 4px solid;
    border-radius: 0 10px 10px 0;
    padding: 1.1rem 1.4rem;
    margin-bottom: .75rem;
}
.feedback-card h4 { margin: 0 0 .45rem; font-size: .95rem; font-weight: 600; }
.feedback-card p  { margin: 0; font-size: .9rem; color: #cbd5e1; line-height: 1.65; }

.overall-box {
    background: #0f2318;
    border: 1px solid #16a34a44;
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: .75rem;
}
.overall-box h3 { color: #4ade80; margin-top: 0; margin-bottom: .75rem; }
.overall-box p  { color: #d1fae5; line-height: 1.75; margin: 0; }

.step { display:flex; align-items:center; gap:.55rem; padding:.4rem 0; font-size:.88rem; color:#94a3b8; }
.step.active { color:#a78bfa; font-weight:600; }
.step.done   { color:#4ade80; }
.step-dot { width:9px; height:9px; border-radius:50%; flex-shrink:0; }
.step.pending .step-dot { background:#3f4968; }
.step.active  .step-dot { background:#a78bfa; animation: pulse 1s infinite; }
.step.done    .step-dot { background:#4ade80; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .8rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}
.stButton > button:hover { opacity: .88; }

.crit-block {
    background: #1a1f2e;
    border: 1px solid #2d3748;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: .6rem;
}
.crit-block h5 { margin: 0 0 .3rem; font-size: .9rem; font-weight: 600; }
.crit-block p  { margin: 0; font-size: .82rem; color: #94a3b8; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ── Sample essay ───────────────────────────────────────────────────────────────
SAMPLE_ESSAY = """# Role of AI in the New World

## Introduction

Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century. It is reshaping the way people live, work, communicate, and solve problems. From smartphones and virtual assistants to healthcare systems and autonomous vehicles, AI has become an integral part of modern society.

## AI in Everyday Life

AI has significantly influenced daily life by making technology more intelligent and user-friendly. Digital assistants such as Siri, Alexa, and Google Assistant help users perform tasks through voice commands. Recommendation systems on streaming platforms and e-commerce websites analyze user preferences to suggest relevant content and products.

## Transforming Healthcare

One of the most important contributions of AI is in the healthcare sector. AI systems can analyze vast amounts of medical data, helping doctors diagnose diseases accurately and quickly. Machine learning algorithms assist in detecting conditions such as cancer, diabetes, and heart disease at early stages.

## Impact on Business and Industry

Businesses across various industries are leveraging AI to improve productivity and decision-making. AI-powered analytics help organizations understand customer behavior, forecast market trends, and optimize operations. Automation of repetitive tasks reduces costs and allows employees to focus on more creative and strategic responsibilities.

## Conclusion

Artificial Intelligence is playing a pivotal role in shaping the new world. It is revolutionizing healthcare, education, business, and countless other sectors while improving the quality of life for millions of people. When developed and used responsibly, AI has the potential to create a smarter, more efficient, and more prosperous future for humanity.
"""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.divider()
    st.success("Connected to FastAPI Backend automatically via `.env` credentials.")
    st.divider()
    st.markdown("## 📊 How It Works")
    st.markdown("""
Three evaluation agents run **in parallel** via LangGraph on the backend:

| Agent | Evaluates |
|---|---|
| 🔤 Language | Grammar, vocabulary, fluency |
| 🔍 Analysis | Depth, arguments, evidence |
| 💡 Clarity | Structure, coherence, flow |

A final node aggregates all feedback and computes the **average score**.
""")
    st.divider()
    st.markdown("## 📌 Tips")
    st.markdown("""
- Essays of **300–1500 words** work best
- Be specific and structured for higher scores
- Each dimension scored **/10**
""")

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>📝 Parallel Essay Evaluator</h1>
  <p>AI-powered multi-dimensional essay analysis · LangGraph parallel workflow</p>
</div>
""", unsafe_allow_html=True)

# ── Layout ─────────────────────────────────────────────────────────────────────
col_essay, col_criteria = st.columns([3, 1], gap="large")

with col_essay:
    st.markdown("#### ✍️ Your Essay")
    essay_text = st.text_area(
        label="essay_input",
        value=SAMPLE_ESSAY,
        height=370,
        label_visibility="collapsed",
        placeholder="Paste or type your essay here…",
    )
    word_count = len(essay_text.split()) if essay_text.strip() else 0
    st.caption(f"📄 {word_count} words")

with col_criteria:
    st.markdown("#### 🎯 Evaluation Criteria")
    st.markdown("""
<div class="crit-block">
  <h5 style="color:#a78bfa">🔤 Language Quality</h5>
  <p>Grammar, vocabulary, sentence variety, and writing fluency.</p>
</div>
<div class="crit-block">
  <h5 style="color:#60a5fa">🔍 Depth of Analysis</h5>
  <p>Argument strength, evidence use, and critical thinking.</p>
</div>
<div class="crit-block">
  <h5 style="color:#34d399">💡 Clarity of Thought</h5>
  <p>Logical flow, coherence, and overall structure.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")
evaluate_btn = st.button("🚀 Evaluate Essay", use_container_width=True)

# ── UI Helpers ─────────────────────────────────────────────────────────────────
def score_color(score: float):
    s = int(round(score))
    if s >= 8: return "#4ade80", "#052e16"
    if s >= 6: return "#facc15", "#1c1500"
    if s >= 4: return "#fb923c", "#1c0f00"
    return "#f87171", "#1c0404"

def score_ring(score, label, icon):
    fg, bg = score_color(score)
    val = f"{score:.1f}" if isinstance(score, float) else str(score)
    return f"""
<div class="score-card">
  <div class="score-ring" style="background:{bg};border:3px solid {fg};color:{fg}">{val}</div>
  <div class="score-title">{icon} {label}</div>
  <div class="score-label">out of 10</div>
</div>"""

# ── Evaluation run ─────────────────────────────────────────────────────────────
if evaluate_btn:
    if not essay_text.strip():
        st.warning("📄 Please enter an essay to evaluate.")
    elif word_count < 50:
        st.warning("📄 Essay is too short — aim for at least 50 words.")
    else:
        st.divider()
        st.markdown("### ⚡ Running Parallel Evaluation…")

        step_ph = st.empty()
        step_ph.markdown("""
<div class="step active"><div class="step-dot"></div>🔤 Sending to FastAPI Backend...</div>
<div class="step active"><div class="step-dot"></div>🔍 Agents evaluating in parallel...</div>
<div class="step pending"><div class="step-dot"></div>📊 Aggregating results</div>
""", unsafe_allow_html=True)

        try:
            with st.spinner("Processing on the server..."):
                # Call the FastAPI Backend
                response = requests.post("https://agentic-ai-essay-evaluator.onrender.com/evaluate", json={"essay": essay_text})
                
            if response.status_code == 200:
                result = response.json()

                step_ph.markdown("""
<div class="step done"><div class="step-dot"></div>🔤 Language quality ✓</div>
<div class="step done"><div class="step-dot"></div>🔍 Depth of analysis ✓</div>
<div class="step done"><div class="step-dot"></div>💡 Clarity of thought ✓</div>
<div class="step done"><div class="step-dot"></div>📊 Results aggregated ✓</div>
""", unsafe_allow_html=True)

                # Map Backend JSON to UI logic
                scores = result.get("individual_scores", [])
                
                # Handling potential issues if one evaluator failed or timed out
                lang_score = scores[0] if len(scores) > 0 else 0
                anal_score = scores[1] if len(scores) > 1 else 0
                clar_score = scores[2] if len(scores) > 2 else 0
                avg_score  = result.get("avg_score", 0.0)

                st.divider()
                st.markdown("### 🏆 Scores")

                c1, c2, c3, c4 = st.columns(4, gap="medium")
                with c1: st.markdown(score_ring(lang_score, "Language", "🔤"), unsafe_allow_html=True)
                with c2: st.markdown(score_ring(anal_score, "Analysis", "🔍"), unsafe_allow_html=True)
                with c3: st.markdown(score_ring(clar_score, "Clarity",  "💡"), unsafe_allow_html=True)
                with c4: st.markdown(score_ring(avg_score,  "Average",  "⭐"), unsafe_allow_html=True)

                st.markdown("")

                # ── Tabs ──
                st.markdown("### 📋 Detailed Feedback")
                tab1, tab2, tab3 = st.tabs(["🔤 Language", "🔍 Analysis", "💡 Clarity"])

                with tab1:
                    st.markdown(f"""
<div class="feedback-card" style="border-color:#a78bfa">
  <h4 style="color:#a78bfa">Language Quality — {lang_score}/10</h4>
  <p>{result.get('language_feedback', 'No feedback provided.')}</p>
</div>""", unsafe_allow_html=True)

                with tab2:
                    st.markdown(f"""
<div class="feedback-card" style="border-color:#60a5fa">
  <h4 style="color:#60a5fa">Depth of Analysis — {anal_score}/10</h4>
  <p>{result.get('analysis_feedback', 'No feedback provided.')}</p>
</div>""", unsafe_allow_html=True)

                with tab3:
                    st.markdown(f"""
<div class="feedback-card" style="border-color:#34d399">
  <h4 style="color:#34d399">Clarity of Thought — {clar_score}/10</h4>
  <p>{result.get('clarity_feedback', 'No feedback provided.')}</p>
</div>""", unsafe_allow_html=True)

                # ── Overall ──
                st.markdown(f"""
<div class="overall-box">
  <h3>🌟 Overall Summary</h3>
  <p>{result.get('overall_feedback', 'No summary generated.')}</p>
</div>
""", unsafe_allow_html=True)

                # ── Download ──
                st.markdown("")
                report = f"""ESSAY EVALUATION REPORT
=======================
Language Quality  : {lang_score}/10
Depth of Analysis : {anal_score}/10
Clarity of Thought: {clar_score}/10
Average Score     : {avg_score}/10

LANGUAGE FEEDBACK
-----------------
{result.get('language_feedback', '')}

ANALYSIS FEEDBACK
-----------------
{result.get('analysis_feedback', '')}

CLARITY FEEDBACK
----------------
{result.get('clarity_feedback', '')}

OVERALL SUMMARY
---------------
{result.get('overall_feedback', '')}
"""
                st.download_button(
                    "📥 Download Full Report",
                    data=report,
                    file_name="essay_evaluation_report.txt",
                    mime="text/plain",
                )
            else:
                st.error(f"❌ Backend returned an error: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Failed to connect to backend. Make sure FastAPI is running on port 8000.")