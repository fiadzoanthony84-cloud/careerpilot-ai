"""CareerPilot AI — Streamlit frontend entry point."""

from __future__ import annotations

import streamlit as st

from utils.api_client import CareerPilotAPI
from utils.constants import NAV_ITEMS, PAGE_TITLES
from utils.charts import (
    create_industries_bar,
    create_missing_skills_bar,
    create_salary_donut,
    create_scam_gauge,
)
from utils.helpers import (
    build_document_viewer,
    build_empty_state,
    build_hero_section,
    build_job_card,
    build_metric_card,
    build_profile_card,
    build_scam_result,
    build_skill_badges,
    build_timeline_items,
    load_css,
)


st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🧭",
    layout="wide",
)

st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)


api = CareerPilotAPI()


# ── Session State ─────────────────────────────────────────────

if "page" not in st.session_state:
    st.session_state.page = "home"

if "cv_data" not in st.session_state:
    st.session_state.cv_data = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "selected_job" not in st.session_state:
    st.session_state.selected_job = None


# ── Sidebar ──────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🧭 CareerPilot AI")

    for item in NAV_ITEMS:
        if st.button(
            f"{item['icon']}  {item['label']}",
            key=f"nav_{item['id']}",
            use_container_width=True,
        ):
            st.session_state.page = item["id"]
            st.rerun()

    st.divider()

    if api.is_demo_mode:
        st.warning("⚠️ Backend offline — showing demo data")
    else:
        st.success("✅ Connected to backend")


page = st.session_state.page

st.title(PAGE_TITLES.get(page, "CareerPilot AI"))


# ── Home ─────────────────────────────────────────────────────

if page == "home":

    st.markdown(
        build_hero_section(),
        unsafe_allow_html=True,
    )

    cols = st.columns(4)

    cv = st.session_state.cv_data

    with cols[0]:
        skills_count = len(cv.get("skills", [])) if cv else 0

        st.markdown(
            build_metric_card(
                "📄",
                str(skills_count),
                "Skills Detected",
                "blue",
            ),
            unsafe_allow_html=True,
        )

    with cols[1]:
        jobs_count = len(
            st.session_state.recommendations or []
        )

        st.markdown(
            build_metric_card(
                "💼",
                str(jobs_count),
                "Job Matches",
                "cyan",
            ),
            unsafe_allow_html=True,
        )

    with cols[2]:
        education_count = (
            len(cv.get("education", []))
            if cv
            else 0
        )

        st.markdown(
            build_metric_card(
                "🎓",
                str(education_count),
                "Qualifications",
                "green",
            ),
            unsafe_allow_html=True,
        )

    with cols[3]:
        st.markdown(
            build_metric_card(
                "🛡️",
                "Ready",
                "Scam Detector",
                "amber",
            ),
            unsafe_allow_html=True,
        )

    if not cv:
        st.markdown(
            build_empty_state(
                "📄",
                "No CV uploaded yet",
                "Head to CV Analysis to upload your CV and unlock personalised job matches.",
            ),
            unsafe_allow_html=True,
        )


# ── CV Analysis ──────────────────────────────────────────────

elif page == "cv_analysis":

    uploaded = st.file_uploader(
        "Upload your CV (PDF)",
        type=["pdf"],
    )

    if uploaded is not None:

        if st.button(
            "Analyze CV",
            type="primary",
            key="analyze_cv_button",
        ):

            with st.spinner("Analyzing your CV..."):

                st.session_state.cv_data = (
                    api.upload_and_analyze_cv(
                        uploaded.read(),
                        uploaded.name,
                    )
                )

                st.session_state.recommendations = None

            st.rerun()

    cv = st.session_state.cv_data

    if cv:

        st.markdown(
            build_profile_card(cv),
            unsafe_allow_html=True,
        )

        # ── Skills ──

        st.subheader("Skills")

        st.markdown(
            build_skill_badges(
                cv.get("skills", [])
            ),
            unsafe_allow_html=True,
        )

        # ── Education ──

        st.subheader("Education")

        education = cv.get("education", [])

        st.markdown(
            build_timeline_items(
                education,
                "degree",
                "institution",
            ),
            unsafe_allow_html=True,
        )

        # ── Experience ──

        st.subheader("Experience")

        experience = cv.get("experience", [])

        st.markdown(
            build_timeline_items(
                experience,
                "title",
                "company",
            ),
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            build_empty_state(
                "📄",
                "Upload a CV to get started",
                "PDF format only.",
            ),
            unsafe_allow_html=True,
        )


# ── Job Recommendations ──────────────────────────────────────

elif page == "job_recommendations":

    if not st.session_state.cv_data:

        st.markdown(
            build_empty_state(
                "💼",
                "No CV on file",
                "Analyze your CV first to get personalised job matches.",
            ),
            unsafe_allow_html=True,
        )

    else:

        if st.session_state.recommendations is None:

            with st.spinner(
                "Finding your best-matching jobs..."
            ):

                st.session_state.recommendations = (
                    api.get_recommendations(
                        st.session_state.cv_data
                    )
                )

        jobs = st.session_state.recommendations or []

        if not jobs:

            st.markdown(
                build_empty_state(
                    "💼",
                    "No job matches found",
                    "Try analyzing your CV again or adding more skills.",
                ),
                unsafe_allow_html=True,
            )

        else:

            # enumerate() gives every button a unique number.
            # This fixes the cl_None duplicate-key error.
            for idx, job in enumerate(jobs):

                st.markdown(
                    build_job_card(job),
                    unsafe_allow_html=True,
                )

                job_title = job.get(
                    "title",
                    "Job",
                )

                if st.button(
                    f"Generate cover letter for {job_title}",
                    key=f"cl_{idx}",
                ):

                    st.session_state.selected_job = job
                    st.session_state.page = "cover_letter"

                    st.rerun()


# ── Career Insights ───────────────────────────────────────────

elif page == "career_insights":

    if not st.session_state.cv_data:

        st.markdown(
            build_empty_state(
                "📊",
                "No CV on file",
                "Analyze your CV first to see career insights.",
            ),
            unsafe_allow_html=True,
        )

    else:

        with st.spinner("Loading insights..."):

            insights = api.get_insights(
                st.session_state.cv_data
            )

        # Make sure insights is a dictionary.
        if not isinstance(insights, dict):
            st.error(
                "The backend returned an unexpected insights format."
            )
            st.stop()

        col1, col2 = st.columns(2)

        # ── Industries ──

        with col1:

            top_industries = insights.get(
                "top_industries",
                [],
            )

            st.plotly_chart(
                create_industries_bar(
                    top_industries
                ),
                use_container_width=True,
            )

        # ── Missing Skills ──

        with col2:

            missing_skills = insights.get(
                "missing_skills",
                [],
            )

            st.plotly_chart(
                create_missing_skills_bar(
                    missing_skills
                ),
                use_container_width=True,
            )

        # ── Salary ──

        salary = insights.get(
            "salary",
            {},
        )

        if isinstance(salary, dict):

            distribution = salary.get(
                "distribution"
            )

            if distribution:

                st.plotly_chart(
                    create_salary_donut(
                        distribution
                    ),
                    use_container_width=True,
                )


# ── Cover Letter ──────────────────────────────────────────────

elif page == "cover_letter":

    job = st.session_state.selected_job
    cv = st.session_state.cv_data

    if not job or not cv:

        st.markdown(
            build_empty_state(
                "✉️",
                "No job selected",
                "Pick a job from Job Matches to generate a tailored cover letter.",
            ),
            unsafe_allow_html=True,
        )

    else:

        job_title = job.get(
            "title",
            "Job",
        )

        with st.spinner(
            "Writing your cover letter..."
        ):

            letter = api.generate_cover_letter(
                job,
                cv,
            )

        st.markdown(
            build_document_viewer(
                f"Cover Letter — {job_title}",
                letter,
            ),
            unsafe_allow_html=True,
        )

        st.download_button(
            "Download as .txt",
            letter,
            file_name="cover_letter.txt",
            key="download_cover_letter",
        )


# ── Scam Detector ─────────────────────────────────────────────

elif page == "scam_detector":

    description = st.text_area(
        "Paste a job posting to check for scam indicators",
        height=200,
    )

    if st.button(
        "Analyze Posting",
        type="primary",
        key="analyze_scam_button",
    ) and description.strip():

        with st.spinner(
            "Checking for red flags..."
        ):

            result = api.analyze_job_posting(
                description
            )

        st.plotly_chart(
            create_scam_gauge(
                result["legitimate_pct"],
                result["fraudulent_pct"],
            ),
            use_container_width=True,
        )

        st.markdown(
            build_scam_result(result),
            unsafe_allow_html=True,
        )


# ── Report ────────────────────────────────────────────────────

elif page == "report":

    cv = st.session_state.cv_data

    if not cv:

        st.markdown(
            build_empty_state(
                "📋",
                "Nothing to report yet",
                "Analyze your CV to generate a full career report.",
            ),
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            build_profile_card(cv),
            unsafe_allow_html=True,
        )

        st.subheader("Top Job Matches")

        jobs = st.session_state.recommendations or []

        for idx, job in enumerate(jobs[:3]):

            st.markdown(
                build_job_card(job),
                unsafe_allow_html=True,
            )