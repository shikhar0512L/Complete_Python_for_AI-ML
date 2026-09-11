# created by Anthropic's Claude AI
import json
import streamlit as st
from abc import ABC, abstractmethod
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SchoolOS",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --ink: #0f0f0f;
    --cream: #f5f0e8;
    --accent: #e8572a;
    --accent2: #2a7ae8;
    --muted: #8a8680;
    --card: #ffffff;
    --border: #e2ddd6;
    --success: #2d9e6b;
    --danger: #d94040;
    --shadow-sm: 0 1px 2px rgba(15,15,15,0.04);
    --shadow-md: 0 4px 12px rgba(15,15,15,0.06);
    --shadow-lg: 0 12px 32px rgba(15,15,15,0.10);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem !important; padding-bottom: 4rem !important; max-width: 1400px;}

/* ─── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--ink) !important;
    border-right: none;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] * {
    color: var(--cream) !important;
}
[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
[data-testid="stSidebar"] [data-baseweb="radio"] {
    gap: 0.2rem;
}
[data-testid="stSidebar"] [data-baseweb="radio"] > div {
    padding: 0.55rem 0.9rem;
    border-radius: 8px;
    transition: background 0.15s;
    cursor: pointer;
}
[data-testid="stSidebar"] [data-baseweb="radio"] > div:hover {
    background: rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] [data-baseweb="radio"] label {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    cursor: pointer;
}

/* ─── Sidebar brand ───────────────────────────────────────────────────── */
.sb-brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.7rem;
    letter-spacing: -0.03em;
    line-height: 1;
    color: #ffffff !important;
}
.sb-brand-sub {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    opacity: 0.45;
    margin-top: 0.35rem;
}
.sb-stat {
    font-size: 0.72rem;
    opacity: 0.45;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    line-height: 1.8;
}
.sb-stat b { color: var(--accent); opacity: 1; }

/* ─── Hero banner (dark) with white "School" + orange "OS" ───────────── */
.hero-banner {
    background: linear-gradient(135deg, #0f0f0f 0%, #1c1c1c 100%);
    border-radius: 18px;
    padding: 2rem 2.2rem 1.6rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(232,87,42,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.main-header {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.9rem;
    letter-spacing: -0.035em;
    line-height: 1;
    color: #ffffff !important;
    margin-bottom: 0;
}
.main-sub {
    font-family: 'DM Sans', sans-serif;
    font-weight: 400;
    color: #a8a29a !important;
    font-size: 0.78rem;
    margin-top: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.accent-dot {
    color: #e8572a !important;
}
.hero-rule {
    border: none;
    border-top: 2px solid #e8572a;
    margin: 1.3rem 0 0 0;
    width: 60px;
    opacity: 0.9;
}

/* ─── Section title ───────────────────────────────────────────────────── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    letter-spacing: -0.01em;
    border-left: 4px solid var(--accent);
    padding-left: 0.85rem;
    margin-bottom: 1.25rem;
    color: var(--ink);
}

/* ─── Stat cards ──────────────────────────────────────────────────────── */
.stat-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    box-shadow: var(--shadow-sm);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0;
    transition: opacity 0.2s;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: #d4cec5;
}
.stat-card:hover::before { opacity: 1; }

.stat-number {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    line-height: 1;
    color: var(--ink);
    letter-spacing: -0.02em;
}
.stat-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    font-weight: 500;
}
.stat-icon {
    position: absolute;
    top: 1.2rem;
    right: 1.3rem;
    font-size: 1.3rem;
    opacity: 0.35;
}

/* ─── Person cards ───────────────────────────────────────────────────── */
.person-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    transition: border-color 0.15s, background 0.15s;
}
.person-card:hover {
    border-color: #c9c2b6;
    background: #fdfbf8;
}
.person-name {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.02rem;
    color: var(--ink);
}
.person-meta {
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 0.15rem;
}

/* ─── Badges ──────────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    white-space: nowrap;
}
.badge-student { background: #fff3ee; color: var(--accent); border: 1px solid #f5c9b8; }
.badge-teacher { background: #eef3ff; color: var(--accent2); border: 1px solid #b8c8f5; }
.badge-avg     { background: #eefaf4; color: var(--success); border: 1px solid #b8e8d0; }
.badge-muted   { background: #f5f0e8; color: var(--muted); border: 1px solid var(--border); }

/* ─── Divider ─────────────────────────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1.5px solid var(--border);
    margin: 1.8rem 0;
}

/* ─── Forms ───────────────────────────────────────────────────────────── */
[data-testid="stForm"] {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.2rem 1.8rem;
    box-shadow: var(--shadow-sm);
}
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
}
.stTextInput input, .stNumberInput input {
    border-radius: 9px !important;
    border: 1.5px solid var(--border) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0.8rem !important;
    background: #fdfcfa !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(232,87,42,0.10) !important;
    background: #fff !important;
}
.stSelectbox > div > div {
    border-radius: 9px !important;
    border: 1.5px solid var(--border) !important;
    background: #fdfcfa !important;
}

