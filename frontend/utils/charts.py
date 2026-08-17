"""CareerPilot AI — Plotly chart builders for analytics dashboards."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go

from .constants import COLORS


def _base_layout(title: str = "", height: int = 320) -> dict:
    """Shared Plotly layout defaults matching the design system."""
    return dict(
        title=dict(text=title, font=dict(size=14, color="#64748B")),
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#64748B", size=12),
        showlegend=False,
    )


def create_industries_bar(industries: list[dict]) -> go.Figure:
    """Horizontal bar chart for top industries."""
    names = [i["name"] for i in industries]
    counts = [i["count"] for i in industries]

    fig = go.Figure(
        go.Bar(
            y=names[::-1],
            x=counts[::-1],
            orientation="h",
            marker=dict(
                color=counts[::-1],
                colorscale=[[0, COLORS["accent"]], [1, COLORS["primary"]]],
                line=dict(width=0),
            ),
            text=[f"{c} jobs" for c in counts[::-1]],
            textposition="auto",
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{y}</b><br>%{x} matching jobs<extra></extra>",
        )
    )
    fig.update_layout(**_base_layout("Top Industries"))
    fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.15)", zeroline=False)
    fig.update_yaxes(showgrid=False)
    return fig


def create_missing_skills_bar(skills: list[dict]) -> go.Figure:
    """Horizontal bar chart for in-demand missing skills."""
    names = [s["name"] for s in skills]
    demand = [s["demand"] for s in skills]

    fig = go.Figure(
        go.Bar(
            y=names[::-1],
            x=demand[::-1],
            orientation="h",
            marker=dict(
                color=demand[::-1],
                colorscale=[[0, "#FBBF24"], [1, COLORS["danger"]]],
                line=dict(width=0),
            ),
            text=[f"{d}%" for d in demand[::-1]],
            textposition="auto",
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{y}</b><br>Market demand: %{x}%<extra></extra>",
        )
    )
    fig.update_layout(**_base_layout("Top Missing Skills"))
    fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.15)", range=[0, 100], zeroline=False)
    fig.update_yaxes(showgrid=False)
    return fig


def create_salary_donut(distribution: list[dict]) -> go.Figure:
    """Donut chart for salary distribution."""
    labels = [d["range"] for d in distribution]
    values = [d["count"] for d in distribution]
    palette = [COLORS["primary"], COLORS["accent"], COLORS["success"], COLORS["warning"], COLORS["secondary"]]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=palette[: len(labels)], line=dict(color="white", width=2)),
            textinfo="label+percent",
            textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>%{value} roles (%{percent})<extra></extra>",
        )
    )
    layout = _base_layout("Salary Distribution", height=340)
    layout["showlegend"] = True
    layout["legend"] = dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=10))
    fig.update_layout(**layout)
    return fig


def create_scam_gauge(legitimate_pct: float, fraudulent_pct: float) -> go.Figure:
    """Dual gauge chart for scam detection results."""
    risk_color = (
        COLORS["success"] if legitimate_pct >= 70
        else COLORS["warning"] if legitimate_pct >= 40
        else COLORS["danger"]
    )

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=legitimate_pct,
        number=dict(suffix="%", font=dict(size=36, color=COLORS["success"])),
        title=dict(text="Legitimate", font=dict(size=14, color="#64748B")),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor="#94A3B8"),
            bar=dict(color=COLORS["success"], thickness=0.25),
            bgcolor="rgba(148,163,184,0.1)",
            borderwidth=0,
            steps=[
                dict(range=[0, 40], color="rgba(239,68,68,0.15)"),
                dict(range=[40, 70], color="rgba(245,158,11,0.15)"),
                dict(range=[70, 100], color="rgba(34,197,94,0.15)"),
            ],
            threshold=dict(line=dict(color=risk_color, width=3), thickness=0.8, value=legitimate_pct),
        ),
        domain=dict(x=[0, 0.48], y=[0, 1]),
    ))

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=fraudulent_pct,
        number=dict(suffix="%", font=dict(size=36, color=COLORS["danger"])),
        title=dict(text="Fraudulent", font=dict(size=14, color="#64748B")),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor="#94A3B8"),
            bar=dict(color=COLORS["danger"], thickness=0.25),
            bgcolor="rgba(148,163,184,0.1)",
            borderwidth=0,
            steps=[
                dict(range=[0, 30], color="rgba(34,197,94,0.15)"),
                dict(range=[30, 60], color="rgba(245,158,11,0.15)"),
                dict(range=[60, 100], color="rgba(239,68,68,0.15)"),
            ],
            threshold=dict(line=dict(color=COLORS["danger"], width=3), thickness=0.8, value=fraudulent_pct),
        ),
        domain=dict(x=[0.52, 1], y=[0, 1]),
    ))

    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def create_dashboard_sparkline(values: list[float], color: str = COLORS["primary"]) -> go.Figure:
    """Mini sparkline for metric cards."""
    fig = go.Figure(
        go.Scatter(
            y=values,
            mode="lines",
            line=dict(color=color, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor=f"rgba(37,99,235,0.08)",
        )
    )
    fig.update_layout(
        height=60,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig
