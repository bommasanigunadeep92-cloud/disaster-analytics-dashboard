"""
Data Loader Module for Disaster Analysis Dashboard.
Loads and caches the cleaned disaster dataset from Disaster_Data_Analytics.main.xlsx.
Preserves the original Excel file completely intact.
"""

import os
from pathlib import Path
import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).parent / "Disaster_Data_Analytics.main.xlsx"
CACHE_DIR = Path(__file__).parent / ".cache"
CACHE_FILE = CACHE_DIR / "disasters_cleaned.pkl"


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes types and cleans the disaster DataFrame."""
    # Ensure numeric columns are properly typed
    numeric_cols = [
        'Total Deaths', 'No. Injured', 'No. Affected', 'No. Homeless',
        'Total Affected', 'Reconstruction Costs (\'000 US$)',
        'Insured Damage (\'000 US$)', 'Total Damage (\'000 US$)',
        'Start Year', 'Start Month', 'Start Day',
        'End Year', 'End Month', 'End Day', 'Latitude', 'Longitude'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill and standardize categorical fields
    if 'Country' in df.columns:
        df['Country'] = df['Country'].fillna('Unknown').astype(str).str.strip()
    if 'Disaster Group' in df.columns:
        df['Disaster Group'] = df['Disaster Group'].fillna('Other').astype(str).str.strip()
    if 'Disaster Subgroup' in df.columns:
        df['Disaster Subgroup'] = df['Disaster Subgroup'].fillna('Other').astype(str).str.strip()
    if 'Disaster Type' in df.columns:
        df['Disaster Type'] = df['Disaster Type'].fillna('Other').astype(str).str.strip()
    if 'Region' in df.columns:
        df['Region'] = df['Region'].fillna('Unknown').astype(str).str.strip()
    if 'Subregion' in df.columns:
        df['Subregion'] = df['Subregion'].fillna('Unknown').astype(str).str.strip()

    # Fill year with 0 if NaN for safety and convert to integer
    if 'Start Year' in df.columns:
        df['Start Year'] = df['Start Year'].fillna(0).astype(int)

    # Human-impact summary
    df['Total Deaths'] = df['Total Deaths'].fillna(0)
    df['Total Affected'] = df['Total Affected'].fillna(0)
    if 'No. Injured' in df.columns:
        df['No. Injured'] = df['No. Injured'].fillna(0)

    return df


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Loads dataset with 2-tier caching:
    1. Fast pickle cache for sub-second cold starts.
    2. Streamlit @st.cache_data for instant in-memory reactive filter updates.
    """
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset file not found at: {DATA_FILE}")

    # Use pickle cache if it exists and is newer than the source Excel file
    if CACHE_FILE.exists():
        try:
            excel_mtime = DATA_FILE.stat().st_mtime
            cache_mtime = CACHE_FILE.stat().st_mtime
            if cache_mtime >= excel_mtime:
                df = pd.read_pickle(CACHE_FILE)
                return df
        except Exception:
            pass  # Fall back to reading Excel

    # Read from original Excel workbook (sheet: Disasters)
    df = pd.read_excel(DATA_FILE, sheet_name='Disasters')
    df = clean_dataframe(df)

    # Save to local cache directory for faster future startups
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        df.to_pickle(CACHE_FILE)
    except Exception:
        pass  # If unable to write cache, continue with in-memory df

    return df
