import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import calendar
import numpy as np

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Elsewedy Electric - EPC Control",
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
        --primary: #2563eb;
        --secondary: #7c3aed;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }

    .project-card {
        background: white;
        border-radius: 20px;
        padding: 0;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    .project-header { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); padding: 25px; color: white; }
    .project-body { padding: 25px; }
    .status-badge { display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 12px; color: white; }
    
    /* Calendar Styling */
    .calendar-container { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .calendar-table { width: 100%; border-collapse: separate; border-spacing: 5px; }
    .calendar-table th { background: #f8fafc; padding: 10px; border-radius: 8px; font-size: 12px; color: #64748b; }
    .calendar-table td { background: white; border: 1px solid #e2e8f0; height: 70px; vertical-align: top; padding: 8px; border-radius: 10px; }
    .today { background: #fef3c7 !important; border: 2px solid #fbbf24 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'current_project' not in st.session_state:
    st.session_state.current_project = None
if 'team_members' not in st.session_state:
    st.session_state.team_members = ["Hossam Atta", "Omar Fathy", "Mokhtar Mostafa", "Ahmed Hassan", "Sara Mohamed"]
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []

# Initialize Projects
if 'projects' not in st.session_state:
    st.session_state.projects = {
        "Morjan Power Station": {
            "info": "Main EPC Project - 400MW Combined Cycle",
            "status": "Active", "progress": 68, "budget": "$250M",
            "start": date(2025, 1, 1), "end": date(2027, 12, 31),
            "location": "Suez, Egypt", "client": "Egyptian Electricity Holding Company"
        },
        "Solar Farm Delta": {
            "info": "Renewable Energy - 200MW Solar PV",
            "status": "Planning", "progress": 28, "budget": "$180M",
            "start": date(2026, 3, 1), "end": date(2028, 6, 30),
            "location": "Benban, Aswan", "client": "New & Renewable Energy Authority"
        }
    }

# Initialize Tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "DOC-01", "Item": "Mechanical Layout Design", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": date(2026, 2, 15), "Progress": 68, "Priority": "High", "Category": "Engineering"},
        {"ID": "RFQ-01", "Item": "Fire Pump System RFQ", "Owner": "Omar Fathy", "Status": "Technical Evaluation", "Due Date": date(2026, 1, 25), "Progress": 45, "Priority": "Critical", "Category": "Procurement"}
    ])

# ==================== UTILITY FUNCTIONS ====================
def log_activity(action, details):
    st.session_state.activity_log.append({'timestamp': datetime.now(), 'action': action, 'details': details})

def get_status_color(status):
    colors = {"Active": "#10b981", "Planning": "#f59e0b", "Completed": "#8b5cf6", "Proposed": "#6366f1"}
    return colors.get(status, "#6b7280")

def get_priority_color(priority):
    colors = {"Critical": "#ef4444", "High": "#f59e0b", "Medium": "#3b82f6", "Low": "#10b981"}
    return colors.get(priority, "#6b7280")

# ==================== MAIN DASHBOARD ====================

if st.session_state.current_project is None:
    # --- HERO SECTION ---
    st.markdown("""
        <div style='text-align: center; padding: 50px 0;'>
            <h1 style='font-size: 4em; font-weight: 800; background: linear-gradient(135deg, #2563eb, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                Elsewedy Electric
            </h1>
            <p style='color: #64748b; font-size: 1.5em;'>Engineering Project Control Center</p>
        </div>
    """, unsafe_allow_html=True)

    # --- TOP METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Projects", len(st.session_state.projects))
    
    total_budget = 0
    for p in st.session_state.projects.values():
        try:
            clean_b = p['budget'].replace('$', '').replace('M', '').replace('SAR', '').strip()
            total_budget += int(clean_b)
        except: pass
    
    m2.metric("Total Budget", f"${total_budget}M")
    m3.metric("Active Tasks", len(st.session_state.tasks))
    m4.metric("Team Members", len(st.session_state.team_members))

    # --- PROJECTS GRID ---
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (name, info) in enumerate(st.session_state.projects.items()):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="project-card">
                    <div class="project-header">
                        <h2 style='margin:0;'>{name}</h2>
                        <small>{info['info']}</small>
                    </div>
                    <div class="project-body">
                        <div style='display:flex; justify-content:space-between; margin-bottom:15px;'>
                            <span class="status-badge" style="background:{get_status_color(info['status'])}">{info['status']}</span>
                            <span style="font-weight:bold; color:#1e293b;">{info['progress']}% Complete</span>
                        </div>
                        <p style='color:#64748b;'>📍 {info['location']} | 💰 {info['budget']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"🚀 Open Control Center: {name}", key=f"open_{i}", use_container_width=True):
                st.session_state.current_project = name
                log_activity("Project Access", name)
                st.rerun()

# ==================== PROJECT CONTROL CENTER ====================
else:
    proj = st.session_state.projects[st.session_state.current_project]
    
    with st.sidebar:
        if st.button("← Back to Hub", use_container_width=True):
            st.session_state.current_project = None
            st.rerun()
        st.markdown("---")
        st.title(st.session_state.current_project)
        st.write(proj['info'])
        st.metric("Project Progress", f"{proj['progress']}%")
        st.metric("Days Remaining", (proj['end'] - date.today()).days)

    st.markdown(f"<h1 style='color:#1e293b;'>🎯 {st.session_state.current_project}</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Calendar", "📊 Analytics", "📋 Tasks & Documents", "📜 Activity Log"])

    # --- TAB 1: CALENDAR ---
    with tab1:
        st.subheader("Project Schedule")
        today = date.today()
        cal = calendar.monthcalendar(2026, 1) # Example for Jan 2026
        
        cal_html = "<div class='calendar-container'><table class='calendar-table'><thead><tr>"
        for day_name in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]:
            cal_html += f"<th>{day_name}</th>"
        cal_html += "</tr></thead><tbody>"
        
        for week in cal:
            cal_html += "<tr>"
            for day in week:
                if day == 0:
                    cal_html += "<td></td>"
                else:
                    is_today = "today" if day == today.day and today.month == 1 else ""
                    cal_html += f"<td class='{is_today}'><span class='day-number'>{day}</span></td>"
            cal_html += "</tr>"
        cal_html += "</tbody></table></div>"
        st.markdown(cal_html, unsafe_allow_html=True)

    # --- TAB 2: ANALYTICS ---
    with tab2:
        df = st.session_state.tasks
        col_a, col_b = st.columns(2)
        with col_a:
            fig1 = px.pie(df, names='Status', title="Tasks by Status", hole=0.4)
            st.plotly_chart(fig1, use_container_width=True)
        with col_b:
            fig2 = px.bar(df, x='Owner', y='Progress', color='Priority', title="Team Progress")
            st.plotly_chart(fig2, use_container_width=True)

    # --- TAB 3: TASKS ---
    with tab3:
        st.subheader("Master Document List (MDL)")
        st.dataframe(st.session_state.tasks, use_container_width=True, hide_index=True)
        
        with st.expander("➕ Add New Deliverable"):
            with st.form("add_task"):
                c1, c2 = st.columns(2)
                t_id = c1.text_input("Document ID")
                t_name = c2.text_input("Document Title")
                t_owner = c1.selectbox("Owner", st.session_state.team_members)
                t_priority = c2.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                t_date = st.date_input("Due Date")
                if st.form_submit_button("Submit Document"):
                    new_task = {"ID": t_id, "Item": t_name, "Owner": t_owner, "Status": "Pending", "Due Date": t_date, "Progress": 0, "Priority": t_priority, "Category": "Engineering"}
                    st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_task])], ignore_index=True)
                    log_activity("Task Created", t_name)
                    st.success("Deliverable Added!")
                    st.rerun()

    # --- TAB 4: ACTIVITY LOG ---
    with tab4:
        st.subheader("Recent System Updates")
        for log in reversed(st.session_state.activity_log[-15:]):
            st.text(f"[{log['timestamp'].strftime('%H:%M:%S')}] {log['action']}: {log['details']}")

# Footer
st.markdown("<br><hr><center style='color:#94a3b8;'>Elsewedy Electric EPC Project Control v5.0 © 2026</center>", unsafe_allow_html=True)
