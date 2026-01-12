import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import calendar

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Elsewedy Projects Control",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED STYLING ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    :root {
        --primary: #2563eb; --secondary: #7c3aed; --success: #10b981;
        --warning: #f59e0b; --danger: #ef4444; --light: #f8fafc;
    }
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .project-card {
        background: white; border-radius: 20px; padding: 0; overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15); transition: all 0.4s;
    }
    .project-card:hover { transform: translateY(-10px); box-shadow: 0 20px 50px rgba(0,0,0,0.25); }
    .project-header { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); padding: 25px; color: white; }
    .project-body { padding: 25px; }
    [data-testid="stMetric"] { background: white; border-radius: 16px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    .stTabs [data-baseweb="tab"] { height: 60px; background: white; border-radius: 12px 12px 0 0; font-weight: 600; color: #64748b; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); color: white !important; }
    
    /* Calendar Styling */
    .calendar-table { width: 100%; border-collapse: separate; border-spacing: 8px; }
    .calendar-table th { background: #2563eb; color: white; padding: 12px; border-radius: 8px; font-size: 12px; }
    .calendar-table td { background: white; padding: 15px; text-align: center; border: 1px solid #e2e8f0; border-radius: 10px; height: 80px; vertical-align: top; position: relative; }
    .task-indicator { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin: 1px; }
    .task-count { position: absolute; top: 5px; right: 5px; background: #ef4444; color: white; border-radius: 10px; padding: 2px 6px; font-size: 10px; }
    .today { background: #fef3c7 !important; border: 2px solid #fbbf24 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'current_project' not in st.session_state:
    st.session_state.current_project = None
if 'team_members' not in st.session_state:
    st.session_state.team_members = ["Hossam Atta", "Omar Fathy", "Mokhtar Mostafa"]

if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "DOC-01", "Item": "Mechanical Layout", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": date(2026, 2, 15), "Progress": 65, "Priority": "High", "Category": "Engineering"},
        {"ID": "RFQ-01", "Item": "Fire Pump RFQ", "Owner": "Omar Fathy", "Status": "Technical Evaluation", "Due Date": date(2026, 1, 25), "Progress": 45, "Priority": "Critical", "Category": "Procurement"},
        {"ID": "RFQ-02", "Item": "Package Unit RFQ", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": date(2026, 1, 30), "Progress": 15, "Priority": "Medium", "Category": "Procurement"}
    ])

# ==================== UTILS ====================
def get_priority_color(p):
    return {"Critical": "#ef4444", "High": "#f59e0b", "Medium": "#3b82f6", "Low": "#10b981"}.get(p, "#6b7280")

# ==================== PROJECT HUB ====================
if st.session_state.current_project is None:
    st.markdown("<h1 style='text-align: center; color: #1e293b; font-size: 3em;'>Elsewedy Electric Hub</h1>", unsafe_allow_html=True)
    
    projects = {
        "Morjan Power Station": {"info": "Main EPC Project", "progress": 68, "status": "Active"},
        "Solar Farm Delta": {"info": "Project 1 Template", "progress": 25, "status": "Planning"},
        "Substation Upgrade": {"info": "Project 2 Template", "progress": 8, "status": "Proposed"}
    }
    
    cols = st.columns(3)
    for i, (name, info) in enumerate(projects.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="project-card">
                    <div class="project-header"><h3>{name}</h3></div>
                    <div class="project-body">
                        <p>{info['info']}</p>
                        <h2 style='color:#2563eb'>{info['progress']}%</h2>
                        <span style='background:#dcfce7; color:#16a34a; padding:5px 10px; border-radius:15px;'>{info['status']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Manage {name.split()[0]}", key=name):
                st.session_state.current_project = name
                st.rerun()

# ==================== PROJECT VIEW ====================
else:
    with st.sidebar:
        if st.button("⬅️ Back to Hub"):
            st.session_state.current_project = None
            st.rerun()
        st.title(st.session_state.current_project)
        st.metric("Overall Progress", f"{st.session_state.tasks['Progress'].mean():.1f}%")

    tab1, tab2, tab3 = st.tabs(["📅 Smart Calendar", "📊 Analytics", "📋 MDL Documents"])

    with tab1:
        col_cal, col_det = st.columns([2, 1])
        with col_cal:
            today = date.today()
            sel_month = st.selectbox("Month", list(calendar.month_name)[1:], index=today.month-1)
            m_idx = list(calendar.month_name).index(sel_month) + 1
            
            cal = calendar.monthcalendar(2026, m_idx)
            cal_html = "<table class='calendar-table'><thead><tr><th>MON</th><th>TUE</th><th>WED</th><th>THU</th><th>FRI</th><th>SAT</th><th>SUN</th></tr></thead><tbody>"
            
            df_c = st.session_state.tasks.copy()
            df_c['Due Date'] = pd.to_datetime(df_c['Due Date']).dt.date

            for week in cal:
                cal_html += "<tr>"
                for i, day in enumerate(week):
                    if day == 0: cal_html += "<td style='background:#f1f5f9'></td>"
                    else:
                        cur_d = date(2026, m_idx, day)
                        tasks_today = df_c[df_c['Due Date'] == cur_d]
                        style = "today" if cur_d == today else ""
                        cal_html += f"<td class='{style}'><span style='font-weight:bold'>{day}</span>"
                        if not tasks_today.empty:
                            cal_html += f"<span class='task-count'>{len(tasks_today)}</span>"
                            for _, t in tasks_today.iterrows():
                                cal_html += f"<div class='task-indicator' style='background:{get_priority_color(t['Priority'])}'></div>"
                        cal_html += "</td>"
                cal_html += "</tr>"
            st.markdown(cal_html + "</tbody></table>", unsafe_allow_html=True)

        with col_det:
            pick = st.date_input("Filter Day", today)
            filtered = st.session_state.tasks[st.session_state.tasks['Due Date'] == pick]
            if not filtered.empty:
                for _, row in filtered.iterrows():
                    st.info(f"**{row['Owner']}**: {row['Item']} ({row['Priority']})")
            else:
                st.write("No tasks found.")

    with tab2:
        df_an = st.session_state.tasks.copy()
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(px.pie(df_an, names='Status', hole=0.4, title="Status Breakdown"), use_container_width=True)
        with c2: st.plotly_chart(px.bar(df_an, x='Owner', y='Progress', color='Priority', title="Team Performance"), use_container_width=True)
        
        st.subheader("Project Gantt Chart")
        df_an['Start'] = pd.to_datetime(date.today())
        st.plotly_chart(px.timeline(df_an, x_start='Start', x_end='Due Date', y='Item', color='Owner'), use_container_width=True)

    with tab3:
        st.subheader("Master Document List (MDL)")
        st.dataframe(st.session_state.tasks, use_container_width=True)
        with st.expander("➕ Add New Entry"):
            with st.form("new_task"):
                f1, f2, f3 = st.columns(3)
                t_id = f1.text_input("ID")
                t_item = f2.text_input("Item")
                t_owner = f3.selectbox("Owner", st.session_state.team_members)
                t_due = st.date_input("Deadline")
                t_pri = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                if st.form_submit_button("Submit"):
                    new_t = {"ID": t_id, "Item": t_item, "Owner": t_owner, "Status": "Pending", "Due Date": t_due, "Progress": 0, "Priority": t_pri}
                    st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_t])], ignore_index=True)
                    st.rerun()

st.markdown(f"<div style='text-align:center; color:grey; padding:30px;'>Elsewedy Electric EPC Hub v4.5 © {datetime.now().year}</div>", unsafe_allow_html=True)
