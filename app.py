import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Morjan Power Station | EPC Control",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%); }
    [data-testid="stSidebar"] { background-color: #1a1a2e; }
    h1, h2, h3 { color: #4a9eff !important; }
    .stMetric { background-color: #252538; padding: 15px; border-radius: 10px; border: 1px solid #444; }
    .footer { position: fixed; bottom: 0; left: 0; right: 0; background-color: #1a1a2e; padding: 5px; text-align: center; color: #7d8da6; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIALIZE DATA ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "DOC-001", "Category": "Engineering", "Item": "Mechanical Layout - Turbine Hall", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": datetime(2026, 2, 15), "Progress": 65},
        {"ID": "RFQ-101", "Category": "Procurement", "Item": "Fire Pump Package RFQ", "Owner": "Hossam Atta", "Status": "Technical Evaluation", "Due Date": datetime(2026, 1, 30), "Progress": 40},
        {"ID": "RFQ-102", "Category": "Procurement", "Item": "Package Unit RFQ", "Owner": "Omar Fathy", "Status": "In Progress", "Due Date": datetime(2026, 2, 10), "Progress": 20},
        {"ID": "CALC-01", "Category": "Engineering", "Item": "Hydraulic Calculations", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": datetime(2026, 3, 5), "Progress": 0},
        {"ID": "DOC-002", "Category": "Engineering", "Item": "Piping Isometric Drawings", "Owner": "Omar Fathy", "Status": "In Progress", "Due Date": datetime(2026, 4, 20), "Progress": 30}
    ])

# --- 4. SIDEBAR ---
st.sidebar.title("🏢 Elsewedy Electric")
st.sidebar.subheader("Morjan Project Control")
view_mode = st.sidebar.radio("Navigate", ["Executive Dashboard", "MDL Tracking", "Procurement Tracker", "Team Performance"])

# Excel Upload
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("📤 Update via Excel", type=['xlsx'])
if uploaded_file:
    try:
        new_df = pd.read_excel(uploaded_file)
        new_df['Due Date'] = pd.to_datetime(new_df['Due Date'])
        st.session_state
