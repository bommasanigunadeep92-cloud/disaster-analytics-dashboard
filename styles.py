"""
Custom Styling and Theming for the Disaster Analytics Dashboard.
Inspired by executive Dark UI palettes (SoftDark / Modern Slate).
"""

import math
import pandas as pd

CUSTOM_CSS = """
<style>
/* Import modern clean fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Main background styling */
.stApp {
    background: radial-gradient(circle at 15% 10%, #151a28 0%, #0c0f17 100%);
    color: #e2e8f0;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: rgba(15, 19, 29, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.07);
}

/* Top App Header Banner */
.dash-header {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}

.dash-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 50%, #ff5252 100%);
}

.dash-title {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.dash-subtitle {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-top: 6px;
    margin-bottom: 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.badge-tag {
    display: inline-block;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 20px;
    background: rgba(0, 210, 255, 0.12);
    color: #00d2ff;
    border: 1px solid rgba(0, 210, 255, 0.25);
}

/* KPI Card Styles */
.kpi-container {
    background: linear-gradient(145deg, rgba(26, 32, 46, 0.85) 0%, rgba(17, 24, 39, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 18px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(8px);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}

.kpi-container:hover {
    transform: translateY(-3px);
    border-color: rgba(255, 255, 255, 0.18);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
}

.kpi-accent-top {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
}

.kpi-label {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94a3b8;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    line-height: 1.1;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -1px;
}

.kpi-subtext {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 6px;
}

/* Chart Container Cards */
.chart-card {
    background: linear-gradient(145deg, rgba(22, 28, 42, 0.75) 0%, rgba(15, 21, 34, 0.85) 100%);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.chart-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.chart-subtitle {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-bottom: 12px;
}

/* Metric color themes */
.metric-cyan { color: #00d2ff; }
.metric-red { color: #ff5252; }
.metric-emerald { color: #00e676; }
.metric-amber { color: #ffd166; }
.metric-purple { color: #b388ff; }

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.6);
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.28);
}

/* Custom Records Table (Pure HTML without pyarrow) */
.table-scroll-container {
    max-height: 380px;
    overflow-y: auto;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    background: #0d121f;
    margin-bottom: 14px;
}

.custom-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.83rem;
    color: #cbd5e1;
    font-family: 'Inter', sans-serif;
}

.custom-table th {
    position: sticky;
    top: 0;
    background: #192237;
    color: #00d2ff;
    font-weight: 600;
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    letter-spacing: 0.3px;
    z-index: 2;
}

.custom-table td {
    padding: 8px 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.custom-table tr:nth-child(even) {
    background: rgba(255, 255, 255, 0.02);
}

.custom-table tr:hover {
    background: rgba(0, 210, 255, 0.07);
    color: #ffffff;
}

.numeric-cell {
    text-align: right !important;
    font-family: 'JetBrains Mono', monospace;
}
</style>
"""


def format_number(val) -> str:
    """Formats large numbers into clean human-readable strings (e.g. 2.61B, 957.7K)."""
    if val is None or pd.isna(val):
        return "0"
    try:
        val = float(val)
        if math.isnan(val) or math.isinf(val):
            return "0"
        if abs(val) >= 1_000_000_000:
            return f"{val / 1_000_000_000:.2f}B"
        elif abs(val) >= 1_000_000:
            return f"{val / 1_000_000:.2f}M"
        elif abs(val) >= 10_000:
            return f"{val / 1_000:.1f}K"
        elif abs(val) >= 1_000:
            return f"{val:,.0f}"
        else:
            return f"{val:.0f}"
    except (ValueError, TypeError):
        return "0"


def get_plotly_theme():
    """Returns a unified layout dictionary for dark-themed Plotly charts."""
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Inter, -apple-system, sans-serif',
            color='#94a3b8',
            size=12
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.06)',
            zeroline=False,
            showline=False,
            tickfont=dict(color='#94a3b8', size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.06)',
            zeroline=False,
            showline=False,
            tickfont=dict(color='#94a3b8', size=11)
        ),
        hoverlabel=dict(
            bgcolor='#1e293b',
            bordercolor='rgba(255, 255, 255, 0.1)',
            font=dict(color='#ffffff', family='Inter, sans-serif', size=12)
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1', size=11),
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )


def render_html_table(df_subset: pd.DataFrame, max_rows: int = 50) -> str:
    """
    Renders a fast, responsive, and beautifully styled HTML table.
    Bypasses pyarrow completely to avoid Windows Application Control policy blocks.
    """
    rows_to_render = df_subset.head(max_rows)
    
    html = ['<div class="table-scroll-container"><table class="custom-table"><thead><tr>']
    for col in rows_to_render.columns:
        is_num = col in ['Total Deaths', 'Total Affected', 'Start Year', 'No. Injured']
        cls = ' class="numeric-cell"' if is_num else ''
        html.append(f'<th{cls}>{col}</th>')
    html.append('</tr></thead><tbody>')
    
    for _, row in rows_to_render.iterrows():
        html.append('<tr>')
        for col in rows_to_render.columns:
            val = row[col]
            is_num = col in ['Total Deaths', 'Total Affected', 'Start Year', 'No. Injured']
            cls = ' class="numeric-cell"' if is_num else ''
            if col in ['Total Deaths', 'Total Affected'] and pd.notna(val) and val > 0:
                formatted_val = f"{int(val):,}"
            else:
                formatted_val = str(val) if pd.notna(val) else "-"
            html.append(f'<td{cls}>{formatted_val}</td>')
        html.append('</tr>')
        
    html.append('</tbody></table></div>')
    return "".join(html)
