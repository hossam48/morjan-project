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
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f1f3f6; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0056b3; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والحالة ---
if 'current_project' not in st.session_state:
    st.session_state.current_project = None

# قائمة المشاريع بعد التعديل
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
        {"ID": "RFQ-02", "Item": "Package Unit RFQ", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": date(2026, 1, 30), "Progress": 10},
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
                    <p style='font-size: 20px; color:#0056b3;'>{info['progress']}%</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open Dashboard", key=f"btn_{name}"):
                st.session_state.current_project = name
                st.rerun()

# --- 4. واجهة المشروع التفصيلية ---
else:
    st.sidebar.button("⬅️ Back to Project List", on_click=lambda: st.session_state.update({"current_project": None}))
    st.sidebar.title(f"📍 {st.session_state.current_project}")
    st.sidebar.info("Mechanical Dept. EPC Control")

    st.title(f"🚀 {st.session_state.current_project} Control Center")
    
    tab1, tab2, tab3 = st.tabs(["📅 Team Calendar", "📊 Analytics & KPI", "📋 MDL Documents"])

    # --- Tab 1: التقويم الشهري ---
    with tab1:
        st.subheader("Monthly Task Outlook")
        col_c1, col_c2 = st.columns([2, 1])
        
        with col_c1:
            today = date.today()
            sel_month = st.selectbox("Month", list(calendar.month_name)[1:], index=today.month-1)
            sel_year = 2026
            month_idx = list(calendar.month_name).index(sel_month)
            
            cal = calendar.monthcalendar(sel_year, month_idx)
            cal_df = pd.DataFrame(cal, columns=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
            st.table(cal_df.replace(0, ""))
        
        with col_c2:
            st.markdown("#### 🔍 Filter Tasks by Day")
            picked_day = st.date_input("Select date to check workload", today)
            filtered = st.session_state.tasks[st.session_state.tasks['Due Date'] == picked_day]
            if not filtered.empty:
                for _, row in filtered.iterrows():
                    st.success(f"**{row['Owner']}**: {row['Item']} ({row['Status']})")
            else:
                st.write("No deadlines for this date.")

    # --- Tab 2: التحليلات ---
    with tab2:
        df = st.session_state.tasks.copy()
        df['Due Date'] = pd.to_datetime(df['Due Date'])
        
        # كروت الأرقام
        m1, m2, m3 = st.columns(3)
        m1.metric("Active Deliverables", len(df))
        m2.metric("Overall Progress", f"{df['Progress'].mean():.1f}%")
        m3.metric("Critical Path Items", "1")

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.pie(df, names='Status', title="Task Status Breakdown", hole=0.3), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x='Owner', y='Progress', color='Status', barmode='group', title="Resource Utilization"), use_container_width=True)
        
        st.subheader("6-Month Project Roadmap")
        df['Start'] = pd.to_datetime(date.today())
        st.plotly_chart(px.timeline(df, x_start='Start', x_end='Due Date', y='Item', color='Owner', template="plotly_white"), use_container_width=True)

    # --- Tab 3: الـ MDL وإضافة المهام ---
    with tab3:
        st.subheader("Master Document List & RFQ Log")
        st.dataframe(st.session_state.tasks.style.background_gradient(subset=['Progress'], cmap='Blues'), use_container_width=True)
        
        with st.expander("➕ Update MDL / Add New RFQ"):
            with st.form("mdl_form"):
                cx, cy = st.columns(2)
                t_item = cx.text_input("Document/Package Name")
                t_owner = cy.selectbox("Owner", ["Hossam Atta", "Omar Fathy", "Mokhtar Mostafa"])
                t_due = st.date_input("Deadline Date")
                t_prog = st.slider("Progress %", 0, 100, 0)
                if st.form_submit_button("Sync to Master Schedule"):
                    new_entry = {"ID": "NEW", "Item": t_item, "Owner": t_owner, "Status": "In Progress", "Due Date": t_due, "Progress": t_prog}
                    st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_entry])], ignore_index=True)
                    st.rerun()

st.markdown("<br><hr><center>Elsewedy Electric - Engineering Management Suite v3.0</center>", unsafe_allow_html=True)
