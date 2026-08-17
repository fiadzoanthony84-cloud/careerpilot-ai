"""CareerPilot AI — UI helper functions and HTML component builders."""

from __future__ import annotations

import base64
import html
import math
from pathlib import Path

from .constants import (
    CSS_PATH,
    LOGO_PATH,
    MATCH_EXCELLENT,
    MATCH_FAIR,
    MATCH_GOOD,
)


def load_css() -> str:
    """Read custom stylesheet from assets."""
    if CSS_PATH.exists():
        return CSS_PATH.read_text(encoding="utf-8")
    return ""


def get_logo_base64() -> str:
    """Encode logo as base64 data URI for inline HTML."""
    if LOGO_PATH.exists():
        data = LOGO_PATH.read_bytes()
        b64 = base64.b64encode(data).decode()
        return f"data:image/png;base64,{b64}"
    return ""


def get_initials(name: str) -> str:
    """Extract up to two initials from a full name."""
    parts = name.strip().split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][0].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def get_match_tier(score: int) -> tuple[str, str]:
    """Return CSS class suffix and label for a match score."""
    if score >= MATCH_EXCELLENT:
        return "excellent", "Excellent Match"
    if score >= MATCH_GOOD:
        return "good", "Strong Match"
    if score >= MATCH_FAIR:
        return "fair", "Moderate Match"
    return "poor", "Low Match"


def format_currency(amount: int) -> str:
    """Format integer salary as GBP currency string."""
    return f"£{amount:,}"


def count_words(text: str) -> int:
    """Count words in a text block."""
    return len(text.split()) if text.strip() else 0


def reading_time_minutes(text: str, wpm: int = 200) -> int:
    """Estimate reading time in minutes."""
    words = count_words(text)
    return max(1, math.ceil(words / wpm))


def esc(text: str) -> str:
    """HTML-escape user-provided text."""
    return html.escape(str(text))


def build_skill_badges(skills: list[str], css_class: str = "") -> str:
    """Render LinkedIn-style skill chip badges."""
    badges = []
    for skill in skills:
        cls = f"cp-skill-badge {css_class}".strip()
        badges.append(f'<span class="{cls}">{esc(skill)}</span>')
    return f'<div class="cp-skills-container">{"".join(badges)}</div>'


def build_metric_card(icon: str, value: str, label: str, icon_class: str = "blue", trend: str = "", delay: int = 0) -> str:
    """Render an animated dashboard metric card."""
    trend_html = f'<div class="cp-metric-trend up">{esc(trend)}</div>' if trend else ""
    delay_class = f" animate-delay-{delay}" if delay else ""
    return f"""
    <div class="cp-metric-card animate-fade-in{delay_class}">
        <div class="cp-metric-icon {icon_class}">{icon}</div>
        <div class="cp-metric-value">{esc(value)}</div>
        <div class="cp-metric-label">{esc(label)}</div>
        {trend_html}
    </div>
    """


def build_profile_card(cv: dict) -> str:
    """Render candidate profile summary card."""
    name = cv.get("name", "Unknown")
    qual = cv.get("top_qualification", "N/A")
    skills_count = len(cv.get("skills", []))
    exp_count = len(cv.get("experience", []))

    return f"""
    <div class="cp-profile-card">
        <div class="cp-avatar">{esc(get_initials(name))}</div>
        <div class="cp-profile-info">
            <h2>{esc(name)}</h2>
            <div class="qualification">{esc(qual)}</div>
            <div class="cp-profile-stats">
                <div class="cp-profile-stat">
                    <div class="num">{skills_count}</div>
                    <div class="lbl">Skills</div>
                </div>
                <div class="cp-profile-stat">
                    <div class="num">{len(cv.get('education', []))}</div>
                    <div class="lbl">Qualifications</div>
                </div>
                <div class="cp-profile-stat">
                    <div class="num">{exp_count}</div>
                    <div class="lbl">Experience</div>
                </div>
            </div>
        </div>
    </div>
    """


def build_timeline_items(items: list[dict], key_title: str = "title", key_org: str = "company") -> str:
    """Render education or experience timeline entries."""
    rows = []
    for item in items:
        title = item.get(key_title, item.get("degree", ""))
        org = item.get(key_org, item.get("institution", ""))
        period = item.get("period", item.get("year", ""))
        detail = item.get("description", item.get("details", ""))
        detail_html = f'<p style="font-size:0.82rem;color:var(--text-muted);margin:0.3rem 0 0;">{esc(detail)}</p>' if detail else ""
        rows.append(f"""
        <div class="cp-timeline-item">
            <div class="cp-timeline-dot"></div>
            <div class="cp-timeline-content">
                <h4>{esc(title)}</h4>
                <div class="org">{esc(org)}</div>
                <div class="period">{esc(period)}</div>
                {detail_html}
            </div>
        </div>
        """)
    return "".join(rows)


