"""CareerPilot AI — Backend API client with graceful fallback."""

from __future__ import annotations

import io
import logging
import os
from typing import Any

import requests

from .constants import API_TIMEOUT, DEFAULT_API_URL
from .mock_data import (
    get_demo_cover_letter,
    get_demo_cv_analysis,
    get_demo_insights,
    get_demo_recommendations,
    get_demo_scam_analysis,
)

logger = logging.getLogger(__name__)


class CareerPilotAPI:
    """HTTP client for the CareerPilot backend with demo-mode fallback."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("CAREERPILOT_API_URL", DEFAULT_API_URL)).rstrip("/")
        self._backend_available: bool | None = None

    # ── Health ──────────────────────────────────────────────

    def check_health(self) -> bool:
        """Ping backend; cache result for the session."""
        if self._backend_available is not None:
            return self._backend_available
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=3)
            self._backend_available = resp.status_code == 200
        except requests.RequestException:
            self._backend_available = False
        return self._backend_available

    @property
    def is_demo_mode(self) -> bool:
        return not self.check_health()

    # ── CV Upload & Analysis ──────────────────────────────────

    def upload_and_analyze_cv(self, file_bytes: bytes, filename: str) -> dict[str, Any]:
        """Upload CV file and return parsed analysis."""
        if self.is_demo_mode:
            logger.info("Demo mode — returning sample CV analysis")
            return get_demo_cv_analysis()

        try:
            files = {"file": (filename, io.BytesIO(file_bytes))}
            resp = requests.post(
                f"{self.base_url}/api/cv/analyze",
                files=files,
                timeout=API_TIMEOUT,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.warning("CV analysis failed, using demo data: %s", exc)
            return get_demo_cv_analysis()

    # ── Job Recommendations ───────────────────────────────────

    def get_recommendations(self, cv_data: dict | None = None) -> list[dict]:
        """Fetch personalised job recommendations."""
        if self.is_demo_mode:
            return get_demo_recommendations()

        try:
            resp = requests.post(
                f"{self.base_url}/api/jobs/recommend",
                json=cv_data or {},
                timeout=API_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else data.get("recommendations", [])
        except requests.RequestException as exc:
            logger.warning("Recommendations failed, using demo data: %s", exc)
            return get_demo_recommendations()

    # ── Career Insights ───────────────────────────────────────

    def get_insights(self, cv_data: dict | None = None) -> dict:
        """Fetch career insights and analytics."""
        if self.is_demo_mode:
            return get_demo_insights()

        try:
            resp = requests.post(
                f"{self.base_url}/api/insights",
                json=cv_data or {},
                timeout=API_TIMEOUT,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.warning("Insights failed, using demo data: %s", exc)
            return get_demo_insights()

    # ── Cover Letter ──────────────────────────────────────────

    def generate_cover_letter(self, job: dict, cv_data: dict) -> str:
        """Generate an AI cover letter for a selected job."""
        if self.is_demo_mode:
            return get_demo_cover_letter(job, cv_data)

        try:
            resp = requests.post(
                f"{self.base_url}/api/cover-letter/generate",
                json={"job": job, "cv": cv_data},
                timeout=API_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("letter", data.get("cover_letter", ""))
        except requests.RequestException as exc:
            logger.warning("Cover letter failed, using demo data: %s", exc)
            return get_demo_cover_letter(job, cv_data)

    # ── Scam Detection ────────────────────────────────────────

    def analyze_job_posting(self, description: str) -> dict:
        """Analyse a job posting for fraud indicators."""
        if self.is_demo_mode:
            # Simple heuristic for demo: flag obvious scam keywords
            scam_keywords = ["wire transfer", "send money", "pay upfront", "work from home easy money"]
            is_scam = any(kw in description.lower() for kw in scam_keywords)
            return get_demo_scam_analysis(is_legitimate=not is_scam)

        try:
            resp = requests.post(
                f"{self.base_url}/api/scam/analyze",
                json={"description": description},
                timeout=API_TIMEOUT,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.warning("Scam analysis failed, using demo data: %s", exc)
            return get_demo_scam_analysis()
