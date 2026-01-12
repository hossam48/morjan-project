import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import calendar

# --- 1. إعدادات الصفحة والستايل المحسّن ---
st.set_page_config(
    page_title="Elsewedy Projects Control",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ستايل محسّن مع تدرجات لونية احترافية وتنسيقات للتقويم والمهام
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif; }
    
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    .project-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.4s; text-align: center; height: 240px; color: white;
    }
    .project-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }
    
    [data-testid="stMetric"] { background: white; border-radius: 15px; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px; background: white; border-radius: 12px 12px 0 0;
        padding: 12px 25px; font-weight: 600; border: 2px solid #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }

    /* Calendar Styling */
    .calendar-container { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .calendar-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    .calendar-table th { background: #667eea; color: white; padding: 10px; }
    .calendar-table td { padding: 15px; text-align: center; border: 1px solid #eee; transition: 0.3s; position: relative; height: 60px; vertical-align: top; }
    .calendar-table td:hover { background: #f0f0ff; }
    .task-indicator { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin: 1px; }
    .task-count { position: absolute; top: 5px; right: 5px; background: #ef4444; color: white; border-radius: 10px; padding: 2px 6px; font-size: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. تهيئة البيانات في Session State ---
def initialize_session_state():
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    
    if 'team_members' not in st.session_state:
        st.session_state.team_members = ["Hossam Atta", "Omar Fathy", "Mokhtar Mostafa", "Ahmed Hassan", "Sara Mohamed"]
    
    if 'projects' not in st.session_state:
        st.session_state.projects = {
            "Morjan Power Station": {"info": "Main EPC Project", "status": "Active", "progress": 68, "budget": "250M USD", "start_date": date(2025, 1, 1), "end_date": date(2027, 12, 31)},
            "Solar Farm Delta": {"info": "Renewable Energy", "status": "Planning", "progress": 28, "budget": "180M USD", "start_date": date(2026, 3, 1), "end_date": date(2028, 6, 30)},
            "Substation Upgrade": {"info": "Infrastructure", "status": "Proposed", "progress": 8, "budget": "95M USD", "start_date": date(2026, 6, 1), "end_date": date(2027, 12, 31)},
            "Industrial Complex": {"info": "Manufacturing", "status": "Completed", "progress": 100, "budget": "320M USD", "start_date": date(2023, 1, 1), "end_date": date(2025, 12, 31)}
        }
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = pd.DataFrame([
            {"ID": "DOC-01", "Item": "Mechanical Layout Design", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": date(2026, 2, 15), "Progress": 65, "Priority": "High"},
            {"ID": "RFQ-01", "Item": "Fire Pump System RFQ", "Owner": "Omar Fathy", "Status": "Technical Evaluation", "Due Date": date(2026, 1, 25), "Progress": 45, "Priority": "Critical"},
            {"ID": "RFQ-02", "Item": "Package Unit RFQ", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": date(2026, 1, 30), "Progress": 10, "Priority": "Medium"}
        ])

initialize_session_state()

# --- 3. دوال مساعدة ---
def get_priority_color(priority):
    return {"Critical": "#ef4444", "High": "#f59e0b", "Medium": "#3b82f6", "Low": "#10b981"}.get(priority, "#6b7280")

# --- 4. الواجهة الرئيسية (Projects Hub) ---
if st.session_state.current_project is None:
    st.markdown("<h1 style='text-align: center; padding: 20px;'>🏗️ Elsewedy Electric Engineering Hub</h1>", unsafe_allow_html=True)
    
    cols = st.columns(len(st.session_state.projects))
    for i, (name, info) in enumerate(st.session_state.projects.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="project-card">
                    <h3>{name}</h3>
                    <p>{info['info']}</p>
                    <div style='font-size: 2.5em; font-weight: 800;'>{info['progress']}%</div>
                    <div style='margin-top:10px; font-weight:bold;'>{info['status']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("📊 Manage", key=f"btn_{i}", use_container_width=True):
                st.session_state.current_project = name
                st.rerun()

# --- 5. واجهة المشروع التفصيلية ---
else:
    proj_name = st.session_state.current_project
    proj_info = st.session_state.projects[proj_name]
    
    with st.sidebar:
        if st.button("⬅️ Back to Hub", use_container_width=True):
            st.session_state.current_project = None
            st.rerun()
        st.title(f"📍 {proj_name}")
        st.metric("Budget", proj_info['budget'])
        st.metric("Progress", f"{proj_info['progress']}%")
        days_left = (proj_info['end_date'] - date.today()).days
        st.metric("Days Remaining", days_left)
        
        st.markdown("---")
        with st.expander("👥 Team Management"):
            new_m = st.text_input("New Member Name")
            if st.button("Add Member"):
                if new_m and new_m not in st.session_state.team_members:
                    st.session_state.team_members.append(new_m)
                    st.rerun()

    st.markdown(f"<h1 style='color:#003366;'>🚀 {proj_name} Control Center</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Calendar", "📊 Analytics", "📋 MDL", "👥 Team"])

    with tab1:
        st.subheader("📅 Interactive Project Calendar")
        c1, c2 = st.columns([2, 1])
        with c1:
            months = list(calendar.month_name)[1:]
            sel_month = st.selectbox("Month", months, index=date.today().month-1)
            month_idx = months.index(sel_month) + 1
            cal = calendar.monthcalendar(2026, month_idx)
            
            cal_html = "<div class='calendar-container'><table class='calendar-table'><thead><tr><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr></thead><tbody>"
            for week in cal:
                cal_html += "<tr>"
                for day in week:
                    if day == 0: cal_html += "<td class='empty-day'></td>"
                    else:
                        cur_date = date(2026, month_idx, day)
                        tasks_on_day = st.session_state.tasks[st.session_state.tasks['Due Date'] == cur_date]
                        style = "today" if cur_date == date.today() else ""
                        cal_html += f"<td class='{style}'><div class='day-number'>{day}</div>"
                        if not tasks_on_day.empty:
                            cal_html += f"<span class='task-count'>{len(tasks_on_day)}</span>"
                            for _, t in tasks_on_day.iterrows():
                                cal_html += f"<span class='task-indicator' style='background:{get_priority_color(t['Priority'])}'></span>"
                        cal_html += "</td>"
                cal_html += "</tr>"
            st.markdown(cal_html + "</tbody></table></div>", unsafe_allow_html=True)
        
        with c2:
            st.markdown("#### 🔍 Filter Tasks")
            pick_d = st.date_input("Select Date", date.today())
            day_tasks = st.session_state.tasks[st.session_state.tasks['Due Date'] == pick_d]
            if not day_tasks.empty:
                for _, row in day_tasks.iterrows():
                    st.success(f"**{row['Owner']}**: {row['Item']} ({row['Progress']}%)")
            else: st.info("No tasks for this day.")

    with tab2:
        st.subheader("📊 Analytics Dashboard")
        df = st.session_state.tasks.copy()
        df['Due Date'] = pd.to_datetime(df['Due Date'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(px.pie(df, names='Status', hole=0.4, title="Status Distribution"), use_container_width=True)
        with col2:
            st.plotly_chart(px.bar(df, x='Owner', y='Progress', color='Priority', barmode='group', title="Resource Utilization"), use_container_width=True)
        
        st.markdown("---")
        st.subheader("🗓️ Project Roadmap (Gantt Chart)")
        df['Start'] = pd.to_datetime(date.today())
        fig_gantt = px.timeline(df, x_start='Start', x_end='Due Date', y='Item', color='Owner', title="Timeline View")
        fig_gantt.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_gantt, use_container_width=True)

    with tab3:
        st.subheader("📋 Master Document List (MDL)")
        st.dataframe(st.session_state.tasks, use_container_width=True)
        with st.expander("➕ Add New Document / RFQ"):
            with st.form("new_task"):
                f1, f2 = st.columns(2)
                t_item = f1.text_input("Item Name")
                t_owner = f2.selectbox("Assign To", st.session_state.team_members)
                t_due = st.date_input("Due Date")
                t_pri = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                if st.form_submit_button("Add to System"):
                    new_r = {"ID": f"NEW-{len(st.session_state.tasks)+1}", "Item": t_item, "Owner": t_owner, "Status": "Pending", "Due Date": t_due, "Progress": 0, "Priority": t_pri}
                    st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_r])], ignore_index=True)
                    st.rerun()

    with tab4:
        st.subheader("👥 Team Workload Analysis")
        for member in st.session_state.team_members:
            m_tasks = st.session_state.tasks[st.session_state.tasks['Owner'] == member]
            avg_p = m_tasks['Progress'].mean() if not m_tasks.empty else 0
            st.markdown(f"**{member}** - {len(m_tasks)} Task(s) | Avg Progress: {avg_p:.1f}%")
            st.progress(float(avg_p/100))

st.markdown("<br><hr><center>Elsewedy Electric Engineering Control Suite v4.6 © 2026</center>", unsafe_allow_html=True)
