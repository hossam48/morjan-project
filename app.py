import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, date

# --- 1. إعدادات الصفحة والستايل ---
st.set_page_config(
    page_title="AlGhat Project Control | Elsewedy Electric",
    page_icon="🏗️",
    layout="wide"
)

# ستايل احترافي بتدرجات زرقاء وهوية هندسية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    .main { background-color: #f4f7f9; }
    [data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-bottom: 4px solid #005a9c;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #e1e8ed;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #005a9c !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعداد الاتصال بقاعدة البيانات (Google Sheets) ---
# استبدل الرابط أدناه برابط ملف Google Sheets الخاص بك
URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit#gid=0"

def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=URL, ttl="1m")
        
        # تنظيف البيانات ومعالجة أعمدة ملف ALGHAT
        # إزالة العلامات الغريبة مثل (*) من التواريخ وتحويلها
        if 'Finish' in df.columns:
            df['Finish'] = df['Finish'].astype(str).str.replace('*', '', regex=False)
            df['Finish'] = pd.to_datetime(df['Finish'], errors='coerce').dt.date
        if 'Start' in df.columns:
            df['Start'] = pd.to_datetime(df['Start'], errors='coerce').dt.date
            
        # إضافة أعمدة الإدارة إذا لم تكن موجودة في الإكسل الأصلي
        if 'Owner' not in df.columns: df['Owner'] = 'Unassigned'
        if 'Status' not in df.columns: df['Status'] = 'Not Started'
        if 'Progress' not in df.columns: df['Progress'] = 0
        
        # التأكد من تنسيق الأرقام
        df['Progress'] = pd.to_numeric(df['Progress'], errors='coerce').fillna(0).astype(int)
        df['Original Duration'] = pd.to_numeric(df['Original Duration'], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"⚠️ فشل الاتصال بـ Google Sheets: {e}")
        return pd.DataFrame()

def save_data(df):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(spreadsheet=URL, data=df)
        st.success("✅ تم تحديث ملف Google Sheets بنجاح!")
    except Exception as e:
        st.error(f"❌ خطأ أثناء الحفظ: {e}")

# --- 3. تهيئة الحالة ---
if 'master_df' not in st.session_state:
    st.session_state.master_df = load_data()

# --- 4. الشريط الجانبي (Sidebar) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b2/Elsewedy_Electric_Logo.png", width=180)
    st.title("لوحة التحكم")
    st.markdown("---")
    
    if st.button("🔄 تحديث البيانات من السحابة", use_container_width=True):
        st.session_state.master_df = load_data()
        st.rerun()
    
    st.markdown("### ملخص المشروع")
    total_activities = len(st.session_state.master_df)
    avg_progress = st.session_state.master_df['Progress'].mean() if total_activities > 0 else 0
    st.write(f"🔢 إجمالي الأنشطة: **{total_activities}**")
    st.write(f"📈 نسبة الإنجاز الكلية: **{avg_progress:.1f}%**")

# --- 5. الهيدر الرئيسي ---
st.markdown(f"""
    <div style='background: linear-gradient(135deg, #005a9c 0%, #002d4e 100%); 
                padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;'>
        <h1 style='margin:0; color: white;'>🏗️ ALGHAT Project Control Center</h1>
        <p style='margin:10px 0 0 0; opacity: 0.9; font-size: 1.1em;'>
            نظام التحكم الهندسي ومتابعة الجدول الزمني - السويدي إليكتريك
        </p>
    </div>
""", unsafe_allow_html=True)

# --- 6. التبويبات (Tabs) ---
tab_dash, tab_mdl, tab_gantt = st.tabs([
    "📊 لوحة التحليلات (Analytics)", 
    "📋 قائمة المهام (MDL & Editor)", 
    "🗓️ المخطط الزمني (Gantt Chart)"
])

