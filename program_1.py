import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Energy Grid Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS (Copied from Reference)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* dark gradient bg */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #141e30 50%, #0f0c29 100%);
    color: #e8e8e8;
}

/* metric cards */
.metric-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform .2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-label { font-size: 12px; letter-spacing: 2px; text-transform: uppercase; color: #9ca3c8; margin-bottom: 4px; }
.metric-value { font-family: 'Bebas Neue', sans-serif; font-size: 42px; color: #7ee8fa; line-height: 1; }
.metric-sub   { font-size: 12px; color: #6b7280; margin-top: 4px; }

/* section header */
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    letter-spacing: 3px;
    color: #7ee8fa;
    border-left: 4px solid #ee7752;
    padding-left: 14px;
    margin: 32px 0 16px 0;
}

/* sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b28 100%);
    border-right: 1px solid rgba(126,232,250,0.15);
}

/* hero banner */
.hero {
    background: linear-gradient(90deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 300% 300%;
    animation: gradientShift 6s ease infinite;
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 28px;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero h1 { font-family:'Bebas Neue',sans-serif; font-size:52px; color:#fff; margin:0; letter-spacing:4px; }
.hero p  { color:rgba(255,255,255,.82); font-size:16px; margin:6px 0 0; }

/* tabs */
button[data-baseweb="tab"] {
    font-family:'DM Sans',sans-serif !important;
    font-weight:600 !important;
    font-size:14px !important;
    letter-spacing:1px !important;
}

/* dataframe */
.stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA LOADING ENGINE
# ─────────────────────────────────────────────
@st.cache_data
def load_and_merge_data():
    search_paths = ['./', './sample_data']
    data_files = []
    
    for path in search_paths:
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.lower().endswith(('.csv', '.parquet', '.paruqet')):
                    data_files.append(os.path.join(path, f))
    
    all_chunks = []
    for file_path in list(set(data_files)):
        fname = os.path.basename(file_path)
        try:
            if fname.lower().endswith('.csv'):
                temp_df = pd.read_csv(file_path)
            else:
                temp_df = pd.read_parquet(file_path)
            
            temp_df.columns = [c.strip() for c in temp_df.columns]
            date_col = [c for c in temp_df.columns if any(x in c.lower() for x in ['date', 'time'])][0]
            val_col = [c for c in temp_df.columns if c != date_col and temp_df[c].dtype != 'object'][0]
            
            region = fname.split('_')[0].replace('.csv','').replace('.parquet','').upper()
            
            chunk = pd.DataFrame({
                'Datetime': pd.to_datetime(temp_df[date_col], errors='coerce'),
                'MW': temp_df[val_col],
                'Region': region
            })
            all_chunks.append(chunk.dropna())
        except:
            continue
            
    full_df = pd.concat(all_chunks, ignore_index=True)
    full_df['Hour'] = full_df['Datetime'].dt.hour
    full_df['Day'] = full_df['Datetime'].dt.day_name()
    full_df['Year'] = full_df['Datetime'].dt.year
    return full_df

with st.spinner("Initializing Grid Data Engine..."):
    df = load_and_merge_data()

if df.empty:
    st.error("No data files found! Please ensure your CSV/Parquet files are in the folder.")
    st.stop()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px;">
        <span style="font-family:'Bebas Neue',sans-serif; font-size:26px; color:#7ee8fa; letter-spacing:3px;">⚡ ENERGY ANALYTICS</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    all_regions = sorted(df['Region'].unique())
    selected_regions = st.multiselect("🌍 Select Regions", all_regions, default=all_regions[:4])
    
    years = sorted(df['Year'].unique())
    year_range = st.select_slider("📅 Select Year Range", options=years, value=(min(years), max(years)))
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px; color:#6b7280; line-height:1.7;">
    <b style="color:#9ca3c8;">DASHBOARD FEATURES</b><br>
    • Multi-Region Grid Comparison<br>
    • Hourly Cycle Intelligence<br>
    • Macro-Trend Forecasting<br>
    • Glass-morphism UI Design<br>
    </div>
    """, unsafe_allow_html=True)

# Filter Data
mask = (df['Region'].isin(selected_regions)) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
fdf = df[mask]

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>ENERGY CONSUMPTION ANALYTICS</h1>
  <p>Macro-Grid Visualization System — Powered by Interactive Data Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPI METRIC CARDS
# ─────────────────────────────────────────────
if not fdf.empty:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Regions Active</div><div class="metric-value">{len(selected_regions)}</div><div class="metric-sub">Power Grids</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Avg Hourly Load</div><div class="metric-value">{fdf["MW"].mean():.0f}</div><div class="metric-sub">Megawatts (MW)</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Peak Demand</div><div class="metric-value">{fdf["MW"].max():,.0f}</div><div class="metric-sub">All-Time Max (MW)</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Data Points</div><div class="metric-value">{len(fdf):,}</div><div class="metric-sub">Analyzed Rows</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHART TABS
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">GRID PERFORMANCE ANALYSIS</div>', unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🕒 Hourly Cycles", "📈 Macro Trends", "📊 Regional Load Spread"])

# Shared Layout configuration for transparent Plotly charts
transparent_layout = dict(
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)", 
    font_color="#e8e8e8",
    margin=dict(l=20, r=20, t=40, b=20)
)

with t1:
    hourly_avg = fdf.groupby(['Hour', 'Region'])['MW'].mean().reset_index()
    fig1 = px.line(
        hourly_avg, x='Hour', y='MW', color='Region', 
        template="plotly_dark",
        title="Average MW by Hour of Day (The Duck Curve)",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig1.update_traces(mode='lines+markers')
    fig1.update_layout(**transparent_layout, height=500)
    st.plotly_chart(fig1, use_container_width=True)

with t2:
    yearly_trend = fdf.groupby(['Year', 'Region'])['MW'].mean().reset_index()
    fig2 = px.area(
        yearly_trend, x='Year', y='MW', color='Region', 
        template="plotly_dark",
        title="Energy Load Growth Over Time",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(**transparent_layout, height=500)
    st.plotly_chart(fig2, use_container_width=True)

with t3:
    c1, c2 = st.columns(2)
    with c1:
        # Box Plot for variance
        fig3 = px.box(
            fdf, x='Region', y='MW', color='Region',
            template="plotly_dark", 
            title="Load Variance by Region",
            points=False
        )
        fig3.update_layout(**transparent_layout, height=450)
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        # Day of week analysis
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_avg = fdf.groupby(['Day', 'Region'])['MW'].mean().reset_index()
        fig4 = px.bar(
            day_avg, x='Day', y='MW', color='Region', barmode='group',
            category_orders={"Day": day_order},
            template="plotly_dark",
            title="Average Load by Day of Week",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig4.update_layout(**transparent_layout, height=450)
        st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────
#  RAW DATA EXPANDER
# ─────────────────────────────────────────────
with st.expander("📋 View Raw Energy Data Engine"):
    st.dataframe(fdf.head(1000).reset_index(drop=True), use_container_width=True, height=320)
    st.caption("Displaying top 1,000 rows to optimize browser performance.")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#4b5563; font-size:12px; padding: 12px 0 24px;">
    <span style="color:#7ee8fa; font-family:'Bebas Neue',sans-serif; letter-spacing:2px;">ENERGY PERFORMANCE ANALYTICS</span> 
    &nbsp;·&nbsp; Built with Streamlit + Plotly 
</div>
""", unsafe_allow_html=True)