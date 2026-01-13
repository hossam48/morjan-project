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
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --secondary: #7c3aed;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #06b6d4;
        --dark: #1e293b;
        --light: #f8fafc;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main > div {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* ============= PROJECT CARDS ============= */
    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin: 30px 0;
    }
    
    .project-card {
        background: white;
        border-radius: 20px;
        padding: 0;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
    }
    
    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        transform: scaleX(0);
        transition: transform 0.4s;
    }
    
    .project-card:hover::before {
        transform: scaleX(1);
    }
    
    .project-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    }
    
    .project-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 25px;
        color: white;
    }
    
    .project-body {
        padding: 25px;
    }
    
    .progress-circle {
        width: 120px;
        height: 120px;
        margin: 20px auto;
        position: relative;
    }
    
    .status-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ============= METRICS ============= */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* ============= TABS ============= */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: white;
        border-radius: 12px 12px 0 0;
        padding: 15px 30px;
        font-weight: 600;
        font-size: 15px;
        border: 2px solid transparent;
        transition: all 0.3s;
        color: #64748b;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f8fafc;
        border-color: var(--primary);
        color: var(--primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white !important;
        border-color: var(--primary);
    }
    
    /* ============= CALENDAR ============= */
    .calendar-container {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .calendar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 20px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .calendar-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 8px;
    }
    
    .calendar-table th {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 15px;
        text-align: center;
        font-weight: 700;
        font-size: 13px;
        border-radius: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .calendar-table td {
        background: white;
        padding: 20px 10px;
        text-align: center;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s;
        position: relative;
        height: 80px;
        vertical-align: top;
    }
    
    .calendar-table td:hover {
        background: #f0f9ff;
        border-color: var(--primary);
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.2);
    }
    
    .day-number {
        font-weight: 700;
        font-size: 18px;
        color: #1e293b;
        display: block;
        margin-bottom: 8px;
    }
    
    .task-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin: 2px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .task-count {
        position: absolute;
        top: 8px;
        right: 8px;
        background: linear-gradient(135deg, var(--danger), #dc2626);
        color: white;
        border-radius: 12px;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
    }
    
    .empty-day {
        background: #f8fafc !important;
        border-color: #f1f5f9 !important;
        cursor: default;
    }
    
    .empty-day:hover {
        transform: none;
        box-shadow: none;
    }
    
    .today {
        background: #fef3c7 !important;
        border: 3px solid #fbbf24 !important;
        box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.2);
    }
    
    .weekend {
        background: #fef2f2 !important;
    }
    
    /* ============= TASK CARDS ============= */
    .task-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid var(--primary);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s;
    }
    
    .task-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .team-member-card {
        background: linear-gradient(135deg, #f8fafc 0%, white 100%);
        border-radius: 16px;
        padding: 25px;
        margin: 20px 0;
        border: 2px solid #e2e8f0;
        transition: all 0.3s;
    }
    
    .team-member-card:hover {
        border-color: var(--primary);
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.15);
    }
    
    /* ============= BUTTONS ============= */
    .stButton>button {
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        font-size: 15px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border: none;
        color: white;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4);
    }
    
    /* ============= DATAFRAME ============= */
    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* ============= SIDEBAR ============= */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* ============= ANIMATIONS ============= */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* ============= SCROLLBAR ============= */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary), var(--secondary));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
