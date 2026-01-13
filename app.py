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

# ستايل محسّن مع تدرجات لونية احترافية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .project-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center;
        height: 240px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .project-card:hover::before {
        opacity: 1;
    }
    
    .project-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .project-card h2 {
        color: white;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .project-card p {
        color: rgba(255,255,255,0.9);
    }
    
    [data-testid="stMetric"] {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background: white;
        border-radius: 12px 12px 0 0;
        padding: 12px 25px;
        font-weight: 600;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f0f0f0;
        border-color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: #667eea;
    }
    
    .status-badge {
        display: inline-block;
        padding: 6px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
    }
    
    .status-active {
        background-color: #10b981;
        color: white;
    }
    
    .status-planning {
        background-color: #f59e0b;
        color: white;
    }
    
    .status-proposed {
        background-color: #6366f1;
        color: white;
    }
    
    .status-completed {
        background-color: #8b5cf6;
        color: white;
    }
    
    .progress-ring {
        width: 100px;
        height: 100px;
        margin: 15px auto;
    }
    
    div[data-testid="stDataFrame"] {
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. تهيئة البيانات في Session State ---
def initialize_session_state():
    """تهيئة جميع متغيرات الحالة"""
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    
    if 'team_members' not in st.session_state:
        st.session_state.team_members = [
            "Hossam Atta",
            "Omar Fathy",
            "Mokhtar Mostafa",
            "Ahmed Hassan",
            "Sara Mohamed"
        ]
    
    if 'projects' not in st.session_state:
        st.session_state.projects = {
            "Morjan Power Station": {
                "info": "Main EPC Project",
                "status": "Active",
                "progress": 65,
                "budget": "250M USD",
                "start_date": date(2025, 1, 1),
                "end_date": date(2027, 12, 31)
            },
            "Solar Farm Delta": {
                "info": "Renewable Energy Project",
                "status": "Planning",
                "progress": 25,
                "budget": "180M USD",
                "start_date": date(2026, 3, 1),
                "end_date": date(2028, 6, 30)
            },
            "Substation Upgrade": {
                "info": "Infrastructure Enhancement",
                "status": "Proposed",
                "progress": 5,
                "budget": "95M USD",
                "start_date": date(2026, 6, 1),
                "end_date": date(2027, 12, 31)
            },
            "Industrial Complex": {
                "info": "Manufacturing Facility",
                "status": "Completed",
                "progress": 100,
                "budget": "320M USD",
                "start_date": date(2023, 1, 1),
                "end_date": date(2025, 12, 31)
            }
        }
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = pd.DataFrame([
            {
                "ID": "DOC-01",
                "Item": "Mechanical Layout Design",
                "Owner": "Hossam Atta",
                "Status": "In Progress",
                "Due Date": date(2026, 2, 15),
                "Progress": 65,
                "Priority": "High"
            },
            {
                "ID": "RFQ-01",
                "Item": "Fire Pump System RFQ",
                "Owner": "Omar Fathy",
                "Status": "Technical Evaluation",
                "Due Date": date(2026, 1, 25),
                "Progress": 40,
                "Priority": "Critical"
            },
            {
                "ID": "RFQ-02",
                "Item": "Package Unit RFQ",
                "Owner": "Mokhtar Mostafa",
                "Status": "Pending",
                "Due Date": date(2026, 1, 30),
                "Progress": 10,
                "Priority": "Medium"
            },
            {
                "ID": "DOC-02",
                "Item": "Electrical Single Line Diagram",
                "Owner": "Ahmed Hassan",
                "Status": "In Progress",
                "Due Date": date(2026, 2, 5),
                "Progress": 80,
                "Priority": "High"
            },
            {
                "ID": "RFQ-03",
                "Item": "Transformer Procurement",
                "Owner": "Sara Mohamed",
                "Status": "Submitted",
                "Due Date": date(2026, 1, 20),
                "Progress": 90,
                "Priority": "Critical"
            }
        ])

initialize_session_state()

# --- 3. دوال مساعدة ---
def get_status_color(status):
    """الحصول على لون الحالة"""
    colors = {
        "Active": "#10b981",
        "Planning": "#f59e0b",
        "Proposed": "#6366f1",
        "Completed": "#8b5cf6"
    }
    return colors.get(status, "#6b7280")

def get_priority_color(priority):
    """الحصول على لون الأولوية"""
    colors = {
        "Critical": "#ef4444",
        "High": "#f59e0b",
        "Medium": "#3b82f6",
        "Low": "#10b981"
    }
    return colors.get(priority, "#6b7280")

def calculate_project_health(progress, tasks_df):
    """حساب صحة المشروع"""
    if progress >= 90:
        return "Excellent", "🟢"
    elif progress >= 70:
        return "On Track", "🟡"
    elif progress >= 50:
        return "At Risk", "🟠"
    else:
        return "Critical", "🔴"

# --- 4. الواجهة الرئيسية (Projects Hub) ---
if st.session_state.current_project is None:
    # Header مع animation
    st.markdown("""
        <div style='text-align: center; padding: 40px 0;'>
            <h1 style='font-size: 3.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       font-weight: 800; margin-bottom: 10px;'>
                🏗️ Elsewedy Electric
            </h1>
            <h2 style='color: #4b5563; font-weight: 400; font-size: 1.8em;'>
                Engineering Control Hub
            </h2>
            <p style='color: #6b7280; font-size: 1.2em; margin-top: 15px;'>
                Select a project to monitor performance and track deliverables
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # عرض المشاريع في grid
    cols = st.columns(min(len(st.session_state.projects), 4))
    
    for i, (name, info) in enumerate(st.session_state.projects.items()):
        with cols[i % 4]:
            status_class = f"status-{info['status'].lower()}"
            
            st.markdown(f"""
                <div class="project-card">
                    <h2>{name}</h2>
                    <p style='font-size: 1.1em; margin: 10px 0;'>{info['info']}</p>
                    <span class='status-badge {status_class}'>{info['status']}</span>
                    <div style='margin-top: 20px;'>
                        <div style='font-size: 2.5em; font-weight: 800;'>{info['progress']}%</div>
                        <div style='font-size: 0.9em; opacity: 0.9;'>Project Progress</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("📊 Manage Project", key=f"btn_{i}", use_container_width=True):
                st.session_state.current_project = name
                st.rerun()

# --- 5. واجهة المشروع التفصيلية ---
else:
    project_info = st.session_state.projects[st.session_state.current_project]
    
    # Sidebar محسّن
    with st.sidebar:
        if st.button("⬅️ Back to Project Hub", use_container_width=True):
            st.session_state.current_project = None
            st.rerun()
        
        st.markdown("---")
        st.title(f"📍 {st.session_state.current_project}")
        st.info(f"**Type:** {project_info['info']}")
        
        st.markdown("### 📊 Project Overview")
        st.metric("Budget", project_info['budget'])
        st.metric("Status", project_info['status'])
        st.metric("Progress", f"{project_info['progress']}%")
        
        st.markdown("### 📅 Timeline")
        st.write(f"**Start:** {project_info['start_date'].strftime('%b %d, %Y')}")
        st.write(f"**End:** {project_info['end_date'].strftime('%b %d, %Y')}")
        
        # حساب الأيام المتبقية
        days_remaining = (project_info['end_date'] - date.today()).days
        st.metric("Days Remaining", days_remaining)
        
        st.markdown("---")
        
        # إدارة أعضاء الفريق
        st.markdown("### 👥 Team Management")
        
        with st.expander("➕ Add Team Member"):
            with st.form("add_member_form"):
                new_member = st.text_input("Member Name", placeholder="e.g., Mohamed Ali")
                if st.form_submit_button("Add Member", use_container_width=True):
                    if new_member and new_member.strip():
                        if new_member not in st.session_state.team_members:
                            st.session_state.team_members.append(new_member)
                            st.success(f"✅ {new_member} added!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Member already exists")
                    else:
                        st.error("⚠️ Please enter a name")
        
        with st.expander("✏️ Edit/Remove Members"):
            if len(st.session_state.team_members) > 0:
                for idx, member in enumerate(st.session_state.team_members):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"👤 {member}")
                    with col2:
                        if st.button("🗑️", key=f"del_{idx}"):
                            # التحقق من وجود مهام للعضو
                            tasks_count = len(st.session_state.tasks[st.session_state.tasks['Owner'] == member])
                            if tasks_count > 0:
                                st.warning(f"⚠️ {member} has {tasks_count} task(s). Reassign them first!")
                            else:
                                st.session_state.team_members.remove(member)
                                st.rerun()
            else:
                st.info("No team members yet")
        
        # عرض قائمة الأعضاء
        st.markdown("### 📋 Current Team")
        for member in st.session_state.team_members:
            tasks_count = len(st.session_state.tasks[st.session_state.tasks['Owner'] == member])
            st.markdown(f"""
                <div style='background: #f0f0f0; padding: 8px; border-radius: 8px; margin: 5px 0;'>
                    <strong>{member}</strong><br>
                    <small>{tasks_count} task(s)</small>
                </div>
            """, unsafe_allow_html=True)

    # Header الصفحة
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; margin-bottom: 30px; color: white;'>
            <h1 style='margin: 0; color: white;'>🚀 {st.session_state.current_project}</h1>
            <p style='margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;'>Control Center & Analytics Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs التفصيلية
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Monthly Calendar",
        "📊 Analytics Dashboard",
        "📋 Master Document List",
        "👥 Team Resources"
    ])

    # --- Tab 1: التقويم الشهري ---
    with tab1:
        st.subheader("📅 Interactive Project Calendar")
        
        col_c1, col_c2 = st.columns([2, 3])
        
        with col_c1:
            today = date.today()
            months = list(calendar.month_name)[1:]
            sel_month = st.selectbox("Select Month", months, index=today.month - 1)
            month_idx = months.index(sel_month) + 1
            
            # إنشاء التقويم
            cal = calendar.monthcalendar(2026, month_idx)
            
            # تحضير البيانات للتقويم
            df_cal = st.session_state.tasks.copy()
            if 'Priority' not in df_cal.columns:
                df_cal['Priority'] = 'Medium'
            df_cal['Due Date'] = pd.to_datetime(df_cal['Due Date']).dt.date
            
            # إنشاء HTML للتقويم التفاعلي
            calendar_html = """
            <style>
            .calendar-container {
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .calendar-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            .calendar-table th {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px;
                text-align: center;
                font-weight: 600;
                font-size: 14px;
            }
            .calendar-table td {
                padding: 15px;
                text-align: center;
                border: 1px solid #e0e0e0;
                cursor: pointer;
                transition: all 0.3s;
                position: relative;
                height: 60px;
                vertical-align: top;
            }
            .calendar-table td:hover {
                background: #f0f0ff;
                transform: scale(1.05);
                box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
            }
            .day-number {
                font-weight: 600;
                font-size: 16px;
                color: #333;
            }
            .task-indicator {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                display: inline-block;
                margin: 2px;
            }
            .task-count {
                position: absolute;
                top: 5px;
                right: 5px;
                background: #ef4444;
                color: white;
                border-radius: 10px;
                padding: 2px 6px;
                font-size: 10px;
                font-weight: 600;
            }
            .empty-day {
                background: #f9f9f9;
            }
            .today {
                background: #fff3cd !important;
                border: 2px solid #ffc107 !important;
            }
            </style>
            <div class="calendar-container">
            <table class="calendar-table">
            <thead>
            <tr>
                <th>Mon</th>
                <th>Tue</th>
                <th>Wed</th>
                <th>Thu</th>
                <th>Fri</th>
                <th>Sat</th>
                <th>Sun</th>
            </tr>
            </thead>
            <tbody>
            """
            
            # ملء التقويم
            for week in cal:
                calendar_html += "<tr>"
                for day in week:
                    if day == 0:
                        calendar_html += '<td class="empty-day"></td>'
                    else:
                        current_date = date(2026, month_idx, day)
                        tasks_on_day = df_cal[df_cal['Due Date'] == current_date]
                        task_count = len(tasks_on_day)
                        
                        is_today = "today" if current_date == today else ""
                        
                        calendar_html += f'<td class="{is_today}">'
                        calendar_html += f'<div class="day-number">{day}</div>'
                        
                        if task_count > 0:
                            calendar_html += f'<span class="task-count">{task_count}</span>'
                            # إضافة مؤشرات ملونة حسب الأولوية
                            for _, task in tasks_on_day.iterrows():
                                color = get_priority_color(task.get('Priority', 'Medium'))
                                calendar_html += f'<span class="task-indicator" style="background: {color};"></span>'
                        
                        calendar_html += '</td>'
                calendar_html += "</tr>"
            
            calendar_html += """
            </tbody>
            </table>
            </div>
            """
            
            st.markdown(calendar_html, unsafe_allow_html=True)
            
            # دليل الألوان
            st.markdown("""
                <div style='background: white; padding: 15px; border-radius: 10px; margin-top: 15px;'>
                    <strong>🎨 Priority Legend:</strong><br>
                    <span style='color: #ef4444;'>●</span> Critical &nbsp;
                    <span style='color: #f59e0b;'>●</span> High &nbsp;
                    <span style='color: #3b82f6;'>●</span> Medium &nbsp;
                    <span style='color: #10b981;'>●</span> Low
                </div>
            """, unsafe_allow_html=True)
        
        with col_c2:
            st.markdown("#### 🔍 Daily Task Details")
            picked_day = st.date_input("📅 Select Date to View Tasks", today, key="day_picker")
            
            # فلترة المهام حسب التاريخ
            df = st.session_state.tasks.copy()
            if 'Priority' not in df.columns:
                df['Priority'] = 'Medium'
            df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
            
            filtered = df[df['Due Date'] == picked_day]
            
            if not filtered.empty:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px;'>
                        <h3 style='margin: 0; color: white;'>📋 {len(filtered)} Task(s) on {picked_day.strftime('%B %d, %Y')}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                # تجميع المهام حسب الشخص
                team_tasks = filtered.groupby('Owner')
                
                for owner, tasks in team_tasks:
                    # عدد المهام لكل شخص
                    task_count = len(tasks)
                    avg_progress = tasks['Progress'].mean()
                    
                    # كارد لكل شخص
                    st.markdown(f"""
                        <div style='background: white; padding: 20px; border-radius: 15px; 
                                    margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                                    border-left: 5px solid #667eea;'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                                <h3 style='margin: 0; color: #667eea;'>👤 {owner}</h3>
                                <div>
                                    <span style='background: #e0e7ff; color: #667eea; padding: 5px 12px; 
                                                 border-radius: 20px; font-size: 12px; font-weight: 600;'>
                                        {task_count} Task(s)
                                    </span>
                                    <span style='background: #dcfce7; color: #16a34a; padding: 5px 12px; 
                                                 border-radius: 20px; font-size: 12px; font-weight: 600; margin-left: 8px;'>
                                        {avg_progress:.0f}% Avg Progress
                                    </span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # عرض كل تاسك للشخص
                    for idx, (_, task) in enumerate(tasks.iterrows(), 1):
                        priority_color = get_priority_color(task.get('Priority', 'Medium'))
                        status_color = {
                            'Completed': '#10b981',
                            'In Progress': '#3b82f6',
                            'Pending': '#f59e0b',
                            'Technical Evaluation': '#8b5cf6',
                            'Submitted': '#06b6d4'
                        }.get(task['Status'], '#6b7280')
                        
                        st.markdown(f"""
                            <div style='background: #f8fafc; padding: 18px; border-radius: 12px; 
                                        margin: 12px 0; border-left: 4px solid {priority_color};
                                        transition: all 0.3s;'>
                                <div style='display: flex; justify-content: space-between; align-items: start;'>
                                    <div style='flex: 1;'>
                                        <div style='margin-bottom: 8px;'>
                                            <span style='background: {priority_color}; color: white; padding: 3px 10px; 
                                                         border-radius: 12px; font-size: 11px; font-weight: 600;'>
                                                {task.get('Priority', 'Medium')}
                                            </span>
                                            <span style='background: {status_color}; color: white; padding: 3px 10px; 
                                                         border-radius: 12px; font-size: 11px; font-weight: 600; margin-left: 6px;'>
                                                {task['Status']}
                                            </span>
                                        </div>
                                        <h4 style='margin: 8px 0; color: #1e293b; font-size: 16px;'>
                                            {idx}. {task['Item']}
                                        </h4>
                                        <p style='margin: 5px 0; color: #64748b; font-size: 13px;'>
                                            📄 <strong>ID:</strong> {task['ID']}
                                        </p>
                                    </div>
                                    <div style='text-align: right; min-width: 80px;'>
                                        <div style='font-size: 28px; font-weight: 700; color: {priority_color};'>
                                            {task['Progress']}%
                                        </div>
                                        <div style='font-size: 11px; color: #64748b;'>Progress</div>
                                    </div>
                                </div>
                                <div style='margin-top: 12px; padding-top: 12px; border-top: 1px solid #e2e8f0;'>
                                    <div style='background: #e2e8f0; height: 8px; border-radius: 10px; overflow: hidden;'>
                                        <div style='background: {priority_color}; height: 100%; width: {task["Progress"]}%; 
                                                    transition: width 0.3s;'></div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                    <div style='background: white; padding: 40px; border-radius: 15px; 
                                text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
                        <div style='font-size: 64px; margin-bottom: 15px;'>📭</div>
                        <h3 style='color: #64748b; margin: 0;'>No Tasks Scheduled</h3>
                        <p style='color: #94a3b8; margin-top: 10px;'>This day is clear - no deadlines!</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # عرض المهام القادمة
            st.markdown("---")
            st.markdown("#### 📌 Upcoming Deadlines")
            upcoming = df[df['Due Date'] > picked_day].sort_values('Due Date').head(5)
            
            if not upcoming.empty:
                for _, row in upcoming.iterrows():
                    days_until = (row['Due Date'] - picked_day).days
                    priority_color = get_priority_color(row.get('Priority', 'Medium'))
                    
                    st.markdown(f"""
                        <div style='background: white; padding: 12px; border-radius: 8px; 
                                    margin: 8px 0; border-left: 3px solid {priority_color};'>
                            <strong style='color: {priority_color};'>{row['Item']}</strong><br>
                            <small style='color: #64748b;'>
                                👤 {row['Owner']} • 📅 in {days_until} day(s) • {row['Due Date'].strftime('%b %d')}
                            </small>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No upcoming deadlines")

    # --- Tab 2: لوحة التحليلات ---
    with tab2:
        df = st.session_state.tasks.copy()
        
        # التأكد من وجود جميع الأعمدة المطلوبة
        if 'Priority' not in df.columns:
            df['Priority'] = 'Medium'
        
        df['Due Date'] = pd.to_datetime(df['Due Date'])
        
        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        
        total_tasks = len(df)
        avg_progress = df['Progress'].mean() if len(df) > 0 else 0
        completed_tasks = len(df[df['Progress'] == 100])
        health, health_icon = calculate_project_health(avg_progress, df)
        
        m1.metric("Total Deliverables", total_tasks, delta=f"{completed_tasks} completed")
        m2.metric("Average Progress", f"{avg_progress:.1f}%")
        m3.metric("Project Health", f"{health_icon} {health}")
        m4.metric("Team Members", df['Owner'].nunique() if len(df) > 0 else 0)
        
        st.markdown("---")
        
        # Charts Row 1
        c1, c2 = st.columns(2)
        
        with c1:
            # Pie Chart للحالات
            if len(df) > 0:
                status_counts = df['Status'].value_counts()
                fig_pie = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="📊 Task Status Distribution",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No data available for status distribution")
        
        with c2:
            # Bar Chart للموارد
            if len(df) > 0:
                owner_progress = df.groupby('Owner', as_index=False)['Progress'].mean()
                fig_bar = px.bar(
                    owner_progress,
                    x='Owner',
                    y='Progress',
                    title="👥 Team Performance (Avg Progress)",
                    color='Progress',
                    color_continuous_scale='Viridis'
                )
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No data available for team performance")
        
        # Charts Row 2
        c3, c4 = st.columns(2)
        
        with c3:
            # Priority Distribution
            if len(df) > 0 and 'Priority' in df.columns:
                priority_counts = df['Priority'].value_counts()
                fig_priority = px.bar(
                    x=priority_counts.index,
                    y=priority_counts.values,
                    title="⚠️ Task Priority Distribution",
                    labels={'x': 'Priority', 'y': 'Count'},
                    color=priority_counts.index,
                    color_discrete_map={
                        'Critical': '#ef4444',
                        'High': '#f59e0b',
                        'Medium': '#3b82f6',
                        'Low': '#10b981'
                    }
                )
                st.plotly_chart(fig_priority, use_container_width=True)
            else:
                st.info("No priority data available")
        
        with c4:
            # Progress Timeline
            if len(df) > 0:
                df_sorted = df.sort_values('Due Date')
                fig_timeline = px.scatter(
                    df_sorted,
                    x='Due Date',
                    y='Progress',
                    size='Progress',
                    color='Status',
                    hover_data=['Item', 'Owner'],
                    title="📈 Progress Timeline"
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
            else:
                st.info("No timeline data available")
        
        # Gantt Chart
        st.subheader("🗓️ Project Roadmap (Gantt Chart)")
        if len(df) > 0:
            df_gantt = df.copy()
            df_gantt['Start'] = pd.to_datetime(date.today())
            
            fig_gantt = px.timeline(
                df_gantt,
                x_start='Start',
                x_end='Due Date',
                y='Item',
                color='Owner',
                title="Project Timeline",
                hover_data=['Status', 'Progress']
            )
            fig_gantt.update_yaxes(categoryorder='total ascending')
            st.plotly_chart(fig_gantt, use_container_width=True)
        else:
            st.info("No tasks available for Gantt chart")

    # --- Tab 3: قائمة المستندات الرئيسية ---
    with tab3:
        st.subheader("📋 Master Document List (MDL)")
        
        # نسخ DataFrame وإضافة Priority إذا لم تكن موجودة
        df_mdl = st.session_state.tasks.copy()
        if 'Priority' not in df_mdl.columns:
            df_mdl['Priority'] = 'Medium'
        
        # فلاتر
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            status_options = df_mdl['Status'].unique().tolist() if len(df_mdl) > 0 else []
            status_filter = st.multiselect(
                "Filter by Status",
                options=status_options,
                default=status_options
            )
        
        with col_f2:
            owner_options = df_mdl['Owner'].unique().tolist() if len(df_mdl) > 0 else []
            owner_filter = st.multiselect(
                "Filter by Owner",
                options=owner_options,
                default=owner_options
            )
        
        with col_f3:
            priority_options = df_mdl['Priority'].unique().tolist() if len(df_mdl) > 0 else []
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=priority_options,
                default=priority_options
            )
        
        # تطبيق الفلاتر
        filtered_df = df_mdl[
            (df_mdl['Status'].isin(status_filter)) &
            (df_mdl['Owner'].isin(owner_filter)) &
            (df_mdl['Priority'].isin(priority_filter))
        ]
        
        # عرض الجدول
        if len(filtered_df) > 0:
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Progress": st.column_config.ProgressColumn(
                        "Progress",
                        format="%d%%",
                        min_value=0,
                        max_value=100,
                    ),
                    "Due Date": st.column_config.DateColumn(
                        "Due Date",
                        format="DD/MM/YYYY"
                    )
                }
            )
        else:
            st.info("No tasks match the selected filters")
        
        # إضافة مهمة جديدة
        with st.expander("➕ Add New Document / Task"):
            with st.form("mdl_form", clear_on_submit=True):
                cx, cy = st.columns(2)
                
                with cx:
                    t_id = st.text_input("Document ID", placeholder="e.g., DOC-03")
                    t_item = st.text_input("Document/Task Name", placeholder="e.g., HVAC Design")
                    t_status = st.selectbox("Status", ["Pending", "In Progress", "Technical Evaluation", "Submitted", "Completed"])
                
                with cy:
                    t_owner = st.selectbox("Owner", st.session_state.team_members)
                    t_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                    t_due = st.date_input("Deadline Date", min_value=date.today())
                
                t_prog = st.slider("Initial Progress %", 0, 100, 0, 5)
                
                submitted = st.form_submit_button("✅ Submit to Master Schedule", use_container_width=True)
                
                if submitted:
                    if t_id and t_item:
                        new_entry = {
                            "ID": t_id,
                            "Item": t_item,
                            "Owner": t_owner,
                            "Status": t_status,
                            "Due Date": t_due,
                            "Progress": t_prog,
                            "Priority": t_priority
                        }
                        st.session_state.tasks = pd.concat(
                            [st.session_state.tasks, pd.DataFrame([new_entry])],
                            ignore_index=True
                        )
                        st.success(f"✅ Task '{t_item}' added successfully!")
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill in all required fields")
        
        # تعديل المهام الموجودة
        with st.expander("✏️ Edit Existing Tasks"):
            if len(filtered_df) > 0:
                task_to_edit = st.selectbox(
                    "Select Task to Edit",
                    options=filtered_df['ID'].tolist(),
                    format_func=lambda x: f"{x} - {filtered_df[filtered_df['ID']==x]['Item'].iloc[0]}"
                )
                
                if task_to_edit:
                    task_data = filtered_df[filtered_df['ID'] == task_to_edit].iloc[0]
                    
                    with st.form("edit_task_form"):
                        st.markdown(f"**Editing: {task_data['Item']}**")
                        
                        ex, ey = st.columns(2)
                        with ex:
                            e_owner = st.selectbox("Owner", st.session_state.team_members, 
                                                  index=st.session_state.team_members.index(task_data['Owner']) 
                                                  if task_data['Owner'] in st.session_state.team_members else 0)
                            e_status = st.selectbox("Status", 
                                                   ["Pending", "In Progress", "Technical Evaluation", "Submitted", "Completed"],
                                                   index=["Pending", "In Progress", "Technical Evaluation", "Submitted", "Completed"].index(task_data['Status']))
                        with ey:
                            e_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"],
                                                     index=["Low", "Medium", "High", "Critical"].index(task_data['Priority']))
                            e_progress = st.slider("Progress %", 0, 100, int(task_data['Progress']), 5)
                        
                        e_due = st.date_input("Due Date", value=pd.to_datetime(task_data['Due Date']).date())
                        
                        if st.form_submit_button("💾 Save Changes", use_container_width=True):
                            # تحديث المهمة
                            idx = st.session_state.tasks[st.session_state.tasks['ID'] == task_to_edit].index[0]
                            st.session_state.tasks.at[idx, 'Owner'] = e_owner
                            st.session_state.tasks.at[idx, 'Status'] = e_status
                            st.session_state.tasks.at[idx, 'Priority'] = e_priority
                            st.session_state.tasks.at[idx, 'Progress'] = e_progress
                            st.session_state.tasks.at[idx, 'Due Date'] = e_due
                            st.success("✅ Task updated successfully!")
                            st.rerun()
            else:
                st.info("No tasks available to edit")

    # --- Tab 4: موارد الفريق ---
    with tab4:
        st.subheader("👥 Team Resources & Workload")
        
        # نسخ DataFrame وإضافة Priority إذا لم تكن موجودة
        df_team = st.session_state.tasks.copy()
        if 'Priority' not in df_team.columns:
            df_team['Priority'] = 'Medium'
        
        if len(df_team) > 0:
            # تحليل الفريق
            team_stats = df_team.groupby('Owner', as_index=False).agg({
                'ID': 'count',
                'Progress': 'mean'
            })
            team_stats.columns = ['Owner', 'Total Tasks', 'Avg Progress']
            
            # عرض إحصائيات الفريق
            for _, member in team_stats.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div style='background: white; padding: 20px; border-radius: 12px; 
                                    margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <h3 style='margin: 0; color: #667eea;'>👤 {member['Owner']}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Assigned Tasks", int(member['Total Tasks']))
                    c2.metric("Average Progress", f"{member['Avg Progress']:.1f}%")
                    
                    # حساب المهام المتأخرة
                    member_tasks = df_team[df_team['Owner'] == member['Owner']].copy()
                    member_tasks['Due Date'] = pd.to_datetime(member_tasks['Due Date'])
                    
                    overdue = len(member_tasks[
                        (member_tasks['Due Date'] < pd.Timestamp(date.today())) &
                        (member_tasks['Progress'] < 100)
                    ])
                    c3.metric("Overdue Tasks", overdue, delta="Needs attention" if overdue > 0 else "On track")
                    
                    # عرض مهام العضو
                    display_cols = ['ID', 'Item', 'Status', 'Progress', 'Due Date']
                    if 'Priority' in member_tasks.columns:
                        display_cols.append('Priority')
                    
                    st.dataframe(
                        member_tasks[display_cols],
                        use_container_width=True,
                        hide_index=True
                    )
        else:
            st.info("No team data available. Add tasks to see team statistics.")

# --- Footer ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <center style='color: #6b7280; padding: 20px;'>
        <strong>Elsewedy Electric - Engineering Control Hub v4.0</strong><br>
        <small>Powered by Streamlit | © 2026 All Rights Reserved</small>
    </center>
""", unsafe_allow_html=True)

عايزك تضيف مشروع اسمه Syncronos 
جواه 3 محطات دى ال time schedule 
اعمل update بالداتا الحقيقية 
