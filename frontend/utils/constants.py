"""CareerPilot AI — Design tokens, navigation, and configuration."""
from pathlib import Path

# ── Paths ───────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
CSS_PATH = ASSETS_DIR / "styles.css"
LOGO_PATH = ASSETS_DIR / "logo.png"

# ── API ─────────────────────────────────────────────────────
DEFAULT_API_URL = "http://localhost:8000"
API_TIMEOUT = 30

# ── Theme Colors ────────────────────────────────────────────
COLORS = {
    "primary": "#2563EB",
    "secondary": "#1E293B",
    "accent": "#06B6D4",
    "background": "#F8FAFC",
    "success": "#22C55E",
    "success_dark": "#15803D",
    "warning": "#F59E0B",
    "danger": "#EF4444",
}

# ── Match Score Thresholds ──────────────────────────────────
MATCH_EXCELLENT = 90
MATCH_GOOD = 80
MATCH_FAIR = 60

# ── Navigation ──────────────────────────────────────────────
NAV_ITEMS = [
    {"id": "home", "label": "Dashboard", "icon": "🏠"},
    {"id": "cv_analysis", "label": "CV Analysis", "icon": "📄"},
    {"id": "job_recommendations", "label": "Job Matches", "icon": "💼"},
    {"id": "career_insights", "label": "Career Insights", "icon": "📊"},
    {"id": "cover_letter", "label": "Cover Letter", "icon": "✉️"},
    {"id": "scam_detector", "label": "Scam Detector", "icon": "🛡️"},
    {"id": "report", "label": "Career Report", "icon": "📋"},
]

# ── Page Titles ─────────────────────────────────────────────
PAGE_TITLES = {
    "home": "Dashboard",
    "cv_analysis": "CV Analysis",
    "job_recommendations": "Job Recommendations",
    "career_insights": "Career Insights",
    "cover_letter": "AI Cover Letter",
    "scam_detector": "Scam Detector",
    "report": "Career Report",
}
