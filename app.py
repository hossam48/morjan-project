import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Morjan Power Station | EPC Control",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (Elsewedy Style - Dark Professional) ---
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%); }
    [data-testid="stSidebar"] { background: #1a1a2e; }
    h1, h2, h3 { color: #4a9eff !important; }
    .stMetric { background-color: #252538; padding: 15px; border-radius: 10px; border: 1px solid #444; }
    .footer { position: fixed; bottom: 0; left: 0; right: 0; background-color: #1a1a2e; padding: 5px; text-align: center; color: #7d8da6; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def calculate_metrics(df):
    today = datetime.now()
    urgent = len(df[(df['Due Date'] <= today + timedelta(days=7)) & (df['Status'] != 'Completed')])
    overdue = len(df[(df['Due Date'] < today) & (df['Status'] != 'Completed')])
    in_prog = len(df[df['Status'] == 'In Progress'])
    avg_prog = df['Progress'].mean()
    return urgent, overdue, in_prog, avg_prog

def export_to_html(df):
    html = f"""
    <html><body style='font-family:Arial; background:#f4f4f9;'>
    <h1 style='color:#357abd;'>Morjan Power Station - Status Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d')}</p>
    {df.to_html(index=False)}
    </body></html>
    """
    return html

# --- INITIALIZE DATA ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "DOC-001", "Category": "Engineering", "Item": "Mechanical Layout - Turbine Hall", "Owner": "Hossam Atta", "Status": "In Progress", "Due Date": datetime(2026, 2, 15), "Progress": 65},
        {"ID": "RFQ-101", "Category": "Procurement", "Item": "Fire Pump Package RFQ", "Owner": "Hossam Atta", "Status": "Technical Evaluation", "Due Date": datetime(2026, 1, 30), "Progress": 40},
        {"ID": "RFQ-102", "Category": "Procurement", "Item": "Package Unit RFQ", "Owner": "Omar Fathy", "Status": "In Progress", "Due Date": datetime(2026, 2, 10), "Progress": 20},
        {"ID": "CALC-01", "Category": "Engineering", "Item": "Hydraulic Calculations", "Owner": "Mokhtar Mostafa", "Status": "Pending", "Due Date": datetime(2026, 3, 5), "Progress": 0},
        {"ID": "DOC-002", "Category": "Engineering", "Item": "Piping Isometric Drawings", "Owner": "Omar Fathy", "Status": "In Progress", "Due Date": datetime(2026, 4, 20), "Progress": 30}
    ])

# --- SIDEBAR & DATA MANAGEMENT ---
st.sidebar.title("🏢 Elsewedy Electric")
st.sidebar.subheader("Morjan Project Control")

view_mode = st.sidebar.radio("Navigate", ["Executive Dashboard", "MDL Tracking", "Procurement Tracker", "Team Performance"])

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("📤 Update via Excel", type=['xlsx'])
if uploaded_file:
    st.session_state.tasks = pd.read_excel(uploaded_file)
    st.sidebar.success("Data Updated!")

# Export Logic
report_html = export_to_html(st.session_state.tasks)
st.sidebar.download_button("📥 Download HTML Report", data=report_html, file_name="Project_Report.html", mime="text/html")

# --- MAIN CONTENT ---
st.title("🏗️ Morjan Power Station - Project Hub")

df = st.session_state.tasks.copy()
df['Due Date'] = pd.to_datetime(df['Due Date'])

if view_mode == "Executive Dashboard":
    urgent, overdue, in_prog, avg_prog = calculate_metrics(df)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Items", len(df))
    col2.metric("Urgent (7 Days)", urgent, delta=f"-{overdue} Overdue", delta_color="inverse")
    col3.metric("In Progress", in_prog)
    col4.metric("Avg Completion", f"{avg_prog:.1f}%")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        fig_pie = px.pie(df, names='Status', title="Overall Status Distribution", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        fig_bar = px.bar(df, x='Owner', y='Progress', color='Status', title="Team Workload & Progress")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("📅 12-Month Outlook (Gantt)")
    fig_gantt = px.timeline(df, x_start=datetime.now(), x_end='Due Date', y='Item', color='Owner')
    st.plotly_chart(fig_gantt, use_container_width=True)

elif view_mode == "MDL Tracking":
    st.subheader("📑 Master Document List Tracking")
    mdl_df = df[df['Category'] == 'Engineering']
    st.dataframe(mdl_df.style.background_gradient(subset=['Progress'], cmap='BuGn'), use_container_width=True)

elif view_mode == "Procurement Tracker":
    st.subheader("📦 RFQ & Procurement Status")
    proc_df = df[df['Category'] == 'Procurement']
    for _, row in proc_df.iterrows():
        exp = st.expander(f"{row['ID']} - {row['Item']} ({row['Status']})")
        exp.write(f"Owner: {row['Owner']} | Deadline: {row['Due Date'].date()}")
        exp.progress(row['Progress']/100)

elif view_mode == "Team Performance":
    st.subheader("🎯 Resource Loading Analysis")
    for eng in df['Owner'].unique():
        eng_df = df[df['Owner'] == eng]
        st.write(f"**{eng}** - Tasks: {len(eng_df)} | Avg Progress: {eng_df['Progress'].mean():.0f}%")
        st.progress(eng_df['Progress'].mean()/100)

# --- ADD TASK FORM ---
with st.expander("➕ Add New Entry"):
    with st.form("new_task"):
        c1, c2, c3 = st.columns(3)
        id_in = c1.text_input("ID")
        item_in = c2.text_input("Item Name")
        owner_in = c3.selectbox("Owner", ["Hossam Atta", "Omar Fathy", "Mokhtar Mostafa"])
        
        c4, c5, c6 = st.columns(3)
        cat_in = c4.selectbox("Category", ["Engineering", "Procurement"])
        stat_in = c5.selectbox("Status", ["Pending", "In Progress", "Technical Evaluation", "Completed"])
        due_in = c6.date_input("Due Date")
        
        prog_in = st.slider("Progress", 0, 100, 0)
        
        if st.form_submit_button("Submit to System"):
            new_data = {"ID": id_in, "Category": cat_in, "Item": item_in, "Owner": owner_in, "Status": stat_in, "Due Date": pd.to_datetime(due_in), "Progress": prog_in}
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_data])], ignore_index=True)
            st.rerun()

st.markdown('<div class="footer">Elsewedy Electric | Morjan Station | EPC Control v2.1</div>', unsafe_allow_html=True)
