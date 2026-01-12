import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import calendar

# --- 1. إعدادات الصفحة والستايل ---
st.set_page_config(page_title="Elsewedy Projects Control", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stMetric"] { background-color: white; border-radius: 12px; border: 1px solid #eee; padding: 15px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f1f3f6; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0056b3; color: white !important; }
    /* تحسين شكل القائمة الجانبية */
    section[data-testid="stSidebar"] { background-color: #f1f3f6; border-right: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والحالة ---
# قائمة المشاريع
project_list = ["Project Hub (Home)", "Morjan Power Station", "Project 1", "Project 2", "Project 3"]

# اختيار المشروع من القائمة الجانبية لضمان ثبات التابات
st.sidebar.title("🏢 Elsewedy Electric")
selected_project = st.sidebar.selectbox("📂 Select Project", project_list)

# بيانات المهام الافتراضية
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "DOC-01", "Item": "Mechanical Layout", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": date(2026, 2, 15), "Progress": 65},
        {"ID": "RFQ-01", "Item": "Fire Pump RFQ", "Owner": "Omar Fathy", "Status": "Technical Evaluation", "Due Date": date(2026, 1, 25), "Progress": 40},
        {"ID": "RFQ-02", "Item": "Package Unit RFQ", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": date(2026, 1, 30), "Progress": 10}
    ])

# --- 3. الواجهة الرئيسية (Project Hub) ---
if selected_project == "Project Hub (Home)":
    st.title("🏗️ Engineering Projects Hub")
    st.info("Welcome! Please select a project from the sidebar to view details.")
    
    # عرض كروت استعراضية فقط
    cols = st.columns(3)
    with cols[0]:
        st.metric("Total Active Projects", "4")
    with cols[1]:
        st.metric("Total Team Members", "3")
    with cols[2]:
        st.metric("Avg. Completion", "43%")
    
    st.markdown("---")
    st.image("https://upload.wikimedia.org/wikipedia/en/3/3b/Elsewedy_Electric_Logo.png", width=200)

# --- 4. واجهة المشروع التفصيلية (تفتح عند اختيار مشروع) ---
else:
    st.title(f"🚀 {selected_project} Control Center")
    
    # هنا التابات ستعمل بسلاسة لأن المشروع مختار من الـ Sidebar
    tab1, tab2, tab3 = st.tabs(["📅 Monthly Calendar", "📊 Analytics Dashboard", "📋 MDL Documents"])

    # --- Tab 1: التقويم ---
    with tab1:
        st.subheader("Monthly Outlook")
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            today = date.today()
            sel_month = st.selectbox("Month", list(calendar.month_name)[1:], index=today.month-1)
            month_idx = list(calendar.month_name).index(sel_month)
            cal = calendar.monthcalendar(2026, month_idx)
            cal_df = pd.DataFrame(cal, columns=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
            st.table(cal_df.replace(0, ""))
        with col_c2:
            picked_day = st.date_input("Filter by Date", today)
            filtered = st.session_state.tasks[st.session_state.tasks['Due Date'] == picked_day]
            if not filtered.empty:
                for _, row in filtered.iterrows():
                    st.success(f"**{row['Owner']}**: {row['Item']}")
            else:
                st.write("No tasks for this day.")

    # --- Tab 2: التحليلات ---
    with tab2:
        df = st.session_state.tasks.copy()
        df['Due Date'] = pd.to_datetime(df['Due Date'])
        m1, m2, m3 = st.columns(3)
        m1.metric("Items", len(df))
        m2.metric("Progress", f"{df['Progress'].mean():.1f}%")
        m3.metric("Status", "On Track")

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.pie(df, names='Status', title="Tasks by Status"), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x='Owner', y='Progress', color='Status', title="Team Loading"), use_container_width=True)

    # --- Tab 3: الـ MDL ---
    with tab3:
        st.subheader("Master Document List")
        st.dataframe(st.session_state.tasks, use_container_width=True)
        
        with st.expander("➕ Add Entry"):
            with st.form("new_entry"):
                it = st.text_input("Item")
                ow = st.selectbox("Owner", ["Hossam Atta", "Omar Fathy", "Mokhtar Mostafa"])
                du = st.date_input("Due")
                pr = st.slider("Progress %", 0, 100, 0)
