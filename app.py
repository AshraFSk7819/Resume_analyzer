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
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 5rem;
}

/* Hero / Header Section */
.hero-container {
    background: #18181B;
    border: 1px solid #3F3F46;
    border-radius: 8px;
    padding: 2rem 2.5rem;
    margin-bottom: 2.5rem;
}

.hero-badge {
    display: inline-block;
    color: #93C5FD;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-size: 2rem;
    font-weight: 600;
    color: #FAFAFA;
    letter-spacing: -0.01em;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
}

.hero-subtitle {
    color: #A1A1AA;
    font-size: 0.95rem;
    margin: 0;
    line-height: 1.5;
    max-width: 800px;
}

/* Section Headings */
.section-title {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #A1A1AA;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #3F3F46;
    padding-bottom: 0.5rem;
}

/* Input Fields overrides */
textarea {
    border-radius: 6px !important;
}

[data-testid="stFileUploader"] {
    border-radius: 6px;
    padding: 1rem;
}

/* Primary Button - Clean Corporate Look */
.stButton > button {
    height: 44px;
    border-radius: 6px;
    background: #FAFAFA;
    border: 1px solid #E4E4E7;
    color: #18181B;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    background: #E4E4E7;
    border-color: #D4D4D8;
    color: #18181B;
}

/* File Info Box */
.file-info-badge {
    background: #18181B;
    border: 1px solid #3F3F46;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin-top: 0.5rem;
    color: #D4D4D8;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Candidate Overview Hero Card */
.candidate-hero-card {
    background: #18181B;
    border: 1px solid #3F3F46;
    border-radius: 8px;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    height: 100%;
}

.candidate-name-text {
    font-size: 1.5rem;
    font-weight: 600;
    color: #FAFAFA;
    margin: 0.25rem 0 0.5rem 0;
    line-height: 1.2;
}

.candidate-tagline {
    color: #A1A1AA;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.candidate-tagline span {
    display: flex;
    align-items: center;
}

.exp-badge-met {
    color: #34D399;
    font-weight: 500;
}

.exp-badge-unmet {
    color: #F87171;
    font-weight: 500;
}

/* Score Card */
.score-hero-box {
    background: #18181B;
    border: 1px solid #3F3F46;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.score-hero-label {
    color: #A1A1AA;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}

.score-hero-number {
    font-size: 2.5rem;
    font-weight: 600;
    line-height: 1;
}

/* Analysis Cards */
.analysis-card {
    background: #18181B;
    border: 1px solid #3F3F46;
    border-radius: 8px;
    padding: 1.5rem;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.card-header-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;
}

.card-title-text {
    font-size: 1rem;
    font-weight: 600;
    color: #FAFAFA;
    margin: 0;
}

.card-desc-text {
    color: #A1A1AA;
    font-size: 0.82rem;
    margin-bottom: 1.25rem;
    line-height: 1.4;
}

/* Structural Bullet Items */
.analysis-item-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 0.75rem;
    font-size: 0.88rem;
    color: #D4D4D8;
    line-height: 1.5;
}

.bullet-icon {
    font-size: 1rem;
    flex-shrink: 0;
    margin-top: 0px;
    font-weight: 700;
}

.bullet-pos { color: #10B981; }
.bullet-neg { color: #EF4444; }
.bullet-neu { color: #3B82F6; }

/* Verdict Box */
.verdict-container {
    background: #18181B;
    border: 1px solid #3F3F46;
    border-left: 3px solid #3B82F6;
    border-radius: 6px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.verdict-badge {
    color: #93C5FD;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.verdict-content {
    color: #FAFAFA;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Skills Chips */
.skills-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.chip-match {
    background: #064E3B;
    border: 1px solid #047857;
    color: #A7F3D0;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 4px;
}

.chip-missing {
    background: #7F1D1D;
    border: 1px solid #B91C1C;
    color: #FECACA;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 4px;
}

.chip-empty {
    color: #71717A;
    font-size: 0.85rem;
    font-style: italic;
}

/* Clean Expander overrides */
[data-testid="stExpander"] {
    border: 1px solid #3F3F46 !important;
    border-radius: 6px !important;
}

/* Footer */
.app-footer {
    text-align: center;
    color: #71717A;
    font-size: 0.75rem;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #3F3F46;
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

    for key in keys:
        if key in details and details[key] is not None:
            return details[key]

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
        return "#34D399"  # Emerald
    if score >= 50:
        return "#FBBF24"  # Amber
    return "#F87171"  # Red


# =========================================================
# HEADER COMPONENT
# =========================================================

st.markdown(
    """
<div class="hero-container">
    <div class="hero-badge">Evaluation Engine</div>
    <h1 class="hero-title">AI Resume & Job Fit Analyzer</h1>
    <p class="hero-subtitle">
        Automated candidate assessment against target requirements. 
        Generates structured feedback on alignment, gaps, and recommendations.
    </p>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# INPUT SECTION
# =========================================================

col_jd, col_resume = st.columns([1, 1], gap="large")

with col_jd:
    st.markdown(
        '<div class="section-title">1. Job Description</div>',
        unsafe_allow_html=True,
    )
    job_description = st.text_area(
        "Job Description Input",
        height=280,
        placeholder="Paste target job requirements, qualifications, and role responsibilities...",
        label_visibility="collapsed",
    )

with col_resume:
    st.markdown(
        '<div class="section-title">2. Candidate Resume</div>',
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
                <span style="font-weight: 500;">{resume_file.name}</span>
                <span style="color:#A1A1AA;">{file_size_kb:.1f} KB</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

# Action Button
btn_col1, btn_col2, btn_col3 = st.columns([1.5, 2, 1.5])
with btn_col2:
    analyze_clicked = st.button("Analyze Candidate Fit", use_container_width=True)


# =========================================================
# ANALYSIS PIPELINE EXECUTION
# =========================================================

if analyze_clicked:
    if not job_description.strip():
        st.warning("Please provide a job description before analyzing.")
    elif resume_file is None:
        st.warning("Please upload a PDF resume to proceed.")
    else:
        temp_pdf_path = None
        try:
            with st.spinner("Processing candidate profile and requirements..."):
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
            st.error(f"Analysis failed: {err}")
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
        strengths = [f"Demonstrates relevant proficiency in {', '.join(matching_skills[:3])}."]

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
        weaknesses = [f"Missing required technical competencies in {', '.join(missing_skills[:3])}."]

    areas_to_improve = normalize_items(
        extract_field(
            details,
            "areas_to_improve",
            "Areas_to_improve",
            "areas_for_improvement",
            "improvement_areas",
            "recommendations",
            default=[],
        )
    )
    if not areas_to_improve and missing_skills:
        areas_to_improve.append("Align resume terminology more directly with target job responsibilities.")

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

    overview_col1, overview_col2 = st.columns([2.5, 1], gap="medium")

    with overview_col1:
        if experience_met is True:
            exp_badge = '<span class="exp-badge-met">Experience Met</span>'
        elif experience_met is False:
            exp_badge = '<span class="exp-badge-unmet">Experience Not Met</span>'
        else:
            exp_badge = '<span style="color:#A1A1AA;">Experience Unspecified</span>'

        total_exp_str = getattr(parsed_resume, "Total_exp", None) or "Not specified"
        email_str = getattr(parsed_resume, "email", None) or ""

        st.markdown(
            f"""
            <div class="candidate-hero-card">
                <div>
                    <div style="color: #A1A1AA; font-size: 0.75rem; text-transform: uppercase; font-weight: 600; margin-bottom: 0.25rem;">Evaluation Profile</div>
                    <div class="candidate-name-text">{candidate_name}</div>
                    <div class="candidate-tagline">
                        <span>Exp: {total_exp_str}</span>
                        {f'<span>{email_str}</span>' if email_str else ''}
                        <span>•</span>
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
                <div class="score-hero-label">Overall Match</div>
                <div class="score-hero-number" style="color: {score_color};">
                    {score_val:.0f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------------
    # 2. FINAL VERDICT BANNER
    # ---------------------------------------------------------
    st.write("")
    st.markdown(
        f"""
        <div class="verdict-container">
            <div class="verdict-badge">Executive Summary</div>
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
        '<div class="section-title">Detailed Fit Analysis</div>',
        unsafe_allow_html=True,
    )

    card_col1, card_col2, card_col3 = st.columns(3, gap="medium")

    with card_col1:
        strengths_html = "".join(
            f'<div class="analysis-item-row"><span class="bullet-icon bullet-pos">+</span><span>{item}</span></div>'
            for item in strengths
        ) or '<div class="chip-empty">No major strengths highlighted.</div>'

        st.markdown(
            f"""
            <div class="analysis-card">
                <div class="card-header-row">
                    <h3 class="card-title-text">Strengths</h3>
                </div>
                <div class="card-desc-text">Key candidate advantages and alignments.</div>
                <div>{strengths_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with card_col2:
        weaknesses_html = "".join(
            f'<div class="analysis-item-row"><span class="bullet-icon bullet-neg">-</span><span>{item}</span></div>'
            for item in weaknesses
        ) or '<div class="chip-empty">No critical weaknesses identified.</div>'

        st.markdown(
            f"""
            <div class="analysis-card">
                <div class="card-header-row">
                    <h3 class="card-title-text">Weaknesses</h3>
                </div>
                <div class="card-desc-text">Gaps and qualification risks.</div>
                <div>{weaknesses_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with card_col3:
        improvements_html = "".join(
            f'<div class="analysis-item-row"><span class="bullet-icon bullet-neu">→</span><span>{item}</span></div>'
            for item in areas_to_improve
        ) or '<div class="chip-empty">No improvement areas specified.</div>'

        st.markdown(
            f"""
            <div class="analysis-card">
                <div class="card-header-row">
                    <h3 class="card-title-text">Recommendations</h3>
                </div>
                <div class="card-desc-text">Actionable steps to bridge current gaps.</div>
                <div>{improvements_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # ---------------------------------------------------------
    # 4. SKILLS BREAKDOWN
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Technical Competency Assessment</div>',
        unsafe_allow_html=True,
    )

    skill_col_left, skill_col_right = st.columns(2, gap="medium")

    with skill_col_left:
        st.markdown(
            f"""
            <div class="analysis-card" style="padding-bottom: 2rem;">
                <div class="card-header-row">
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
            <div class="analysis-card" style="padding-bottom: 2rem;">
                <div class="card-header-row">
                    <h3 class="card-title-text">Missing Required Skills ({len(missing_skills)})</h3>
                </div>
                <div class="card-desc-text">Key job requirements not evidenced in the resume.</div>
                {render_chips(missing_skills, missing=True)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # ---------------------------------------------------------
    # 5. EXPANDABLE TECHNICAL DETAILS & EXPORT
    # ---------------------------------------------------------

    with st.expander("View Extracted Candidate Profile Data"):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.markdown(f"**Name:** {getattr(parsed_resume, 'name', 'N/A')}")
            st.markdown(f"**Email:** {getattr(parsed_resume, 'email', 'N/A')}")
            st.markdown(f"**Phone:** {getattr(parsed_resume, 'phone', 'N/A')}")
            st.markdown(f"**Total Experience:** {getattr(parsed_resume, 'Total_exp', 'N/A')}")
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

    with st.expander("View Raw JSON Evaluation Payload"):
        st.json(details)

    # Export Report
    st.write("")
    report_text = f"""# Candidate Fit Analysis Report
**Candidate Name:** {candidate_name}
**Overall Match Score:** {score_val:.0f}%
**Experience Requirement Met:** {'Yes' if experience_met is True else 'No' if experience_met is False else 'Unspecified'}

## Executive Summary
{final_verdict}

## Strengths
{chr(10).join(f"- {s}" for s in strengths)}

## Weaknesses
{chr(10).join(f"- {w}" for w in weaknesses)}

## Recommendations
{chr(10).join(f"- {a}" for a in areas_to_improve)}

## Matching Skills
{', '.join(matching_skills) if matching_skills else 'None'}

## Missing Important Skills
{', '.join(missing_skills) if missing_skills else 'None'}
"""

    exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 1])
    with exp_col2:
        st.download_button(
            label="Download Analysis Report (.md)",
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
    AI Resume & Candidate Fit Analyzer
</div>
""",
    unsafe_allow_html=True,
)