/* ─── Buttons ─────────────────────────────────────────────────────────── */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    background: var(--ink) !important;
    color: var(--cream) !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.65rem 1.8rem !important;
    transition: background 0.18s, transform 0.1s !important;
    box-shadow: var(--shadow-sm) !important;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: var(--accent) !important;
    transform: translateY(-1px);
    box-shadow: var(--shadow-md) !important;
}
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0);
}

/* ─── Messages ────────────────────────────────────────────────────────── */
.msg-success, .msg-error, .msg-info {
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    font-weight: 500;
    font-size: 0.9rem;
    margin: 0.9rem 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.msg-success { background: #eefaf4; border-left: 4px solid var(--success); color: #1a6b47; }
.msg-error   { background: #fff0f0; border-left: 4px solid var(--danger);  color: #8b1f1f; }
.msg-info    { background: #eef3ff; border-left: 4px solid var(--accent2); color: #1a3d7a; }

/* ─── Empty state ─────────────────────────────────────────────────────── */
.empty-state {
    background: #fdfcfa;
    border: 1.5px dashed var(--border);
    border-radius: 14px;
    padding: 2.2rem 1.5rem;
    text-align: center;
    color: var(--muted);
}
.empty-icon { font-size: 2rem; opacity: 0.5; margin-bottom: 0.5rem; }
.empty-text { font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)


# ─── Data Layer ─────────────────────────────────────────────────────────────
DATABASE = "school_data.json"

def load_data():
    p = Path(DATABASE)
    if p.exists():
        content = p.read_text()
        if content.strip():
            return json.loads(content)
    return {"students": [], "teachers": []}

def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

def validate_email(email):
    return "@" in email and "." in email

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


# ─── Helper: page header (dark banner with white + orange) ─────────────────
def page_header(title_html, subtitle):
    st.markdown(f"""
    <div class='hero-banner'>
        <div class='main-header'>{title_html}</div>
        <div class='main-sub'>{subtitle}</div>
        <hr class='hero-rule'>
    </div>
    """, unsafe_allow_html=True)

def person_row(name, meta, badge_text, badge_class):
    return f"""
    <div class='person-card'>
        <div>
            <div class='person-name'>{name}</div>
            <div class='person-meta'>{meta}</div>
        </div>
        <span class='badge {badge_class}'>{badge_text}</span>
    </div>"""

def empty_state(icon, text):
    return f"""
    <div class='empty-state'>
        <div class='empty-icon'>{icon}</div>
        <div class='empty-text'>{text}</div>
    </div>"""


# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0.5rem 1.8rem 0.5rem;'>
        <div class='sb-brand'>School<span style='color:#e8572a;'>OS</span></div>
        <div class='sb-brand-sub'>Management System</div>
    </div>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "Navigation",
        ["Dashboard", "Register Student", "Register Teacher",
         "Add Grade", "Student Details", "Teacher Details"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: #2a2a2a; margin: 2rem 0 1.5rem;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='sb-stat'>
        <b>{len(data['students'])}</b> Students<br>
        <b>{len(data['teachers'])}</b> Teachers<br>
        <b>{sum(len(s['grades']) for s in data['students'])}</b> Grades
    </div>
    """, unsafe_allow_html=True)


# ─── DASHBOARD ──────────────────────────────────────────────────────────────
if nav == "Dashboard":
    page_header(
        "School<span class='accent-dot'>OS</span>",
        "Management System · Overview"
    )

    col1, col2, col3, col4 = st.columns(4)
    all_grades = [m for s in data['students'] for m in s['grades'].values()]
    avg_school = sum(all_grades) / len(all_grades) if all_grades else 0

    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <span class='stat-icon'>🎓</span>
            <div class='stat-number'>{len(data['students'])}</div>
            <div class='stat-label'>Students</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <span class='stat-icon'>👨‍🏫</span>
            <div class='stat-number'>{len(data['teachers'])}</div>
            <div class='stat-label'>Teachers</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        total_grades = sum(len(s['grades']) for s in data['students'])
        st.markdown(f"""
        <div class='stat-card'>
            <span class='stat-icon'>📝</span>
            <div class='stat-number'>{total_grades}</div>
            <div class='stat-label'>Grades Recorded</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='stat-card'>
            <span class='stat-icon'>📊</span>
            <div class='stat-number' style='color:#e8572a;'>{avg_school:.1f}</div>
            <div class='stat-label'>School Average</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:2.2rem;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<div class='section-title'>Recent Students</div>", unsafe_allow_html=True)
        if data['students']:
            for s in data['students'][-5:][::-1]:
                grades = s['grades']
                avg = sum(grades.values()) / len(grades) if grades else None
                avg_txt = f"avg {avg:.1f}" if avg is not None else "no grades"
                st.markdown(person_row(
                    s['name'],
                    f"Roll #{s['roll_no']} · Age {s['age']}",
                    avg_txt,
                    "badge-avg" if avg is not None else "badge-muted"
                ), unsafe_allow_html=True)
        else:
            st.markdown(empty_state("🎓", "No students registered yet."), unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='section-title'>Faculty</div>", unsafe_allow_html=True)
        if data['teachers']:
            for t in data['teachers'][-5:][::-1]:
                st.markdown(person_row(
                    t['name'],
                    f"ID: {t['emp_id']} · Age {t['age']}",
                    t['subject'],
                    "badge-teacher"
                ), unsafe_allow_html=True)
        else:
            st.markdown(empty_state("👨‍🏫", "No teachers registered yet."), unsafe_allow_html=True)


# ─── REGISTER STUDENT ───────────────────────────────────────────────────────
elif nav == "Register Student":
    page_header(
        "Register <span class='accent-dot'>Student</span>",
        "Add a new student to the system"
    )

    with st.form("reg_student"):
        st.markdown("<div class='section-title'>Student Information</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            email = st.text_input("Email Address", placeholder="e.g. rahul@school.edu")
        with c2:
            age = st.number_input("Age", min_value=5, max_value=30, value=16)
            roll_no = st.text_input("Roll Number", placeholder="e.g. 101")

        submitted = st.form_submit_button("Register Student →", use_container_width=True)

    if submitted:
        if not name or not email or not roll_no:
            st.markdown("<div class='msg-error'>⚠ Please fill in all fields.</div>", unsafe_allow_html=True)
        elif not validate_email(email):
            st.markdown("<div class='msg-error'>⚠ Invalid email address.</div>", unsafe_allow_html=True)
        elif any(s['roll_no'] == roll_no for s in data['students']):
            st.markdown("<div class='msg-error'>⚠ A student with this roll number already exists.</div>", unsafe_allow_html=True)
        else:
            data['students'].append({
                "name": name, "age": age,
                "email": email, "roll_no": roll_no, "grades": {}
            })
            save_data(data)
            st.markdown(f"<div class='msg-success'>✓ <b>{name}</b> has been registered successfully.</div>", unsafe_allow_html=True)


# ─── REGISTER TEACHER ───────────────────────────────────────────────────────
elif nav == "Register Teacher":
    page_header(
        "Register <span class='accent-dot'>Teacher</span>",
        "Add a new teacher to the system"
    )

    with st.form("reg_teacher"):
        st.markdown("<div class='section-title'>Teacher Information</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name", placeholder="e.g. Priya Verma")
            email = st.text_input("Email Address", placeholder="e.g. priya@school.edu")
            subject = st.text_input("Subject", placeholder="e.g. Mathematics")
        with c2:
            age = st.number_input("Age", min_value=21, max_value=70, value=35)
            emp_id = st.text_input("Employee ID", placeholder="e.g. T-201")

        submitted = st.form_submit_button("Register Teacher →", use_container_width=True)

    if submitted:
        if not name or not email or not emp_id or not subject:
            st.markdown("<div class='msg-error'>⚠ Please fill in all fields.</div>", unsafe_allow_html=True)
        elif not validate_email(email):
            st.markdown("<div class='msg-error'>⚠ Invalid email address.</div>", unsafe_allow_html=True)
        elif any(t['emp_id'] == emp_id for t in data['teachers']):
            st.markdown("<div class='msg-error'>⚠ A teacher with this Employee ID already exists.</div>", unsafe_allow_html=True)
        else:
            data['teachers'].append({
                "name": name, "age": age,
                "email": email, "subject": subject, "emp_id": emp_id
            })
            save_data(data)
            st.markdown(f"<div class='msg-success'>✓ <b>{name}</b> has been registered successfully.</div>", unsafe_allow_html=True)


# ─── ADD GRADE ──────────────────────────────────────────────────────────────
elif nav == "Add Grade":
    page_header(
        "Add <span class='accent-dot'>Grade</span>",
        "Record a subject score for a student"
    )

    if not data['students']:
        st.markdown("<div class='msg-error'>⚠ No students registered yet. Register a student first.</div>", unsafe_allow_html=True)
    else:
        student_options = {f"{s['name']} (Roll #{s['roll_no']})": s['roll_no'] for s in data['students']}

        with st.form("add_grade"):
            st.markdown("<div class='section-title'>Grade Entry</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                selected = st.selectbox("Select Student", list(student_options.keys()))
            with c2:
                subject = st.text_input("Subject", placeholder="e.g. Physics")
            with c3:
                marks = st.number_input("Marks", min_value=0.0, max_value=100.0, value=75.0, step=0.5)

            submitted = st.form_submit_button("Save Grade →", use_container_width=True)

        if submitted:
            if not subject:
                st.markdown("<div class='msg-error'>⚠ Subject name is required.</div>", unsafe_allow_html=True)
            else:
                roll_no = student_options[selected]
                for s in data['students']:
                    if s['roll_no'] == roll_no:
                        s['grades'][subject] = marks
                        save_data(data)
                        st.markdown(f"<div class='msg-success'>✓ Grade saved — <b>{subject}: {marks}</b></div>", unsafe_allow_html=True)
                        break


# ─── STUDENT DETAILS ────────────────────────────────────────────────────────
elif nav == "Student Details":
    page_header(
        "Student <span class='accent-dot'>Details</span>",
        "View a student's profile and grades"
    )

    if not data['students']:
        st.markdown(empty_state("🎓", "No students registered yet."), unsafe_allow_html=True)
    else:
        student_options = {f"{s['name']} (Roll #{s['roll_no']})": s for s in data['students']}
        selected = st.selectbox("Select Student", list(student_options.keys()))
        s = student_options[selected]
        grades = s['grades']
        avg = sum(grades.values()) / len(grades) if grades else 0

        st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='stat-card'>
                <span class='stat-icon'>👤</span>
                <div class='stat-number' style='font-size:1.6rem;'>{s['name']}</div>
                <div class='stat-label'>Full Name</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='stat-card'>
                <span class='stat-icon'>🆔</span>
                <div class='stat-number'>{s['roll_no']}</div>
                <div class='stat-label'>Roll Number</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='stat-card'>
                <span class='stat-icon'>🎂</span>
                <div class='stat-number'>{s['age']}</div>
                <div class='stat-label'>Age</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='stat-card'>
                <span class='stat-icon'>📈</span>
                <div class='stat-number' style='color:#e8572a;'>{avg:.1f}</div>
                <div class='stat-label'>Average Score</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1.6rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.85rem; color:#8a8680; padding-left:0.2rem;'>📧 {s['email']}</div>", unsafe_allow_html=True)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Grades</div>", unsafe_allow_html=True)
        if grades:
            cols = st.columns(min(len(grades), 4))
            for idx, (subj, score) in enumerate(grades.items()):
                with cols[idx % 4]:
                    color = "#2d9e6b" if score >= 75 else "#e8572a" if score < 50 else "#2a7ae8"
                    st.markdown(f"""
                    <div class='stat-card' style='text-align:center;'>
                        <div class='stat-number' style='color:{color}; font-size:2.2rem;'>{score:.0f}</div>
                        <div class='stat-label'>{subj}</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.markdown(empty_state("📝", "No grades recorded yet."), unsafe_allow_html=True)


# ─── TEACHER DETAILS ────────────────────────────────────────────────────────
elif nav == "Teacher Details":
    page_header(
        "Teacher <span class='accent-dot'>Details</span>",
        "View a teacher's profile"
    )

    if not data['teachers']:
        st.markdown(empty_state("👨‍🏫", "No teachers registered yet."), unsafe_allow_html=True)
    else:
        teacher_options = {f"{t['name']} — {t['subject']}": t for t in data['teachers']}
        selected = st.selectbox("Select Teacher", list(teacher_options.keys()))
        t = teacher_options[selected]

        st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='stat-card'>
                <span class='stat-icon'>👤</span>
                <div class='stat-number' style='font-size:1.6rem;'>{t['name']}</div>
                <div class='stat-label'>Full Name</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='stat-card'>
                <span class='stat-icon'>🆔</span>
                <div class='stat-number'>{t['emp_id']}</div>
                <div class='stat-label'>Employee ID</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='stat-card'>
                <span class='stat-icon'>🎂</span>
                <div class='stat-number'>{t['age']}</div>
                <div class='stat-label'>Age</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='stat-card'>
                <span class='stat-icon'>📚</span>
                <div class='stat-number' style='font-size:1.35rem; color:#2a7ae8;'>{t['subject']}</div>
                <div class='stat-label'>Subject</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1.4rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.85rem; color:#8a8680; padding-left:0.2rem;'>📧 {t['email']}</div>", unsafe_allow_html=True)