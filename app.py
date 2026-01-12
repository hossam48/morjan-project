import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Morjan Hub | Elsewedy", layout="wide")

# --- 2. ستايل الألوان الهندسي الفاتح (Professional Light Style) ---
st.markdown("""
    <style>
    /* الخلفية العامة بيضاء مريحة للعين */
    .main { background-color: #f8f9fa; color: #212529; }
    
    /* تنسيق الكروت (التي تظهر في الصورة) */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 20px;
    }
    
    /* تعديل لون الأرقام داخل الكروت */
    [data-testid="stMetricValue"] { color: #0056b3 !important; font-weight: bold; }
    
    /* العناوين باللون الأزرق الرسمي */
    h1, h2, h3 { color: #003366 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* القائمة الجانبية */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #dee2e6; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. البيانات (نفس بياناتك) ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "DOC-01", "Category": "Engineering", "Item": "Mechanical Layout", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": datetime(2026, 2, 15), "Progress": 65},
        {"ID": "RFQ-01", "Category": "Procurement", "Item": "Fire Pump RFQ", "Owner": "Omar Fathy", "Status": "Technical Evaluation", "Due Date": datetime(2026, 1, 30), "Progress": 40},
        {"ID": "RFQ-02", "Category": "Procurement", "Item": "Package Unit RFQ", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": datetime(2026, 2, 10), "Progress": 10},
        {"ID": "DWG-03", "Category": "Engineering", "Item": "Piping Isometric", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": datetime(2026, 3, 20), "Progress": 30}
    ])

# --- 4. واجهة البرنامج ---
st.title("🏗️ Morjan Power Station Hub")
st.markdown("---")

df = st.session_state.tasks.copy()
df['Due Date'] = pd.to_datetime(df['Due Date'])

# الأرقام (Metrics) - ستظهر الآن بخلفية بيضاء وخط أزرق واضح
c1, c2, c3 = st.columns(3)
c1.metric("Total Tasks", len(df))
c2.metric("In Progress", len(df[df['Status'] == 'In Progress']))
c3.metric("Avg Progress", f"{df['Progress'].mean():.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# الرسوم البيانية بألوان فاتحة
col_left, col_right = st.columns(2)
with col_left:
    fig_pie = px.pie(df, names='Status', title="Tasks Distribution", color_discrete_sequence=px.colors.qualitative.Safe)
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    fig_bar = px.bar(df, x='Owner', y='Progress', color='Status', title="Team Workload", barmode='group')
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

# الجدول الزمني
st.subheader("📅 Project Timeline (Gantt)")
df['Start'] = datetime.now()
fig_gantt = px.timeline(df, x_start='Start', x_end='Due Date', y='Item', color='Owner', template="plotly_white")
fig_gantt.update_yaxes(autorange="reversed")
st.plotly_chart(fig_gantt, use_container_width=True)

# إضافة بيانات جديدة
with st.expander("➕ Add New Task / Document"):
    with st.form("add_task"):
        item = st.text_input("Item Name")
        owner = st.selectbox("Assign To", ["Hossam Atta", "Omar Fathy", "Mokhtar Mostafa"])
        due = st.date_input("Due Date")
        if st.form_submit_button("Sync to Schedule"):
            new_row = {"ID": "NEW", "Category": "Engineering", "Item": item, "Owner": owner, "Status": "Pending", "Due Date": pd.to_datetime(due), "Progress": 0}
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True)
            st.rerun()
