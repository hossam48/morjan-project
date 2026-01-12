import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import calendar

# --- 1. إعدادات الصفحة والستايل الفاتح ---
st.set_page_config(page_title="Elsewedy Projects Control", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .project-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-top: 5px solid #0056b3; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: 0.3s; text-align: center; height: 220px;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); border-top: 5px solid #ef4444; }
    [data-testid="stMetric"] { background-color: white; border-radius: 12px; border: 1px solid #eee; padding: 15px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f1f3f6; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0056b3; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والحالة ---
if 'current_project' not in st.session_state:
    st.session_state.current_project = None

# قائمة المشاريع (تأكدنا من قفل كل الأقواس هنا)
projects = {
    "Morjan Power Station": {"info": "Main EPC Project", "status": "Active", "progress": 65},
    "Project 1": {"info": "Standard Template", "status": "Planning", "progress": 10},
    "Project 2": {"info": "Standard Template", "status": "Proposed", "progress": 0},
    "Project 3": {"info": "Standard Template", "status": "Completed", "progress": 100}
}

# بيانات المهام الافتراضية لمرجان
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "DOC-01", "Item": "Mechanical Layout", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": date(2026, 2, 15), "Progress": 65},
        {"ID": "RFQ-01", "Item": "Fire Pump RFQ", "Owner": "Omar Fathy", "Status": "Technical Evaluation", "Due Date": date(2026, 1, 25), "Progress": 40},
        {"ID": "RFQ-02", "Item": "Package Unit RFQ", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": date(2026, 1, 30), "Progress": 10}
    ])

# --- 3. الواجهة الرئيسية (Projects Hub) ---
if st.session_state.current_project is None:
    st.title("🏗️ Elsewedy Electric - Engineering Hub")
    st.markdown("### Select a Project to Monitor Performance")
    
    cols = st.columns(len(projects))
    for i, (name, info) in enumerate(projects.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="project-card">
                    <h2 style='color:#003366'>{name}</h2>
                    <p style='color:gray'>{info['info']}</p>
                    <hr>
                    <p><b>Status: {info['status']}</b></p>
                    <p style='font-size: 24px; color:#0056b3; font-weight: bold;'>{info['progress']}%</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Manage Project", key=f"btn_{i}"):
                st.session_state.current_project = name
                st.rerun()

# --- 4. واجهة المشروع التفصيلية (داخل المشروع المختار) ---
else:
    st.sidebar.button("⬅️ Back to Project Hub", on_click=lambda: st.session_state.update({"current_project": None}))
    st.sidebar.title(f"📍 {st.session_state.current_project}")
    st.sidebar.info("Engineering EPC Control")

    st.title(f"🚀 {st.session_state.current_project} Control Center")
    
    tab1, tab2, tab3 = st.tabs(["📅 Monthly Calendar", "📊 Analytics Dashboard", "📋 MDL Documents"])

    # --- Tab 1: التق