# --- Tab 1: Analytics ---
with tab_dash:
    df = st.session_state.master_df
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        # مقاييس سريعة
        col1.metric("إجمالي المهام", len(df))
        col2.metric("متوسط الإنجاز", f"{avg_progress:.1f}%")
        
        # حساب المهام المتأخرة (تاريخ النهاية قبل اليوم والنسبة أقل من 100)
        overdue = df[(df['Finish'] < date.today()) & (df['Progress'] < 100)]
        col3.metric("مهام متأخرة", len(overdue), delta="- Needs Action", delta_color="inverse")
        
        completed = len(df[df['Progress'] == 100])
        col4.metric("مهام مكتملة", completed)
        
        st.markdown("---")
        
        c_left, c_right = st.columns(2)
        with c_left:
            # توزيع المهام حسب الحالة
            fig_status = px.pie(df, names='Status', title="توزيع المهام حسب الحالة", hole=0.4,
                               color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_status, use_container_width=True)
            
        with c_right:
            # أفضل أداء للمهندسين
            owner_perf = df.groupby('Owner')['Progress'].mean().reset_index()
            fig_perf = px.bar(owner_perf, x='Owner', y='Progress', title="أداء الفريق (متوسط الإنجاز %)",
                             color='Progress', color_continuous_scale='Blues')
            st.plotly_chart(fig_perf, use_container_width=True)

# --- Tab 2: MDL & Editor ---
with tab_mdl:
    st.subheader("📝 محرر بيانات المشروع (Live Editor)")
    st.info("يمكنك تعديل النسب (Progress)، المهندس المسؤول (Owner)، والحالة مباشرة من الجدول أدناه:")
    
    # فلترة البحث
    search_query = st.text_input("🔍 ابحث برقم النشاط أو الاسم (Activity ID / Name)")
    filtered_df = st.session_state.master_df
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Activity ID'].astype(str).str.contains(search_query, case=False) | 
            filtered_df['Activity Name'].astype(str).str.contains(search_query, case=False)
        ]

    # عرض محرر البيانات
    edited_df = st.data_editor(
        filtered_df,
        use_container_width=True,
        num_rows="dynamic",
        height=500,
        column_config={
            "Progress": st.column_config.ProgressColumn("نسبة الإنجاز", min_value=0, max_value=100, format="%d%%"),
            "Status": st.column_config.SelectboxColumn("الحالة", options=["Not Started", "In Progress", "Submitted", "Approved", "Completed"]),
            "Finish": st.column_config.DateColumn("تاريخ الانتهاء"),
            "Start": st.column_config.DateColumn("تاريخ البدء"),
            "Activity ID": st.column_config.Column("ID", disabled=True)
        },
        key="data_editor_key"
    )
    
    st.markdown("---")
    col_save, col_empty = st.columns([1, 4])
    with col_save:
        if st.button("💾 حفظ المزامنة مع Google Sheets", type="primary", use_container_width=True):
            # تحديث النسخة الأصلية بالتغييرات المفلترة
            st.session_state.master_df.update(edited_df)
            save_data(st.session_state.master_df)

# --- Tab 3: Gantt Chart ---
with tabs[2]:
    st.subheader("🕒 المخطط الزمني للمشروع (Gantt Chart)")
    gantt_df = st.session_state.master_df.dropna(subset=['Start', 'Finish']).copy()
    
    if not gantt_df.empty:
        # عرض أول 40 نشاط لضمان وضوح الرسم (يمكنك تغيير هذا)
        fig_gantt = px.timeline(
            gantt_df.head(40), 
            start="Start", 
            finish="Finish", 
            y="Activity Name", 
            color="Progress",
            title="Project Roadmap (Top 40 Activities)",
            hover_data=['Activity ID', 'Owner', 'Status'],
            color_continuous_scale='Viridis'
        )
        fig_gantt.update_yaxes(autorange="reversed") 
        st.plotly_chart(fig_gantt, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد تواريخ كافية (Start/Finish) لعرض المخطط الزمني.")

# --- Footer ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
    <center style='color: #6b7280; padding: 10px;'>
        <strong>Elsewedy Electric - Digital Transformation Unit</strong><br>
        <small>Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>
    </center>
""", unsafe_allow_html=True)