def build_job_card(job: dict) -> str:
    """Render a premium LinkedIn-style job recommendation card."""
    score = job.get("match_score", 0)
    tier, tier_label = get_match_tier(score)
    required = build_skill_badges(job.get("required_skills", []))
    missing = build_skill_badges(job.get("missing_skills", []), "missing")

    return f"""
    <div class="cp-job-card">
        <div class="cp-job-rank">#{job.get('rank', '?')}</div>
        <div class="cp-job-header">
            <div>
                <div class="cp-job-title">{esc(job.get('title', ''))}</div>
                <div class="cp-job-company">{esc(job.get('company', ''))}</div>
            </div>
        </div>
        <div class="cp-job-meta">
            <span class="cp-job-tag">📍 {esc(job.get('location', ''))}</span>
            <span class="cp-job-tag">🏢 {esc(job.get('industry', ''))}</span>
            <span class="cp-job-tag">💰 {esc(job.get('salary', ''))}</span>
        </div>
        <div class="cp-match-score">
            <span class="cp-match-label">{tier_label}</span>
            <div class="cp-progress-bar">
                <div class="cp-progress-fill {tier}" style="width:{score}%;"></div>
            </div>
            <span class="cp-match-percent {tier}">{score}%</span>
        </div>
        <div class="cp-job-skills-section">
            <h4>Required Skills</h4>
            {required}
        </div>
        <div class="cp-job-skills-section">
            <h4>Skills to Develop</h4>
            {missing}
        </div>
        <div class="cp-job-description">{esc(job.get('description', ''))}</div>
    </div>
    """


def build_document_viewer(title: str, content: str) -> str:
    """Render AI document preview with toolbar."""
    words = count_words(content)
    read_time = reading_time_minutes(content)
    return f"""
    <div class="cp-document-viewer">
        <div class="cp-document-toolbar">
            <div class="dots">
                <span class="dot-red"></span>
                <span class="dot-yellow"></span>
                <span class="dot-green"></span>
            </div>
            <div class="cp-document-title">{esc(title)}</div>
            <div></div>
        </div>
        <div class="cp-document-body">{esc(content)}</div>
        <div class="cp-document-meta">
            <span>📝 {words} words</span>
            <span>⏱ {read_time} min read</span>
            <span>🤖 AI Generated</span>
        </div>
    </div>
    """


def build_scam_result(result: dict) -> str:
    """Render scam detection result card."""
    level = result.get("risk_level", "moderate")
    flags_html = ""
    if result.get("flags"):
        flags_items = "".join(f"<li>{esc(f)}</li>" for f in result["flags"])
        flags_html = f'<ul style="text-align:left;margin:1rem auto;max-width:400px;color:var(--danger);">{flags_items}</ul>'

    details_items = "".join(f"<li>{esc(d)}</li>" for d in result.get("details", []))
    details_html = f'<ul style="text-align:left;margin:1rem auto;max-width:450px;font-size:0.88rem;">{details_items}</ul>'

    return f"""
    <div class="cp-scam-result {level}">
        <div class="cp-scam-icon">{result.get('risk_icon', '⚠️')}</div>
        <div class="cp-scam-label {level}">{esc(result.get('risk_label', 'UNKNOWN'))}</div>
        <div class="cp-scam-detail">Analysis complete — review the indicators below.</div>
        {details_html}
        {flags_html}
    </div>
    """


def build_empty_state(icon: str, title: str, message: str) -> str:
    """Render a friendly empty state placeholder."""
    return f"""
    <div class="cp-empty-state animate-fade-in">
        <div class="icon">{icon}</div>
        <h3>{esc(title)}</h3>
        <p>{esc(message)}</p>
    </div>
    """


def build_hero_section(subtitle: str = "") -> str:
    """Render the animated dashboard hero banner."""
    return f"""
    <div class="cp-hero animate-fade-in">
        <div class="cp-hero-content">
            <div class="cp-hero-badge"><span class="dot"></span> AI-Powered Platform</div>
            <h1>CAREERPILOT AI</h1>
            <p>{esc(subtitle or "Smart Career Guidance & Job Matching Platform")}</p>
            <div class="cp-hero-stats">
                <div class="cp-hero-stat">
                    <div class="value">AI</div>
                    <div class="label">Powered Analysis</div>
                </div>
                <div class="cp-hero-stat">
                    <div class="value">Real-time</div>
                    <div class="label">Job Matching</div>
                </div>
                <div class="cp-hero-stat">
                    <div class="value">Secure</div>
                    <div class="label">Scam Detection</div>
                </div>
            </div>
        </div>
    </div>
    """
