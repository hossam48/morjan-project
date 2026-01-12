import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import calendar

# --- 1. إعدادات الصفحة والستايل الفاتح الاحترافي ---
st.set_page_config(page_title="Elsewedy Projects Control", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .project-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-top: 5px solid #0056b3; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: 0.3s; text-align: center;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); border-top: 5px solid #ef4444; }
    [data-testid="stMetric"] { background-color: white; border-radius: 12px; border: 1px solid #eee; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f1f3f6; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0056b3; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والحالة ---
if 'current_project' not in st.session_state:
    st.session_state.current_project = None

# قائمة المشاريع
projects = {
    "Morjan Power Station": {"info": "Main EPC Project", "status": "Active", "progress": 65},
    "Project 1": {"info": "Standard Template", "status": "Planning", "progress": 10},
    "Project 2": {"info": "Standard Template", "status": "Proposed", "progress": 0
