# 🛡️ Global Disaster Analytics Web Dashboard

An interactive, executive-grade disaster analytics dashboard built with **Python, Streamlit, Pandas, and Plotly**, analyzing global disaster impact, mortality, and trends from 2010 to 2026 based on the EM-DAT CRED / UCLouvain dataset.

---

## 📊 Dashboard Features
- **Key Performance Indicators (KPIs)**: Total Disasters, Total Fatalities, Total Affected Population, and Impacted Countries.
- **Disaster Group Donut Chart**: Natural vs Technological disaster ratio with central metric callout.
- **Year-Wise Trend Analysis**: Historical trajectory of events with dual-axis mortality tracking.
- **Disaster Subgroup Breakdown**: Ranked frequency across disaster classifications.
- **Top 10 Impacted Countries**: Interactive ranking by Disaster Count, Total Deaths, or Total Affected.
- **Disaster Type Deep-Dive**: Frequency breakdown of individual disaster types (Flood, Storm, Road, Earthquake, Epidemic, etc.).
- **Interactive Slicers**: Start Year range slider (2010–2026), Country multi-select with search, and Disaster Group filter.
- **Data Explorer & Export**: Pure HTML table with CSV export of filtered records.

---

## 🚀 Deployment Instructions (Streamlit Community Cloud)

1. Upload the files in this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **Create app** $\rightarrow$ select your repository.
4. Set **Main file path** to `app.py`.
5. Click **Deploy!**

---

## 💻 Running Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the application
streamlit run app.py
```
