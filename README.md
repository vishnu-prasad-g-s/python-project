# ⚡ Energy Grid Analytics Dashboard

> A high-performance macro-grid visualization system for monitoring and analyzing hourly energy consumption across multiple regional power grids.

---

## 📌 Project Overview

The **Energy Grid Analytics Dashboard** transforms millions of rows of raw energy data into actionable grid intelligence. Built on **Streamlit** and **Plotly**, it delivers a premium dark-mode, glass-morphism UI that gives grid operators, analysts, and researchers a comprehensive **macro-to-micro** view of electricity demand — across regions, time-of-day, and multi-year timelines.

---

## 🎯 Core Objectives

| Goal | Description |
|---|---|
| 🦆 Duck Curve Detection | Identify how demand drops during solar-peak hours and spikes at dusk |
| 🌍 Regional Comparison | Compare consumption efficiency between geographic utility grids |
| 📈 Trend Tracking | Monitor load growth over years to inform infrastructure decisions |
| ⚙️ Variance Analysis | Detect which regions have volatile demand profiles |

---

## 🗂️ Project Structure

```
energy-grid-analytics/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
└── sample_data/            # Drop your CSV or Parquet data files here
    ├── NORTH_energy.csv
    ├── SOUTH_energy.parquet
    └── ...
```

---

## ⚙️ Technical Stack

| Layer | Technology |
|---|---|
| **Backend / Data** | Python 3.9+, Pandas, NumPy |
| **Frontend / UI** | Streamlit, Custom CSS3 (Glass-morphism) |
| **Visualization** | Plotly Express (interactive charts) |
| **Data Formats** | CSV, Apache Parquet |
| **Typography** | Google Fonts — Bebas Neue, DM Sans |

---

## 📂 Data File Requirements

The app auto-discovers data files in the **root directory** (`./`) and `./sample_data/`. Files must follow this convention:

### Naming Convention
```
REGIONNAME_anytext.csv
REGIONNAME_anytext.parquet
```
The **prefix before the first underscore** becomes the Region label (e.g., `north_2024.csv` → Region: `NORTH`).

### Required Columns
Each file must contain **at least two columns**:

| Column Type | Detected By | Example Names |
|---|---|---|
| **Datetime** | Contains `date` or `time` in name | `datetime`, `timestamp`, `date` |
| **Load (MW)** | Any numeric column that isn't datetime | `MW`, `load`, `demand`, `value` |

### Example CSV Format
```csv
datetime,MW
2018-01-01 00:00:00,14322.0
2018-01-01 01:00:00,13891.5
2018-01-01 02:00:00,13450.2
...
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/energy-grid-analytics.git
cd energy-grid-analytics
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your Data Files
Place your `.csv` or `.parquet` energy files in the root folder or `./sample_data/`. Follow the naming convention above.

### 5. Launch the Dashboard
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 📊 Dashboard Modules

### 🔢 KPI Intelligence Layer
Real-time metric cards displaying:
- **Regions Active** — Number of utility grids in the current filter
- **Avg Hourly Load** — Baseline energy demand in MW
- **Peak Demand** — All-time maximum load recorded
- **Data Points** — Total rows being analyzed

### 🕒 Tab 1 — Hourly Cycles (Duck Curve)
Line chart showing average MW consumption by hour of day, per region. Exposes the classical **Duck Curve** pattern driven by solar generation and evening demand spikes.

### 📈 Tab 2 — Macro Trends
Area chart tracking **Energy Load Growth Over Time** (year-over-year), helping determine whether regions are reducing consumption or require infrastructure expansion.

### 📊 Tab 3 — Regional Load Spread
- **Box Plot** — Visualizes load variance and outliers per region
- **Bar Chart** — Compares average load by day of week (weekday vs. weekend patterns)

---

## 🎛️ Sidebar Controls

| Control | Function |
|---|---|
| 🌍 Select Regions | Filter by one or more regional grids |
| 📅 Year Range Slider | Narrow the analysis window to specific years |

---

## 🧠 Why This Project Matters

Raw energy data is overwhelming in isolation. This dashboard acts as a **Visual Decision-Support System**, enabling stakeholders to:

- Schedule **load shedding** proactively during predicted peak windows
- Plan **renewable energy integration** aligned to the Duck Curve valleys
- Make evidence-based **infrastructure investment** decisions from trend data
- Benchmark **regional efficiency** improvements over time

---

## 🔮 Potential Enhancements

- [ ] Anomaly detection with statistical Z-score flagging
- [ ] Forecast overlay using Prophet or ARIMA models
- [ ] CSV/Excel export of filtered data
- [ ] Live SCADA or API data feed integration
- [ ] Map-based regional choropleth visualization

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">
  <b>⚡ ENERGY PERFORMANCE ANALYTICS</b> &nbsp;·&nbsp; Built with Streamlit + Plotly
</div>
