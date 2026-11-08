"""
Global Disaster Analytics Dashboard
Interactive, modern web dashboard built with Streamlit, Pandas, and Plotly.
Matches and elevates the analytical capabilities of the Power BI project.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import load_data
from styles import CUSTOM_CSS, format_number, get_plotly_theme, render_html_table

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Global Disaster Analytics Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom modern dark theme styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Ingestion
# ---------------------------------------------------------
try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ---------------------------------------------------------
# Sidebar Controls & Interactive Filters
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 20px;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 8px;">
                <span>🌐</span> Filter Controls
            </div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Customize view & date parameters</div>
        </div>
    """, unsafe_allow_html=True)

    # 1. Year Range Filter
    all_years = sorted([int(y) for y in df_raw['Start Year'].unique() if y > 0])
    min_year, max_year = min(all_years), max(all_years)
    
    selected_year_range = st.slider(
        "📅 Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        help="Filter disaster events by start year"
    )

    # 2. Disaster Group Filter
    groups_list = ["All Groups"] + sorted(list(df_raw['Disaster Group'].unique()))
    selected_group = st.selectbox(
        "🏷️ Disaster Group",
        options=groups_list,
        index=0,
        help="Select Natural, Technological, or All disaster classifications"
    )

    # 3. Country Multi-Select Filter
    all_countries = sorted(list(df_raw['Country'].unique()))
    
    # Selection quick buttons
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("Clear All", use_container_width=True):
            st.session_state['selected_countries'] = []
    with col_c2:
        if st.button("All Countries", use_container_width=True):
            st.session_state['selected_countries'] = all_countries

    if 'selected_countries' not in st.session_state:
        st.session_state['selected_countries'] = []

    selected_countries = st.multiselect(
        "📍 Country Filter",
        options=all_countries,
        default=st.session_state.get('selected_countries', []),
        placeholder="All Countries (or choose specific...)",
        help="Filter by one or multiple nations"
    )

    # Sidebar Footer Information
    st.markdown("---")
    st.markdown("""
        <div style="font-size: 0.75rem; color: #64748b; line-height: 1.5;">
            <b style="color: #94a3b8;">Source Dataset:</b> EM-DAT CRED / UCLouvain<br>
            <b style="color: #94a3b8;">Coverage:</b> 2010 – 2026<br>
            <b style="color: #94a3b8;">Total Records:</b> 9,407 events
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Apply Filters to Dataset
# ---------------------------------------------------------
df_filtered = df_raw.copy()

# Filter by Year
df_filtered = df_filtered[
    (df_filtered['Start Year'] >= selected_year_range[0]) &
    (df_filtered['Start Year'] <= selected_year_range[1])
]

# Filter by Disaster Group
if selected_group != "All Groups":
    df_filtered = df_filtered[df_filtered['Disaster Group'] == selected_group]

# Filter by Country
if selected_countries:
    df_filtered = df_filtered[df_filtered['Country'].isin(selected_countries)]

# ---------------------------------------------------------
# Header Banner
# ---------------------------------------------------------
active_country_text = f"{len(selected_countries)} Selected" if selected_countries else "All Countries"
st.markdown(f"""
    <div class="dash-header">
        <h1 class="dash-title">
            <span>🛡️</span> GLOBAL DISASTER ANALYTICS DASHBOARD
        </h1>
        <div class="dash-subtitle">
            <span>Interactive Risk, Mortality & Impact Intelligence</span>
            <span class="badge-tag">📅 {selected_year_range[0]} – {selected_year_range[1]}</span>
            <span class="badge-tag">🌐 {active_country_text}</span>
            <span class="badge-tag">🏷️ {selected_group}</span>
            <span class="badge-tag">📊 {len(df_filtered):,} Events</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Calculate Key Performance Indicators (KPIs)
# ---------------------------------------------------------
total_disasters = len(df_filtered)
total_deaths = int(df_filtered['Total Deaths'].sum())
total_affected = int(df_filtered['Total Affected'].sum())
total_countries_count = df_filtered['Country'].nunique()
total_injured = int(df_filtered['No. Injured'].sum()) if 'No. Injured' in df_filtered.columns else 0

# Baseline comparison against total dataset
pct_disasters = (total_disasters / len(df_raw)) * 100 if len(df_raw) > 0 else 0

# ---------------------------------------------------------
# KPI Cards Display Row
# ---------------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-accent-top" style="background: #00d2ff;"></div>
            <div class="kpi-label">
                <span>Total Disasters</span>
                <span>⚡</span>
            </div>
            <div class="kpi-value metric-cyan">{total_disasters:,}</div>
            <div class="kpi-subtext">{pct_disasters:.1f}% of global records</div>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-accent-top" style="background: #ff5252;"></div>
            <div class="kpi-label">
                <span>Total Deaths</span>
                <span>💀</span>
            </div>
            <div class="kpi-value metric-red">{format_number(total_deaths)}</div>
            <div class="kpi-subtext">{total_deaths:,} fatalities recorded</div>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-accent-top" style="background: #ffd166;"></div>
            <div class="kpi-label">
                <span>Total Affected</span>
                <span>👥</span>
            </div>
            <div class="kpi-value metric-amber">{format_number(total_affected)}</div>
            <div class="kpi-subtext">{total_affected:,} lives impacted</div>
        </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-accent-top" style="background: #00e676;"></div>
            <div class="kpi-label">
                <span>Countries Impacted</span>
                <span>🌐</span>
            </div>
            <div class="kpi-value metric-emerald">{total_countries_count}</div>
            <div class="kpi-subtext">Across {df_filtered['Region'].nunique() if 'Region' in df_filtered.columns else 0} continental regions</div>
        </div>
    """, unsafe_allow_html=True)

# Edge case: No data matches the filter
if total_disasters == 0:
    st.warning("⚠️ No disaster records found matching the selected filter criteria. Please broaden your filters in the sidebar.")
    st.stop()

# ---------------------------------------------------------
# Visualizations Row 1: Donut Chart & Year-wise Trends
# ---------------------------------------------------------
col_row1_left, col_row1_right = st.columns([1, 2])

with col_row1_left:
    st.markdown("""
        <div class="chart-card">
            <div class="chart-title"><span>🍩</span> Disaster Group Distribution</div>
            <div class="chart-subtitle">Proportion of Natural vs Technological disasters</div>
    """, unsafe_allow_html=True)

    group_counts = df_filtered['Disaster Group'].value_counts().reset_index()
    group_counts.columns = ['Disaster Group', 'Count']
    
    color_map = {
        'Natural': '#00d2ff',
        'Technological': '#ff7675',
        'Other': '#a29bfe'
    }

    fig_donut = px.pie(
        group_counts,
        names='Disaster Group',
        values='Count',
        hole=0.62,
        color='Disaster Group',
        color_discrete_map=color_map
    )
    
    fig_donut.update_traces(
        textposition='outside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#0c0f17', width=2)),
        pull=[0.03] * len(group_counts)
    )
    
    # Add central total annotation
    fig_donut.update_layout(
        **get_plotly_theme(),
        showlegend=False,
        height=320,
        annotations=[dict(
            text=f"<b style='font-size:18px; color:#fff;'>{total_disasters:,}</b><br><span style='font-size:11px; color:#94a3b8;'>EVENTS</span>",
            x=0.5, y=0.5, font_size=13, showarrow=False
        )]
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_row1_right:
    st.markdown("""
        <div class="chart-card">
            <div class="chart-title"><span>📈</span> Year-Wise Disaster & Impact Trends</div>
            <div class="chart-subtitle">Historical trajectory of events and annual mortality</div>
    """, unsafe_allow_html=True)

    # Aggregate by Year
    trend_df = df_filtered[df_filtered['Start Year'] > 0].groupby('Start Year').agg(
        Disasters=('DisNo.', 'count'),
        Deaths=('Total Deaths', 'sum'),
        Affected=('Total Affected', 'sum')
    ).reset_index()

    fig_trend = go.Figure()

    # Disasters trend line with area shading
    fig_trend.add_trace(go.Scatter(
        x=trend_df['Start Year'],
        y=trend_df['Disasters'],
        name='Total Disasters',
        mode='lines+markers',
        line=dict(color='#00d2ff', width=3, shape='spline'),
        marker=dict(size=7, color='#00d2ff', line=dict(color='#ffffff', width=1.5)),
        fill='tozeroy',
        fillcolor='rgba(0, 210, 255, 0.08)',
        yaxis='y'
    ))

    # Secondary axis for Total Deaths
    fig_trend.add_trace(go.Bar(
        x=trend_df['Start Year'],
        y=trend_df['Deaths'],
        name='Annual Deaths',
        marker=dict(color='rgba(255, 82, 82, 0.45)', line=dict(color='#ff5252', width=1)),
        yaxis='y2'
    ))

    # Update Dual-Axis layout
    trend_theme = get_plotly_theme()
    trend_theme['yaxis2'] = dict(
        title=dict(text="Total Deaths", font=dict(color='#ff5252', size=11)),
        overlaying='y',
        side='right',
        showgrid=False,
        tickfont=dict(color='#ff5252', size=10)
    )
    trend_theme['yaxis']['title'] = dict(text="Disaster Count", font=dict(color='#00d2ff', size=11))
    trend_theme['height'] = 320
    trend_theme['hovermode'] = "x unified"

    fig_trend.update_layout(**trend_theme)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Visualizations Row 2: Subgroups & Top 10 Countries
# ---------------------------------------------------------
col_row2_left, col_row2_right = st.columns(2)

with col_row2_left:
    st.markdown("""
        <div class="chart-card">
            <div class="chart-title"><span>📂</span> Disaster Subgroup Analysis</div>
            <div class="chart-subtitle">Event frequency ranked across disaster sub-categories</div>
    """, unsafe_allow_html=True)

    subgroup_counts = df_filtered['Disaster Subgroup'].value_counts().reset_index()
    subgroup_counts.columns = ['Subgroup', 'Count']
    subgroup_counts = subgroup_counts.sort_values(by='Count', ascending=True)

    fig_subgroup = px.bar(
        subgroup_counts,
        x='Count',
        y='Subgroup',
        orientation='h',
        color='Count',
        color_continuous_scale=[[0, '#1e3c72'], [0.5, '#2a5298'], [1, '#00d2ff']],
        text='Count'
    )
    
    fig_subgroup.update_traces(
        textposition='outside',
        texttemplate='%{text:,}',
        marker_line_width=0
    )
    
    subgroup_layout = get_plotly_theme()
    subgroup_layout['coloraxis_showscale'] = False
    subgroup_layout['xaxis']['title'] = "Number of Disasters"
    subgroup_layout['yaxis']['title'] = ""
    subgroup_layout['height'] = 360

    fig_subgroup.update_layout(**subgroup_layout)
    st.plotly_chart(fig_subgroup, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_row2_right:
    # Metric switcher for top countries
    metric_choice = st.radio(
        "Rank Countries By:",
        options=["Disaster Count", "Total Deaths", "Total Affected"],
        horizontal=True,
        key="country_metric_radio"
    )

    metric_col_map = {
        "Disaster Count": ("DisNo.", "count", "#00e676", "Total Disasters"),
        "Total Deaths": ("Total Deaths", "sum", "#ff5252", "Total Deaths"),
        "Total Affected": ("Total Affected", "sum", "#ffd166", "Total Affected People")
    }
    src_col, agg_fn, bar_color, label_name = metric_col_map[metric_choice]

    if agg_fn == "count":
        country_agg = df_filtered.groupby('Country')['DisNo.'].count().reset_index()
        country_agg.columns = ['Country', 'Value']
    else:
        country_agg = df_filtered.groupby('Country')[src_col].sum().reset_index()
        country_agg.columns = ['Country', 'Value']

    top10_countries = country_agg.nlargest(10, 'Value').sort_values(by='Value', ascending=True)

    st.markdown(f"""
        <div class="chart-card">
            <div class="chart-title"><span>🏆</span> Top 10 Countries ({label_name})</div>
            <div class="chart-subtitle">Most vulnerable and impacted nations</div>
    """, unsafe_allow_html=True)

    fig_top10 = px.bar(
        top10_countries,
        x='Value',
        y='Country',
        orientation='h',
        text='Value',
        color_discrete_sequence=[bar_color]
    )
    
    fig_top10.update_traces(
        textposition='outside',
        texttemplate='%{x:,.0f}',
        marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
    )

    top10_layout = get_plotly_theme()
    top10_layout['xaxis']['title'] = label_name
    top10_layout['yaxis']['title'] = ""
    top10_layout['height'] = 315

    fig_top10.update_layout(**top10_layout)
    st.plotly_chart(fig_top10, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Visualizations Row 3: Disaster Type Deep-Dive
# ---------------------------------------------------------
st.markdown("""
    <div class="chart-card">
        <div class="chart-title"><span>🌪️</span> Disaster Type Breakdown</div>
        <div class="chart-subtitle">Incident frequency across specific disaster types</div>
""", unsafe_allow_html=True)

type_counts = df_filtered['Disaster Type'].value_counts().nlargest(12).reset_index()
type_counts.columns = ['Disaster Type', 'Count']
type_counts = type_counts.sort_values(by='Count', ascending=False)

fig_type = px.bar(
    type_counts,
    x='Disaster Type',
    y='Count',
    color='Count',
    color_continuous_scale=[[0, '#2d3748'], [0.5, '#4a5568'], [1, '#00d2ff']],
    text='Count'
)

fig_type.update_traces(
    textposition='outside',
    texttemplate='%{text:,}',
    marker_line_width=0
)

type_layout = get_plotly_theme()
type_layout['coloraxis_showscale'] = False
type_layout['xaxis']['title'] = ""
type_layout['yaxis']['title'] = "Disaster Count"
type_layout['height'] = 330

fig_type.update_layout(**type_layout)
st.plotly_chart(fig_type, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Table & Records Explorer (Pure HTML without pyarrow)
# ---------------------------------------------------------
with st.expander("🔍 View & Export Filtered Records Table", expanded=False):
    st.markdown(f"**Total Filtered Records:** `{len(df_filtered):,}` events matching criteria.")
    
    display_cols = [
        'DisNo.', 'Start Year', 'Country', 'Region', 'Disaster Group',
        'Disaster Subgroup', 'Disaster Type', 'Total Deaths', 'Total Affected'
    ]
    available_display_cols = [c for c in display_cols if c in df_filtered.columns]
    
    table_subset = df_filtered[available_display_cols].sort_values(by='Start Year', ascending=False)
    
    col_t1, col_t2 = st.columns([3, 1])
    with col_t2:
        rows_limit = st.selectbox("Show rows:", options=[25, 50, 100, 200], index=1, key="rows_limit_select")
        
    # Render pure HTML table without pyarrow dependency
    table_html = render_html_table(table_subset, max_rows=rows_limit)
    st.markdown(table_html, unsafe_allow_html=True)
    if len(table_subset) > rows_limit:
        st.caption(f"Showing top {rows_limit} of {len(table_subset):,} filtered records. Download CSV below for full dataset.")

    # CSV Download Button
    csv_data = table_subset.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"disaster_analytics_filtered_{selected_year_range[0]}_{selected_year_range[1]}.csv",
        mime="text/csv",
        use_container_width=True
    )
