import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Morjan Station | EPC Control", layout="wide")

# --- 2. ستايل الألوان (Elsewedy Dark Theme) ---
st.markdown("""
    <style>
    .main { background-color: #1e1e2e; color: white; }
    .stMetric { background-color: #252538; padding: 15px; border-radius: 10px; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. تجهيز البيانات الأساسية ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "DOC-01", "Category": "Engineering", "Item": "Mechanical Layout", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": datetime(2026, 2, 15), "Progress": 65},
        {"ID": "RFQ-01", "Category": "Procurement", "Item": "Fire Pump RFQ", "Owner": "Omar Fathy", "Status": "Technical Evaluation", "Due Date": datetime(2026, 1, 30), "Progress": 40},
        {"ID": "RFQ-02", "Category": "Procurement", "Item": "Package Unit RFQ", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": datetime(2026, 2, 10), "Progress": 10}
    ])

# --- 4. القائمة الجانبية ---
st.sidebar.title("🏢 Elsewedy Electric")
view_mode = st.sidebar.radio("Navigate", ["Dashboard", "MDL Tracking", "Procurement", "Team"])

# --- 5. الصفحة الرئيسية (Dashboard) ---
st.title("🏗️ Morjan Power Station Hub")
df = st.session_state.tasks.copy()
df['Due Date'] = pd.to_datetime(df['Due Date'])

if view_mode == "Dashboard":
    # أرقام سريعة
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tasks", len(df))
    c2.metric("In Progress", len(df[df['Status'] == 'In Progress']))
    c3.metric("Avg Progress", f"{df['Progress'].mean():.1f}%")

    st.markdown("---")
    
    # الرسم البياني للتوزيع
    col_left, col_right = st.columns(2)
    with col_left:
        fig_pie = px.pie(df, names='Status', title="Status Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_right:
        fig_bar = px.bar(df, x='Owner', y='Progress', color='Status', title="Team Workload")
        st.plotly_chart(fig_bar, use_container_width=True)

    # جدول زمني (Gantt) - نسخة مبسطة جداً لتجنب الإيرور
    st.subheader("📅 Project Timeline")
    df_gantt = df.copy()
    df_gantt['Start'] = datetime.now() # يبدأ من النهاردة
    fig_gantt = px.timeline(df_gantt, x_start='Start', x_end='Due Date', y='Item', color='Owner')
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)

elif view_mode == "MDL Tracking":
    st.subheader("📑 Master Document List")
    st.write(df[df['Category'] == 'Engineering'])

elif view_mode == "Procurement":
    st.subheader("📦 RFQ Tracking")
    proc_df = df[df['Category'] == 'Procurement']
    for _, row in proc_df.iterrows():
        st.write(f"**{row['Item']}** - Progress: {row['Progress']}%")
        st.progress(int(row['Progress']))

elif view_mode == "Team":
    st.subheader("🎯 Team Performance")
    st.bar_chart(df.set_index('Owner')['Progress'])

# --- 6. إضافة مهمة جديدة (بسيطة جداً) ---
with st.expander("➕ Add New Task"):
    with st.form("add_form"):
        new_item = st.text_input("Item Name")
        new_owner = st.selectbox("Owner", ["Hossam Atta", "Omar Fathy", "Mokhtar Mostafa"])
        new_date = st.date_input("Due Date")
        if st.form_submit_button("Add"):
            new_row = {"ID": "NEW", "Category": "Engineering", "Item": new_item, "Owner": new_owner, "Status": "Pending", "Due Date": pd.to_datetime(new_date), "Progress": 0}
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True)
            st.rerun()