def init_state():
    """Initialize all session state variables"""
    defaults = {
        'current_project': None,
        'team_members': [
            "Hossam Atta", "Omar Fathy", "Mokhtar Mostafa",
            "Ahmed Hassan", "Sara Mohamed"
        ],
        'projects': {
            "Morjan Power Station": {
                "info": "Main EPC Project - 400MW Combined Cycle",
                "status": "Active",
                "progress": 68,
                "budget": "$250M",
                "start": date(2025, 1, 1),
                "end": date(2027, 12, 31),
                "location": "Suez, Egypt",
                "client": "Egyptian Electricity Holding Company"
            },
            "Solar Farm Delta": {
                "info": "Renewable Energy - 200MW Solar PV",
                "status": "Planning",
                "progress": 28,
                "budget": "$180M",
                "start": date(2026, 3, 1),
                "end": date(2028, 6, 30),
                "location": "Benban, Aswan",
                "client": "New & Renewable Energy Authority"
            },
            "Substation Upgrade": {
                "info": "Infrastructure - 500kV Substation",
                "status": "Proposed",
                "progress": 8,
                "budget": "$95M",
                "start": date(2026, 6, 1),
                "end": date(2027, 12, 31),
                "location": "Cairo North",
                "client": "Cairo Electricity Distribution"
            },
            "Industrial Complex Giza": {
                "info": "Manufacturing - 150MW Distribution",
                "status": "Completed",
                "progress": 100,
                "budget": "$320M",
                "start": date(2023, 1, 1),
                "end": date(2025, 12, 31),
                "location": "6th of October City",
                "client": "Industrial Development Authority"
            }
        },
        'tasks': pd.DataFrame([
            {"ID": "DOC-01", "Item": "Mechanical Layout Design", "Owner": "Hossam Atta", 
             "Status": "In Progress", "Due Date": date(2026, 2, 15), "Progress": 68, 
             "Priority": "High", "Category": "Engineering"},
            {"ID": "RFQ-01", "Item": "Fire Pump System RFQ", "Owner": "Omar Fathy",
             "Status": "Technical Evaluation", "Due Date": date(2026, 1, 25), "Progress": 45,
             "Priority": "Critical", "Category": "Procurement"},
            {"ID": "RFQ-02", "Item": "Package Unit RFQ", "Owner": "Mokhtar Mostafa",
             "Status": "Pending", "Due Date": date(2026, 1, 30), "Progress": 15,
             "Priority": "Medium", "Category": "Procurement"},
            {"ID": "DOC-02", "Item": "Electrical Single Line Diagram", "Owner": "Ahmed Hassan",
             "Status": "In Progress", "Due Date": date(2026, 2, 5), "Progress": 82,
             "Priority": "High", "Category": "Engineering"},
            {"ID": "RFQ-03", "Item": "Transformer Procurement", "Owner": "Sara Mohamed",
             "Status": "Submitted", "Due Date": date(2026, 1, 20), "Progress": 92,
             "Priority": "Critical", "Category": "Procurement"}
        ]),
        'activity_log': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ==================== UTILITY FUNCTIONS ====================
def get_status_color(status):
    colors = {
        "Active": "#10b981", "Planning": "#f59e0b",
        "Proposed": "#6366f1", "Completed": "#8b5cf6"
    }
    return colors.get(status, "#6b7280")

def get_priority_color(priority):
    colors = {
        "Critical": "#ef4444", "High": "#f59e0b",
        "Medium": "#3b82f6", "Low": "#10b981"
    }
    return colors.get(priority, "#6b7280")

def calculate_health(progress):
    if progress >= 90: return "Excellent", "🟢", "#10b981"
    elif progress >= 70: return "On Track", "🟡", "#f59e0b"
    elif progress >= 50: return "At Risk", "🟠", "#fb923c"
    else: return "Critical", "🔴", "#ef4444"

def log_activity(action, details):
    """Log user activities"""
    st.session_state.activity_log.append({
        'timestamp': datetime.now(),
        'action': action,
        'details': details
    })

def create_progress_circle(progress, size=120):
    """Create circular progress indicator"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = progress,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#2563eb"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 50], 'color': '#fecaca'},
                {'range': [50, 75], 'color': '#fef08a'},
                {'range': [75, 100], 'color': '#bbf7d0'}
            ],
        }
    ))
    fig.update_layout(
        height=size, width=size,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'size': 20, 'color': "#1e293b", 'family': "Inter"}
    )
    return fig

# ==================== PROJECT HUB ====================
if st.session_state.current_project is None:
    # Hero Section
    st.markdown("""
        <div style='text-align: center; padding: 60px 20px; animation: fadeIn 0.8s;'>
            <div style='font-size: 80px; margin-bottom: 20px;'>⚡</div>
            <h1 style='font-size: 4em; font-weight: 800; margin: 0;
                       background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                Elsewedy Electric
            </h1>
            <h2 style='color: #64748b; font-weight: 400; font-size: 2em; margin: 20px 0;'>
                Engineering Project Control Platform
            </h2>
            <p style='color: #94a3b8; font-size: 1.2em; max-width: 600px; margin: 20px auto;'>
                Enterprise-grade EPC project management system for monitoring deliverables, 
                tracking milestones, and optimizing resource allocation.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    total_projects = len(st.session_state.projects)
    active_projects = sum(1 for p in st.session_state.projects.values() if p['status'] == 'Active')
    total_budget = sum(int(p['budget'].replace('$','').replace('M','')) for p in st.session_state.projects.values())
    
    col1.metric("Total Projects", total_projects)
    col2.metric("Active Projects", active_projects)
    col3.metric("Total Budget", f"${total_budget}M")
    col4.metric("Team Members", len(st.session_state.team_members))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Project Cards Grid
    cols = st.columns(2)
    for i, (name, info) in enumerate(st.session_state.projects.items()):
        with cols[i % 2]:
            health, icon, color = calculate_health(info['progress'])
            
            st.markdown(f"""
                <div class="project-card animate-in" style='animation-delay: {i*0.1}s;'>
                    <div class="project-header">
                        <h2 style='margin: 0; font-size: 1.5em;'>{name}</h2>
                        <p style='margin: 10px 0 0 0; opacity: 0.9;'>{info['info']}</p>
                    </div>
                    <div class="project-body">
                        <div style='display: flex; justify-content: space-between; margin-bottom: 20px;'>
                            <span class='status-badge' style='background: {get_status_color(info['status'])}; color: white;'>
                                {info['status']}
                            </span>
                            <span style='font-weight: 700; color: {color};'>{icon} {health}</span>
                        </div>
                        <div style='text-align: center; margin: 25px 0;'>
                            <div style='font-size: 3em; font-weight: 800; 
                                        background: linear-gradient(135deg, #2563eb, #7c3aed);
                                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                                {info['progress']}%
                            </div>
                            <div style='font-size: 0.9em; color: #64748b; margin-top: 5px;'>
                                Project Completion
                            </div>
                        </div>
                        <div style='background: #f8fafc; padding: 15px; border-radius: 12px; margin-top: 20px;'>
                            <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                                <span style='color: #64748b;'>💰 Budget:</span>
                                <strong>{info['budget']}</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                                <span style='color: #64748b;'>📍 Location:</span>
                                <strong>{info.get('location', 'N/A')}</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                                <span style='color: #64748b;'>🏢 Client:</span>
                                <strong style='font-size: 0.85em;'>{info.get('client', 'N/A')}</strong>
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🚀 Enter Control Center", key=f"btn_{i}", use_container_width=True):
                st.session_state.current_project = name
                log_activity("Project Opened", name)
                st.rerun()

# ==================== PROJECT CONTROL CENTER ====================
else:
    proj = st.session_state.projects[st.session_state.current_project]
    
    # Advanced Sidebar
    with st.sidebar:
        if st.button("← Back to Hub", use_container_width=True):
            st.session_state.current_project = None
            st.rerun()
        
        st.markdown("<hr style='margin: 20px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Project Info
        st.markdown(f"""
            <div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.1); 
                        border-radius: 12px; margin-bottom: 20px;'>
                <h2 style='color: white; margin: 0; font-size: 1.3em;'>
                    {st.session_state.current_project}
                </h2>
                <p style='color: rgba(255,255,255,0.8); margin: 10px 0 0 0; font-size: 0.9em;'>
                    {proj['info']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Quick Stats
        st.metric("📊 Progress", f"{proj['progress']}%", delta=f"{proj['progress']-50}% vs target")
        st.metric("💰 Budget", proj['budget'])
        st.metric("📅 Days Left", (proj['end'] - date.today()).days)
        
        st.markdown("<hr style='margin: 20px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Team Management
        st.markdown("### 👥 Team Management")
        
        with st.expander("➕ Add Member"):
            new_member = st.text_input("Name", placeholder="Full Name")
            if st.button("Add", use_container_width=True):
                if new_member and new_member not in st.session_state.team_members:
                    st.session_state.team_members.append(new_member)
                    log_activity("Team Member Added", new_member)
                    st.success(f"✅ {new_member} added!")
                    st.rerun()
        
        with st.expander("📋 View Team"):
            for member in st.session_state.team_members:
                tasks = len(st.session_state.tasks[st.session_state.tasks['Owner'] == member])
                st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.1); padding: 12px; 
                                border-radius: 8px; margin: 8px 0; color: white;'>
                        <strong>{member}</strong><br>
                        <small style='opacity: 0.8;'>{tasks} task(s)</small>
                    </div>
                """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
                    padding: 40px; border-radius: 20px; margin-bottom: 30px; color: white;
                    box-shadow: 0 10px 40px rgba(37, 99, 235, 0.3);'>
            <h1 style='margin: 0; font-size: 2.5em; font-weight: 800;'>
                🎯 {st.session_state.current_project}
            </h1>
            <p style='margin: 15px 0 0 0; font-size: 1.2em; opacity: 0.95;'>
                Engineering Project Control Center • Real-time Monitoring Dashboard
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Smart Calendar",
        "📊 Analytics Hub",
        "📋 Master Document List",
        "👥 Resource Management",
        "📈 Reports & Insights"
    ])
    
    # ==================== TAB 1: SMART CALENDAR ====================
    with tab1:
        col_cal, col_detail = st.columns([2, 3])
        
        with col_cal:
            st.subheader("📅 Project Calendar")
            
            today = date.today()
            months = list(calendar.month_name)[1:]
            sel_month = st.selectbox("Month", months, index=today.month-1)
            month_idx = months.index(sel_month) + 1
            
            cal = calendar.monthcalendar(2026, month_idx)
            df_cal = st.session_state.tasks.copy()
            df_cal['Due Date'] = pd.to_datetime(df_cal['Due Date']).dt.date
            
            # Build Calendar HTML
            cal_html = f"""
            <div class="calendar-container">
                <div class="calendar-header">
                    <h3 style='margin: 0; font-size: 1.5em;'>{sel_month} 2026</h3>
                    <span style='color: #64748b;'>Click any day to view tasks</span>
                </div>
                <table class="calendar-table">
                <thead><tr>
                    <th>MON</th><th>TUE</th><th>WED</th><th>THU</th>
                    <th>FRI</th><th>SAT</th><th>SUN</th>
                </tr></thead>
                <tbody>
            """
            
            for week in cal:
                cal_html += "<tr>"
                for i, day in enumerate(week):
                    if day == 0:
                        cal_html += '<td class="empty-day"></td>'
                    else:
                        cur_date = date(2026, month_idx, day)
                        tasks = df_cal[df_cal['Due Date'] == cur_date]
                        count = len(tasks)
                        
                        is_today = "today" if cur_date == today else ""
                        is_weekend = "weekend" if i >= 5 else ""
                        
                        cal_html += f'<td class="{is_today} {is_weekend}">'
                        cal_html += f'<span class="day-number">{day}</span>'
                        
                        if count > 0:
                            cal_html += f'<span class="task-count">{count}</span>'
                            for _, t in tasks.iterrows():
                                color = get_priority_color(t['Priority'])
                                cal_html += f'<span class="task-indicator" style="background:{color}"></span>'
                        
                        cal_html += '</td>'
                cal_html += "</tr>"
            
            cal_html += "</tbody></table></div>"
            st.markdown(cal_html, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 12px; margin-top: 20px;'>
                    <strong style='font-size: 1.1em;'>🎨 Priority Legend</strong><br><br>
                    <span style='color: #ef4444; font-size: 1.5em;'>●</span> <strong>Critical</strong> &nbsp;&nbsp;
                    <span style='color: #f59e0b; font-size: 1.5em;'>●</span> <strong>High</strong> &nbsp;&nbsp;
                    <span style='color: #3b82f6; font-size: 1.5em;'>●</span> <strong>Medium</strong> &nbsp;&nbsp;
                    <span style='color: #10b981; font-size: 1.5em;'>●</span> <strong>Low</strong>
                </div>
            """, unsafe_allow_html=True)
        
        with col_detail:
            st.subheader("🔍 Daily Task Overview")
            picked = st.date_input("Select Date", today, key="cal_picker")
            
            df = st.session_state.tasks.copy()
            df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
            filtered = df[df['Due Date'] == picked]
            
            if not filtered.empty:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #2563eb, #7c3aed); 
                                padding: 25px; border-radius: 15px; color: white; margin-bottom: 25px;'>
                        <h2 style='margin: 0; font-size: 1.8em;'>
                            📋 {len(filtered)} Task(s) on {picked.strftime('%B %d, %Y')}
                        </h2>
                        <p style='margin: 10px 0 0 0; opacity: 0.9;'>
                            {len(filtered.groupby('Owner'))} team member(s) with deliverables
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                for owner, tasks in filtered.groupby('Owner'):
                    avg_prog = tasks['Progress'].mean()
                    health, icon, _ = calculate_health(avg_prog)
                    
                    st.markdown(f"""
                        <div class="team-member-card">
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
                                <h3 style='margin: 0; color: #1e293b; font-size: 1.3em;'>
                                    👤 {owner}
                                </h3>
                                <div>
                                    <span style='background: #dbeafe; color: #2563eb; padding: 6px 14px;
                                                 border-radius: 20px; font-size: 12px; font-weight: 700; margin-right: 8px;'>
                                        {len(tasks)} TASK(S)
                                    </span>
                                    <span style='background: #dcfce7; color: #16a34a; padding: 6px 14px;
                                                 border-radius: 20px; font-size: 12px; font-weight: 700;'>
                                        {avg_prog:.0f}% AVG
                                    </span>
                                </div>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    for idx, (_, task) in enumerate(tasks.iterrows(), 1):
                        pcol = get_priority_color(task['Priority'])
                        
                        st.markdown(f"""
                            <div class="task-card" style='border-left-color: {pcol};'>
                                <div style='display: flex; justify-content: space-between;'>
                                    <div style='flex: 1;'>
                                        <div style='margin-bottom: 12px;'>
                                            <span style='background: {pcol}; color: white; padding: 4px 12px;
                                                         border-radius: 14px; font-size: 11px; font-weight: 700;
                                                         text-transform: uppercase;'>
                                                {task['Priority']}
                                            </span>
                                            <span style='background: #e2e8f0; color: #475569; padding: 4px 12px;
                                                         border-radius: 14px; font-size: 11px; font-weight: 700;
                                                         margin-left: 8px; text-transform: uppercase;'>
                                                {task['Status']}
                                            </span>
                                        </div>
                                        <h4 style='margin: 10px 0; color: #1e293b; font-size: 1.1em;'>
                                            {idx}. {task['Item']}
                                        </h4>
                                        <p style='margin: 8px 0; color: #64748b; font-size: 0.9em;'>
                                            📄 <strong>ID:</strong> {task['ID']} &nbsp;|&nbsp;
                                            📂 <strong>Category:</strong> {task.get('Category', 'General')}
                                        </p>
                                    </div>
                                    <div style='text-align: center; min-width: 100px;'>
                                        <div style='font-size: 2.5em; font-weight: 800; color: {pcol};'>
                                            {task['Progress']}%
                                        </div>
                                        <div style='font-size: 0.75em; color: #64748b; text-transform: uppercase;'>
                                            Complete
                                        </div>
                                    </div>
                                </div>
                                <div style='margin-top: 15px; padding-top: 15px; border-top: 2px solid #f1f5f9;'>
                                    <div style='background: #e2e8f0; height: 10px; border-radius: 10px; overflow: hidden;'>
                                        <div style='background: linear-gradient(90deg, {pcol}, {pcol}aa);
                                                    height: 100%; width: {task["Progress"]}%;
                                                    transition: width 0.5s ease;'></div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background: white; padding: 60px; border-radius: 20px;
                                text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);'>
                        <div style='font-size: 5em; margin-bottom: 20px;'>📭</div>
                        <h2 style='color: #64748b; margin: 0;'>No Tasks Scheduled</h2>
                        <p style='color: #94a3b8; margin-top: 15px; font-size: 1.1em;'>
                            This day is clear - no deadlines or deliverables
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Upcoming
            st.markdown("---")
            st.subheader("📌 Next 5 Deadlines")
            upcoming = df[df['Due Date'] > picked].sort_values('Due Date').head(5)
            
            if not upcoming.empty:
                for _, row in upcoming.iterrows():
                    days = (row['Due Date'] - picked).days
                    pcol = get_priority_color(row['Priority'])
                    st.markdown(f"""
                        <div style='background: white; padding: 15px; border-radius: 12px;
                                    margin: 10px 0; border-left: 4px solid {pcol};
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
                            <strong style='color: {pcol}; font-size: 1.05em;'>{row['Item']}</strong><br>
                            <small style='color: #64748b;'>
                                👤 {row['Owner']} &nbsp;•&nbsp;
                                📅 In {days} day(s) ({row['Due Date'].strftime('%b %d')}) &nbsp;•&nbsp;
                                📊 {row['Progress']}%
                            </small>
                        </div>
                    """, unsafe_allow_html=True)
    
    # ==================== TAB 2: ANALYTICS ====================
    with tab2:
        df = st.session_state.tasks.copy()
        df['Due Date'] = pd.to_datetime(df['Due Date'])
        
        # KPIs
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📋 Total Tasks", len(df), delta=f"{len(df[df['Progress']<100])} active")
        m2.metric("📈 Avg Progress", f"{df['Progress'].mean():.1f}%")
        m3.metric("⚠️ Critical Items", len(df[df['Priority']=='Critical']))
        m4.metric("✅ Completed", len(df[df['Progress']==100]))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row 1
        c1, c2 = st.columns(2)
        with c1:
            status = df['Status'].value_counts()
            fig1 = px.pie(values=status.values, names=status.index,
                         title="📊 Task Status Distribution", hole=0.5,
                         color_discrete_sequence=px.colors.qualitative.Bold)
            fig1.update_traces(textposition='inside', textinfo='percent+label',
                             textfont_size=14)
            fig1.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig1, use_container_width=True)
        
        with c2:
            owner_avg = df.groupby('Owner')['Progress'].mean().sort_values(ascending=True)
            fig2 = px.bar(x=owner_avg.values, y=owner_avg.index,
                         title="👥 Team Performance (Avg Progress)",
                         labels={'x': 'Progress %', 'y': 'Team Member'},
                         color=owner_avg.values, color_continuous_scale='Viridis')
            fig2.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Charts Row 2
        c3, c4 = st.columns(2)
        with c3:
            priority = df['Priority'].value_counts()
            fig3 = px.bar(x=priority.index, y=priority.values,
                         title="⚠️ Priority Distribution",
                         color=priority.index,
                         color_discrete_map={
                             'Critical': '#ef4444', 'High': '#f59e0b',
                             'Medium': '#3b82f6', 'Low': '#10b981'
                         })
            fig3.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
        
        with c4:
            category = df.groupby('Category')['Progress'].mean().sort_values(ascending=False)
            fig4 = px.bar(x=category.index, y=category.values,
                         title="📂 Progress by Category",
                         color=category.values, color_continuous_scale='Blues')
            fig4.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)
        
        # Gantt
        st.subheader("🗓️ Project Timeline (Gantt Chart)")
        df_gantt = df.copy()
        df_gantt['Start'] = pd.to_datetime(date.today())
        fig_gantt = px.timeline(df_gantt, x_start='Start', x_end='Due Date',
                               y='Item', color='Owner', hover_data=['Status', 'Progress'])
        fig_gantt.update_yaxes(categoryorder='total ascending')
        fig_gantt.update_layout(height=500)
        st.plotly_chart(fig_gantt, use_container_width=True)
    
    # ==================== TAB 3: MDL ====================
    with tab3:
        st.subheader("📋 Master Document List")
        
        df_mdl = st.session_state.tasks.copy()
        
        # Filters
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            status_f = st.multiselect("Status", df_mdl['Status'].unique(),
                                     default=df_mdl['Status'].unique())
        with f2:
            owner_f = st.multiselect("Owner", df_mdl['Owner'].unique(),
                                    default=df_mdl['Owner'].unique())
        with f3:
            priority_f = st.multiselect("Priority", df_mdl['Priority'].unique(),
                                       default=df_mdl['Priority'].unique())
        with f4:
            category_f = st.multiselect("Category", df_mdl['Category'].unique(),
                                       default=df_mdl['Category'].unique())
        
        filtered = df_mdl[
            (df_mdl['Status'].isin(status_f)) &
            (df_mdl['Owner'].isin(owner_f)) &
            (df_mdl['Priority'].isin(priority_f)) &
            (df_mdl['Category'].isin(category_f))
        ]
        
        if len(filtered) > 0:
            st.dataframe(filtered, use_container_width=True, height=400,
                        column_config={
                            "Progress": st.column_config.ProgressColumn(
                                "Progress", format="%d%%", min_value=0, max_value=100),
                            "Due Date": st.column_config.DateColumn(
                                "Due Date", format="DD/MM/YYYY")
                        })
        else:
            st.info("No tasks match filters")
        
        # Add Task
        with st.expander("➕ Add New Task"):
            with st.form("add_task"):
                c1, c2 = st.columns(2)
                with c1:
                    tid = st.text_input("ID", placeholder="DOC-XX")
                    item = st.text_input("Task Name")
                    status = st.selectbox("Status", ["Pending", "In Progress",
                                                     "Technical Evaluation", "Submitted", "Completed"])
                with c2:
                    owner = st.selectbox("Owner", st.session_state.team_members)
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                    category = st.selectbox("Category", ["Engineering", "Procurement",
                                                         "Construction", "Quality", "Safety"])
                
                due = st.date_input("Due Date", min_value=date.today())
                prog = st.slider("Progress %", 0, 100, 0, 5)
                
                if st.form_submit_button("✅ Add Task", use_container_width=True):
                    if tid and item:
                        new = {"ID": tid, "Item": item, "Owner": owner, "Status": status,
                              "Due Date": due, "Progress": prog, "Priority": priority,
                              "Category": category}
                        st.session_state.tasks = pd.concat([st.session_state.tasks,
                                                           pd.DataFrame([new])], ignore_index=True)
                        log_activity("Task Created", item)
                        st.success(f"✅ {item} added!")
                        st.rerun()
        
        # Edit Task
        with st.expander("✏️ Edit Task"):
            if len(filtered) > 0:
                edit_id = st.selectbox("Select Task", filtered['ID'].tolist(),
                                      format_func=lambda x: f"{x} - {filtered[filtered['ID']==x]['Item'].iloc[0]}")
                task = filtered[filtered['ID'] == edit_id].iloc[0]
                
                with st.form("edit_task"):
                    e1, e2 = st.columns(2)
                    with e1:
                        e_owner = st.selectbox("Owner", st.session_state.team_members,
                                              index=st.session_state.team_members.index(task['Owner']))
                        e_status = st.selectbox("Status", ["Pending", "In Progress",
                                                           "Technical Evaluation", "Submitted", "Completed"],
                                               index=["Pending", "In Progress", "Technical Evaluation",
                                                     "Submitted", "Completed"].index(task['Status']))
                    with e2:
                        e_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"],
                                                 index=["Low", "Medium", "High", "Critical"].index(task['Priority']))
                        e_prog = st.slider("Progress", 0, 100, int(task['Progress']), 5)
                    
                    if st.form_submit_button("💾 Save", use_container_width=True):
                        idx = st.session_state.tasks[st.session_state.tasks['ID'] == edit_id].index[0]
                        st.session_state.tasks.at[idx, 'Owner'] = e_owner
                        st.session_state.tasks.at[idx, 'Status'] = e_status
                        st.session_state.tasks.at[idx, 'Priority'] = e_priority
                        st.session_state.tasks.at[idx, 'Progress'] = e_prog
                        log_activity("Task Updated", edit_id)
                        st.success("✅ Updated!")
                        st.rerun()
    
    # ==================== TAB 4: RESOURCES ====================
    with tab4:
        st.subheader("👥 Resource Management")
        
        df_team = st.session_state.tasks.copy()
        team_stats = df_team.groupby('Owner').agg({
            'ID': 'count',
            'Progress': 'mean'
        }).reset_index()
        team_stats.columns = ['Owner', 'Tasks', 'Avg Progress']
        
        for _, member in team_stats.iterrows():
            st.markdown(f"""
                <div class="team-member-card">
                    <h3 style='margin: 0 0 15px 0; color: #1e293b;'>
                        👤 {member['Owner']}
                    </h3>
            """, unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Tasks", int(member['Tasks']))
            c2.metric("Avg Progress", f"{member['Avg Progress']:.1f}%")
            
            member_tasks = df_team[df_team['Owner'] == member['Owner']]
            member_tasks['Due Date'] = pd.to_datetime(member_tasks['Due Date'])
            overdue = len(member_tasks[
                (member_tasks['Due Date'] < pd.Timestamp(date.today())) &
                (member_tasks['Progress'] < 100)
            ])
            c3.metric("Overdue", overdue, delta="Attention" if overdue > 0 else "Clear")
            
            critical = len(member_tasks[member_tasks['Priority'] == 'Critical'])
            c4.metric("Critical", critical)
            
            st.dataframe(member_tasks[['ID', 'Item', 'Status', 'Progress', 'Due Date', 'Priority']],
                        use_container_width=True, hide_index=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # ==================== TAB 5: REPORTS ====================
    with tab5:
        st.subheader("📈 Executive Summary & Insights")
        
        df_rep = st.session_state.tasks.copy()
        df_rep['Due Date'] = pd.to_datetime(df_rep['Due Date'])
        
        # Summary
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #2563eb, #7c3aed);
                        padding: 40px; border-radius: 20px; color: white; margin-bottom: 30px;'>
                <h2 style='margin: 0 0 20px 0;'>📊 Project Health Dashboard</h2>
                <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;'>
                    <div>
                        <div style='font-size: 2.5em; font-weight: 800;'>{proj['progress']}%</div>
                        <div style='opacity: 0.9;'>Overall Progress</div>
                    </div>
                    <div>
                        <div style='font-size: 2.5em; font-weight: 800;'>{len(df_rep)}</div>
                        <div style='opacity: 0.9;'>Total Deliverables</div>
                    </div>
                    <div>
                        <div style='font-size: 2.5em; font-weight: 800;'>{len(st.session_state.team_members)}</div>
                        <div style='opacity: 0.9;'>Team Members</div>
                    </div>
                    <div>
                        <div style='font-size: 2.5em; font-weight: 800;'>{(proj['end']-date.today()).days}</div>
                        <div style='opacity: 0.9;'>Days Remaining</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Key Insights
        st.markdown("### 🔍 Key Insights")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**📌 Top Performer:** {df_rep.groupby('Owner')['Progress'].mean().idxmax()} "
                   f"with {df_rep.groupby('Owner')['Progress'].mean().max():.1f}% avg progress")
            
            overdue_all = len(df_rep[(df_rep['Due Date'] < pd.Timestamp(date.today())) &
                                     (df_rep['Progress'] < 100)])
            if overdue_all > 0:
                st.warning(f"⚠️ **{overdue_all} overdue tasks** require immediate attention")
            else:
                st.success("✅ No overdue tasks - project on track!")
        
        with col2:
            critical_count = len(df_rep[df_rep['Priority'] == 'Critical'])
            st.error(f"🔴 **{critical_count} critical priority items** in pipeline")
            
            next_week = df_rep[df_rep['Due Date'] <= pd.Timestamp(date.today() + timedelta(days=7))]
            st.warning(f"📅 **{len(next_week)} tasks due** within next 7 days")
        
        # Activity Log
        if st.session_state.activity_log:
            st.markdown("### 📜 Recent Activity")
            for log in reversed(st.session_state.activity_log[-10:]):
                st.text(f"{log['timestamp'].strftime('%Y-%m-%d %H:%M')} - {log['action']}: {log['details']}")

# Footer
st.markdown("<br><hr style='border-color: rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
st.markdown("""
    <center style='color: #64748b; padding: 30px;'>
        <div style='font-size: 2em; margin-bottom: 15px;'>⚡</div>
        <strong style='font-size: 1.2em;'>Elsewedy Electric - Engineering Control Platform</strong><br>
        <small style='opacity: 0.7;'>Enterprise EPC Project Management System • v5.0 Ultimate Edition</small><br>
        <small style='opacity: 0.7;'>© 2026 Elsewedy Electric. All Rights Reserved.</small>
    </center>
""", unsafe_allow_html=True)
