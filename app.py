"""
Streamlit Application: AI Resume & Candidate Fit Analyzer
Provides senior-level evaluation comparing candidate resumes against job descriptions.
Displays Strengths, Weaknesses, Areas to Improve, Final Verdict, and Skill Fit.
"""

from __future__ import annotations

import os
import tempfile
from typing import Any

import streamlit as st
from resume_analyzer import analyze_resume


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume & Candidate Fit Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUSTOM CSS / DESIGN SYSTEM
# =========================================================

st.markdown(
    """
<style>
/* Base Theme & Layout */
.stApp {
    background: #090d16;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

/* Header Section */
.hero-container {
    background: linear-gradient(135deg, #111827 0%, #1e1b4b 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 4px 10px;
    border-radius: 9999px;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin: 0 0 0.4rem 0;
    line-height: 1.2;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 1rem;
    margin: 0;
    line-height: 1.5;
}

/* Section Headings */
.section-title {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #94a3b8;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Input Fields */
textarea {
    background: #0f172a !important;
    color: #f1f5f9 !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    font-size: 0.92rem !important;
}

textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
}

[data-testid="stFileUploader"] {
    background: #0f172a;
    border: 1px dashed #334155;
    border-radius: 10px;
    padding: 0.5rem;
}

/* Primary Button */
.stButton > button {
    height: 48px;
    border-radius: 10px;
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
    border: 1px solid #818cf8;
    color: #ffffff;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.35);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%);
    border-color: #a5b4fc;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45);
    transform: translateY(-1px);
}

/* File Info Box */
.file-info-badge {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 0.65rem 0.9rem;
    margin-top: 0.6rem;
    color: #cbd5e1;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Candidate Overview Hero Card */
.candidate-hero-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.25rem;
}

.candidate-name-text {
    font-size: 1.85rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 0.2rem 0 0.4rem 0;
    line-height: 1.2;
}

.candidate-tagline {
    color: #94a3b8;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.exp-badge-met {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.exp-badge-unmet {
    background: rgba(244, 63, 94, 0.12);
    border: 1px solid rgba(244, 63, 94, 0.3);
    color: #fb7185;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

/* Score Card */
.score-hero-box {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.score-hero-number {
    font-size: 3.4rem;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 0.35rem;
}

.score-hero-label {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Analysis Cards */
.analysis-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.card-header-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0.4rem;
}

.card-title-text {
    font-size: 1.08rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0;
}

.card-desc-text {
    color: #64748b;
    font-size: 0.82rem;
    margin-bottom: 1rem;
    line-height: 1.4;
}

/* Card Themes */
.card-strengths {
    border-top: 3px solid #10b981;
}

.card-weaknesses {
    border-top: 3px solid #f43f5e;
}

.card-improvements {
    border-top: 3px solid #06b6d4;
}

.card-verdict {
    border-top: 3px solid #6366f1;
}

/* Bullet Items */
.analysis-item-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 0.75rem;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.5;
}

.bullet-icon-emerald {
    color: #10b981;
    font-size: 0.95rem;
    flex-shrink: 0;
    margin-top: 2px;
}

.bullet-icon-rose {
    color: #f43f5e;
    font-size: 0.95rem;
    flex-shrink: 0;
    margin-top: 2px;
}

.bullet-icon-cyan {
    color: #06b6d4;
    font-size: 0.95rem;
    flex-shrink: 0;
    margin-top: 2px;
}

/* Verdict Box */
.verdict-container {
    background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
    border: 1px solid #1e293b;
    border-left: 4px solid #6366f1;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.25rem;
}

.verdict-badge {
    color: #818cf8;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}

.verdict-content {
    color: #e2e8f0;
    font-size: 0.95rem;
    line-height: 1.65;
}

/* Skills Chips */
.skills-container {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 0.3rem;
}

.chip-match {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: #6ee7b7;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 5px 10px;
    border-radius: 6px;
}

.chip-missing {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: #fcd34d;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 5px 10px;
    border-radius: 6px;
}

.chip-empty {
    color: #64748b;
    font-size: 0.82rem;
    font-style: italic;
}

/* Metric Pill */
.metric-pill {
    background: #1e293b;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    text-align: center;
}

.metric-pill-val {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f8fafc;
}

.metric-pill-lbl {
    font-size: 0.72rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 2px;
}

/* Clean Expander */
[data-testid="stExpander"] {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
}

/* Footer */
.app-footer {
    text-align: center;
    color: #475569;
    font-size: 0.78rem;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1e293b;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================


def extract_field(details: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """
    Robust case-insensitive and snake/camel-case resilient key lookup from details dictionary.
    """
    if not isinstance(details, dict):
        return default

    # 1. Exact match search
    for key in keys:
        if key in details and details[key] is not None:
            return details[key]

    # 2. Case and underscore insensitive search
    normalized_map = {
        str(k).lower().replace(" ", "_").replace("-", ""): v
        for k, v in details.items()
    }
    for key in keys:
        norm_key = str(key).lower().replace(" ", "_").replace("-", "")
        if norm_key in normalized_map and normalized_map[norm_key] is not None:
            return normalized_map[norm_key]

    return default


def normalize_items(value: Any) -> list[str]:
    """
    Converts various LLM outputs (list, string, dict) into a clean list of strings.
    """
    if not value:
        return []

    if isinstance(value, list):
        clean_list: list[str] = []
        for item in value:
            if isinstance(item, str):
                trimmed = item.strip().lstrip("•-*0123456789. ")
                if trimmed:
                    clean_list.append(trimmed)
            elif isinstance(item, dict):
                joined = " — ".join(f"{k}: {v}" for k, v in item.items())
                clean_list.append(joined)
            else:
                clean_list.append(str(item))
        return clean_list

    if isinstance(value, str):
        lines = [
            line.strip().lstrip("•-*0123456789. ")
            for line in value.split("\n")
            if line.strip()
        ]
        return lines

    return [str(value)]


def render_chips(skills: list[str], missing: bool = False) -> str:
    """
    Generates HTML chip badges for matching or missing skills.
    """
    if not skills:
        return '<span class="chip-empty">None identified</span>'

    css_class = "chip-missing" if missing else "chip-match"
    html_items = "".join(
        f'<span class="{css_class}">{skill}</span>' for skill in skills
    )
    return f'<div class="skills-container">{html_items}</div>'


def get_score_color(score: float) -> str:
    """
    Returns appropriate color hex according to match score.
    """
    if score >= 75:
        return "#10b981"  # Emerald
    if score >= 50:
        return "#f59e0b"  # Amber
    return "#f43f5e"  # Rose


# =========================================================
# HEADER COMPONENT
# =========================================================

st.markdown(
    """
<div class="hero-container">
    <div class="hero-badge">⚡ AI-Powered Fit Engine</div>
    <h1 class="hero-title">Resume & Job Fit Analyzer</h1>
    <p class="hero-subtitle">
        Intelligent candidate evaluation against target job requirements.
        Generates in-depth analysis on Strengths, Weaknesses, Areas to Improve, and Final Verdict.
    </p>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# INPUT SECTION
# =========================================================

col_jd, col_resume = st.columns([1.1, 0.9], gap="large")

with col_jd:
    st.markdown(
        '<div class="section-title">📋 1. Job Description</div>',
        unsafe_allow_html=True,
    )
    job_description = st.text_area(
        "Job Description Input",
        height=280,
        placeholder="Paste target job requirements, qualifications, and role responsibilities here...",
        label_visibility="collapsed",
    )

with col_resume:
    st.markdown(
        '<div class="section-title">📄 2. Candidate Resume (PDF)</div>',
        unsafe_allow_html=True,
    )
    resume_file = st.file_uploader(
        "Upload Candidate Resume PDF",
        type=["pdf"],
        help="Upload the candidate's resume in PDF format",
        label_visibility="collapsed",
    )

    if resume_file:
        file_size_kb = resume_file.size / 1024
        st.markdown(
            f"""
            <div class="file-info-badge">
                <span>📄 <strong>{resume_file.name}</strong></span>
                <span style="color:#94a3b8;">{file_size_kb:.1f} KB</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

# Action Button
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    analyze_clicked = st.button("🚀 Analyze Candidate Fit", use_container_width=True)


# =========================================================
# ANALYSIS PIPELINE EXECUTION
# =========================================================

if analyze_clicked:
    if not job_description.strip():
        st.warning("⚠️ Please provide a job description before analyzing.")
    elif resume_file is None:
        st.warning("⚠️ Please upload a PDF resume to proceed.")
    else:
        # Safe temporary file management
        temp_pdf_path = None
        try:
            with st.spinner("Analyzing candidate profile and requirements..."):
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as temp_pdf:
                    temp_pdf.write(resume_file.getbuffer())
                    temp_pdf_path = temp_pdf.name

                # Execute core backend analysis
                parsed_resume, match_result = analyze_resume(
                    temp_pdf_path, job_description
                )

                # Persist in session state
                st.session_state["analyzed_resume"] = parsed_resume
                st.session_state["match_result"] = match_result
                st.session_state["job_description"] = job_description
                st.session_state["file_name"] = resume_file.name

        except Exception as err:
            st.error(f"❌ Analysis failed: {err}")
        finally:
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                try:
                    os.remove(temp_pdf_path)
                except OSError:
                    pass


# =========================================================
# RESULTS DASHBOARD DISPLAY
# =========================================================

if "match_result" in st.session_state and "analyzed_resume" in st.session_state:
    parsed_resume = st.session_state["analyzed_resume"]
    match_result = st.session_state["match_result"]
    details = match_result.details if hasattr(match_result, "details") else {}
    score_val = float(getattr(match_result, "score", 0.0))

    # ---------------------------------------------------------
    # DATA EXTRACTION WITH RESILIENT FALLBACKS
    # ---------------------------------------------------------

    candidate_name = (
        getattr(parsed_resume, "name", None)
        or extract_field(
            details,
            "candidate_name",
            "Candidate_name",
            "name",
            default="Candidate",
        )
    )

    matching_skills = normalize_items(
        extract_field(
            details,
            "matching_skills",
            "Matching_skills",
            "matched_skills",
            default=[],
        )
    )

    missing_skills = normalize_items(
        extract_field(
            details,
            "missing_important_skills",
            "Missing_important_skills",
            "missing_skills",
            "missing_qualifications",
            default=[],
        )
    )

    experience_met = extract_field(
        details,
        "experience_met",
        "Experience_met",
        "experience_requirement_met",
        default=None,
    )

    # Strengths Extraction
    strengths = normalize_items(
        extract_field(
            details,
            "strengths",
            "Strengths",
            "key_strengths",
            "candidate_strengths",
            "advantages",
            default=[],
        )
    )
    if not strengths and matching_skills:
        strengths = [
            f"Demonstrates relevant proficiency in {', '.join(matching_skills[:3])}."
        ]
        if getattr(parsed_resume, "Total_exp", None):
            strengths.append(
                f"Brings {parsed_resume.Total_exp} of professional background."
            )
        if getattr(parsed_resume, "projects", None):
            strengths.append(
                f"Possesses hands-on project experience across {len(parsed_resume.projects)} documented initiatives."
            )

    # Weaknesses Extraction
    weaknesses = normalize_items(
        extract_field(
            details,
            "weaknesses",
            "Weaknesses",
            "weakness",
            "candidate_weaknesses",
            "gaps",
            "deficiencies",
            default=[],
        )
    )
    if not weaknesses and missing_skills:
        weaknesses = [
            f"Missing required technical competencies in {', '.join(missing_skills[:3])}."
        ]
        if experience_met is False:
            weaknesses.append("Does not meet stated minimum years of experience.")

    # Areas to Improve Extraction
    areas_to_improve = normalize_items(
        extract_field(
            details,
            "areas_to_improve",
            "Areas_to_improve",
            "areas_for_improvement",
            "improvement_areas",
            "recommendations",
            "suggestions",
            "how_to_improve",
            default=[],
        )
    )
    if not areas_to_improve:
        if missing_skills:
            areas_to_improve.append(
                f"Gain verified proficiency in {', '.join(missing_skills[:2])} via certifications or production code."
            )
        areas_to_improve.append(
            "Emphasize measurable business impact and scale metrics in resume project descriptions."
        )
        areas_to_improve.append(
            "Align resume terminology more directly with target job responsibilities."
        )

    # Final Verdict Extraction
    final_verdict = extract_field(
        details,
        "final_verdict",
        "Final_verdict",
        "verdict",
        "Verdict",
        "recruiter_verdict",
        "summary",
        default="Candidate evaluation complete. Review the strengths and weakness breakdown for details.",
    )

    st.markdown("---")

    # ---------------------------------------------------------
    # 1. CANDIDATE PROFILE & SCORE OVERVIEW
    # ---------------------------------------------------------

    overview_col1, overview_col2 = st.columns([1.8, 0.9], gap="medium")

    with overview_col1:
        # Experience met badge formatting
        if experience_met is True:
            exp_badge = '<span class="exp-badge-met">✓ Experience Requirement Met</span>'
        elif experience_met is False:
            exp_badge = '<span class="exp-badge-unmet">✕ Experience Requirement Not Met</span>'
        else:
            exp_badge = '<span style="color:#94a3b8; font-size:0.82rem;">Experience requirement: Unspecified</span>'

        total_exp_str = getattr(parsed_resume, "Total_exp", None) or "Not specified"
        email_str = getattr(parsed_resume, "email", None) or ""

        st.markdown(
            f"""
            <div class="candidate-hero-card">
                <div>
                    <div class="section-title">Candidate Evaluation</div>
                    <div class="candidate-name-text">{candidate_name}</div>
                    <div class="candidate-tagline">
                        <span>💼 <strong>Total Exp:</strong> {total_exp_str}</span>
                        {f'<span>✉️ {email_str}</span>' if email_str else ''}
                        {exp_badge}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with overview_col2:
        score_color = get_score_color(score_val)
        st.markdown(
            f"""
            <div class="score-hero-box">
                <div class="score-hero-number" style="color: {score_color};">
                    {score_val:.0f}%
                </div>
                <div class="score-hero-label">Overall Match Score</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Match Progress Bar
    st.progress(min(max(score_val / 100.0, 0.0), 1.0))
    st.write("")

    # ---------------------------------------------------------
    # 2. FINAL VERDICT BANNER
    # ---------------------------------------------------------

    st.markdown(
        f"""
        <div class="verdict-container">
            <div class="verdict-badge">🎯 Executive Recruiter Verdict</div>
            <div class="verdict-content">{final_verdict}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # ---------------------------------------------------------
    # 3. STRENGTHS, WEAKNESSES & AREAS TO IMPROVE GRID
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Detailed Fit Analysis</div>',
        unsafe_allow_html=True,
    )

    card_col1, card_col2, card_col3 = st.columns(3, gap="medium")

    # ---- STRENGTHS CARD ----
    with card_col1:
        strengths_html = "".join(
            f'<div class="analysis-item-row"><span class="bullet-icon-emerald">✓</span><span>{item}</span></div>'
            for item in strengths
        ) or '<div class="chip-empty">No major strengths highlighted.</div>'

        st.markdown(
            f"""
            <div class="analysis-card card-strengths">
                <div class="card-header-row">
                    <span style="font-size:1.2rem;">✨</span>
                    <h3 class="card-title-text">Strengths</h3>
                </div>
                <div class="card-desc-text">Key candidate advantages and strong alignments.</div>
                <div>{strengths_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- WEAKNESSES CARD ----
    with card_col2:
        weaknesses_html = "".join(
            f'<div class="analysis-item-row"><span class="bullet-icon-rose">✕</span><span>{item}</span></div>'
            for item in weaknesses
        ) or '<div class="chip-empty">No critical weaknesses identified.</div>'

        st.markdown(
            f"""
            <div class="analysis-card card-weaknesses">
                <div class="card-header-row">
                    <span style="font-size:1.2rem;">⚠️</span>
                    <h3 class="card-title-text">Weaknesses</h3>
                </div>
                <div class="card-desc-text">Gaps, missing skills, and qualification risks.</div>
                <div>{weaknesses_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- AREAS TO IMPROVE CARD ----
    with card_col3:
        improvements_html = "".join(
            f'<div class="analysis-item-row"><span class="bullet-icon-cyan">💡</span><span>{item}</span></div>'
            for item in areas_to_improve
        ) or '<div class="chip-empty">No improvement areas specified.</div>'

        st.markdown(
            f"""
            <div class="analysis-card card-improvements">
                <div class="card-header-row">
                    <span style="font-size:1.2rem;">📈</span>
                    <h3 class="card-title-text">Areas to Improve</h3>
                </div>
                <div class="card-desc-text">Actionable recommendations to bridge gaps.</div>
                <div>{improvements_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # ---------------------------------------------------------
    # 4. SKILLS BREAKDOWN (MATCHING VS MISSING)
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">🧩 Technical & Domain Skills Breakdown</div>',
        unsafe_allow_html=True,
    )

    skill_col_left, skill_col_right = st.columns(2, gap="medium")

    with skill_col_left:
        st.markdown(
            f"""
            <div class="analysis-card">
                <div class="card-header-row">
                    <span style="font-size:1.1rem;">✅</span>
                    <h3 class="card-title-text">Matching Skills ({len(matching_skills)})</h3>
                </div>
                <div class="card-desc-text">Skills present in resume that match job requirements.</div>
                {render_chips(matching_skills, missing=False)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with skill_col_right:
        st.markdown(
            f"""
            <div class="analysis-card">
                <div class="card-header-row">
                    <span style="font-size:1.1rem;">🔍</span>
                    <h3 class="card-title-text">Missing Important Skills ({len(missing_skills)})</h3>
                </div>
                <div class="card-desc-text">Key job requirements not evidenced in the resume.</div>
                {render_chips(missing_skills, missing=True)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # ---------------------------------------------------------
    # 5. EXPANDABLE TECHNICAL DETAILS & EXPORT
    # ---------------------------------------------------------

    with st.expander("🔍 View Extracted Candidate Profile"):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.markdown(f"**Name:** {getattr(parsed_resume, 'name', 'N/A')}")
            st.markdown(f"**Email:** {getattr(parsed_resume, 'email', 'N/A')}")
            st.markdown(f"**Phone:** {getattr(parsed_resume, 'phone', 'N/A')}")
            st.markdown(
                f"**Total Experience:** {getattr(parsed_resume, 'Total_exp', 'N/A')}"
            )
            st.markdown("**Education:**")
            for edu in getattr(parsed_resume, "education", []):
                st.markdown(f"- {edu}")
        with p_col2:
            st.markdown("**Parsed Skills:**")
            st.write(", ".join(getattr(parsed_resume, "skills", [])) or "None")
            st.markdown("**Projects:**")
            for proj in getattr(parsed_resume, "projects", []):
                st.markdown(f"- {proj}")
            st.markdown("**Certifications:**")
            for cert in getattr(parsed_resume, "certifications", []):
                st.markdown(f"- {cert}")

    with st.expander("📊 View Raw Evaluation Payload"):
        st.json(details)

    # Export Report
    st.write("")
    report_text = f"""# Candidate Fit Analysis Report
**Candidate Name:** {candidate_name}
**Overall Match Score:** {score_val:.0f}%
**Experience Requirement Met:** {'Yes' if experience_met is True else 'No' if experience_met is False else 'Unspecified'}

## Executive Verdict
{final_verdict}

## Strengths
{chr(10).join(f"- {s}" for s in strengths)}

## Weaknesses
{chr(10).join(f"- {w}" for w in weaknesses)}

## Areas to Improve
{chr(10).join(f"- {a}" for a in areas_to_improve)}

## Matching Skills
{', '.join(matching_skills) if matching_skills else 'None'}

## Missing Important Skills
{', '.join(missing_skills) if missing_skills else 'None'}
"""

    exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 1])
    with exp_col2:
        st.download_button(
            label="📥 Download Analysis Report (Markdown)",
            data=report_text,
            file_name=f"fit_analysis_{candidate_name.lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="app-footer">
    AI Resume & Candidate Fit Analyzer • Built with Streamlit & Groq
</div>
""",
    unsafe_allow_html=True,
)
