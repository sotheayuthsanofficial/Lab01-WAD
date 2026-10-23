import streamlit as st
import pandas as pd
import plotly.express as px

# =============================================================
# PAGE CONFIG
# =============================================================
st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# THEME / STYLING
# =============================================================
PRIMARY = "#0F9D77"      # teal accent
NAVY = "#132A3A"         # deep navy
NAVY_LIGHT = "#1F3A4D"
RISK_COLORS = {"Low Risk": "#15803D", "Medium Risk": "#A16207", "High Risk": "#B91C1C"}
RISK_BG = {"Low Risk": "#DCFCE7", "Medium Risk": "#FEF9C3", "High Risk": "#FEE2E2"}

# The font import must be the first thing inside <style>
font_import = "@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');"

# Python colors are sent to CSS as variables, so the CSS below can use var(--navy) etc.
color_variables = (
    ":root { --primary: " + PRIMARY + "; --navy: " + NAVY + "; --navy-light: " + NAVY_LIGHT + "; }"
)

page_css = """
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.block-container {
    padding-top: 1.6rem;
}

/* ---- Header banner ---- */
.edurisk-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 55%, var(--primary) 150%);
    color: #FFFFFF;
    padding: 1.8rem 2rem;
    border-radius: 18px;
    margin-bottom: 1.6rem;
    box-shadow: 0 8px 24px rgba(19, 42, 58, 0.25);
}
.edurisk-header h1 {
    margin: 0 0 0.3rem 0;
    font-size: 2rem;
    font-weight: 700;
}
.edurisk-header p {
    margin: 0;
    opacity: 0.88;
    font-size: 1.02rem;
}

/* ---- KPI cards ---- */
.kpi-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.1rem 1.1rem 0.9rem 1.1rem;
    box-shadow: 0 2px 14px rgba(16, 24, 40, 0.3);
    border-left: 5px solid var(--accent, var(--primary));
    height: 100%;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--navy);
    margin-top: 0.15rem;
}
.kpi-label {
    font-size: 0.78rem;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}

/* ---- Risk badge ---- */
.risk-badge {
    padding: 4px 14px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.95rem;
    display: inline-block;
}

/* ---- Feature card (Home page) ---- */
.feature-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.2rem;
    box-shadow: 0 2px 14px rgba(16, 24, 40, 0.3);
    text-align: center;
    height: 100%;
}
.feature-card h4 { margin: 0.5rem 0 0.3rem 0; color: var(--navy); }
.feature-card p { color: #6B7280; font-size: 0.88rem; margin: 0; }

/* ---- Tool card (About page only) ---- */
.tool-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 0.9rem 0.5rem;
    box-shadow: 0 2px 8px rgba(16, 24, 40, 0.3);
    text-align: center;
    margin-bottom: 1.5rem;
}
.tool-name {
    color: var(--navy);
    font-weight: 600;
    font-size: 0.95rem;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy) 0%, var(--navy-light) 100%);
}
section[data-testid="stSidebar"] * {
    color: #F1F5F9 !important;
}
section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.35rem;
}
section[data-testid="stSidebar"] label {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.45rem 0.6rem;
    margin-bottom: 0.15rem;
}

/* ---- Buttons ---- */
.stButton button, .stDownloadButton button {
    background: var(--primary);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: var(--navy);
    color: white;
}

footer {visibility: hidden;}
"""

st.markdown(
    "<style>" + font_import + color_variables + page_css + "</style>",
    unsafe_allow_html=True,
)


def header(title, subtitle):
    st.markdown(
        '<div class="edurisk-header">'
        "<h1>" + title + "</h1>"
        "<p>" + subtitle + "</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def kpi_card(label, value, accent=PRIMARY):
    st.markdown(
        '<div class="kpi-card" style="--accent:' + accent + ';">'
        '<div class="kpi-value">' + str(value) + "</div>"
        '<div class="kpi-label">' + label + "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def risk_badge(risk):
    return (
        '<span class="risk-badge" style="background:' + RISK_BG[risk] + ";"
        "color:" + RISK_COLORS[risk] + ';">' + risk + "</span>"
    )


def style_risk_table(df):
    def highlight(val):
        if val in RISK_COLORS:
            return "background-color:" + RISK_BG[val] + ";color:" + RISK_COLORS[val] + ";font-weight:600;"
        return ""
    styler = df.style
    # pandas >= 2.1 renamed Styler.applymap to Styler.map; support both.
    apply_fn = getattr(styler, "map", None) or styler.applymap
    return apply_fn(highlight, subset=["Risk Level"])


# =============================================================
# DATA
# =============================================================
def load_students_data():
    try:
        # students.csv must be in the same folder where you run streamlit
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()


students_df = load_students_data()


def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"


students_df["Risk Level"] = students_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

# =============================================================
# SIDEBAR NAVIGATION
# =============================================================
with st.sidebar:
    st.markdown(
        "<div style='text-align:center; padding: 0.4rem 0 1rem 0;'>"
        "<div style='font-weight:700; font-size:1.1rem;'>EduRisk Menu</div>"
        "<div style='font-size:0.78rem; opacity:0.75;'>Student Risk Monitoring</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"],
        label_visibility="collapsed",
    )

    st.markdown("----------------------------------")
    st.markdown("----------------------------------")
    st.markdown("----------------------------------")
    st.markdown("----------------------------------")
    st.markdown("----------------------------------")
    st.caption("Web App Development for Data Science")

# =============================================================
# HOME
# =============================================================
if selected_page == "Home":
    header(
        "EduRisk Analytics",
        "Frontend Prototype with CSV Data Loading",
    )
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads Student Data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )
    st.success("Lab 03 app is running successfully!")

    st.markdown("####")
    c1, c2, c3 = st.columns(3)
    with c1:
            st.markdown(
            """<div class="feature-card">
            <h4>Interactive Dashboard</h4>
            <p>Filter students by course, risk level, attendance, and score.</p>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
            st.markdown(
                """<div class="feature-card">
                <h4>Risk Checker</h4>
                <p>Enter one student's score and attendance to get an instant risk result.</p>
                </div>""",
                unsafe_allow_html=True,
        )
    with c3:
            st.markdown(
                """<div class="feature-card">
                <h4>Export Data</h4>
                <p>Download the filtered dataset as a CSV file for further analysis.</p>
                </div>""",
                unsafe_allow_html=True,
            )

# =============================================================
# DASHBOARD
# =============================================================
elif selected_page == "Dashboard":
    header(
        "Dashboard Prototype",
        "This dashboard gives a quick overview of student performance using data loaded from students.csv.",
    )

    with st.container(border=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            selected_course = st.selectbox(
                "Select Course",
                ["All"] + list(students_df["Course"].unique())
            )
        with f2:
            selected_risk = st.selectbox(
                "Select Risk Level",
                ["All", "Low Risk", "Medium Risk", "High Risk"]
            )
        with f3:
            min_attendance = st.slider("Minimum Attendance", 0, 100, 0)
        with f4:
            min_score = st.slider("Minimum Score", 0, 100, 0)

    filtered_df = students_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]

    total_students = len(filtered_df)

    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    else:
        average_score = 0
        average_attendance = 0

    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    tab_overview, tab_data, tab_charts = st.tabs(["Overview", "Data Table", "Charts"])

    with tab_overview:
        st.markdown("##### Dashboard Metrics")
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            kpi_card("Students", total_students, PRIMARY)
        with k2:
            kpi_card("Average Score", round(average_score, 2), "#2563EB")
        with k3:
            kpi_card("Average Attendance", str(round(average_attendance, 2)) + "%", "#7C3AED")
        with k4:
            kpi_card("High Risk", high_risk_students, "#B91C1C")

    with tab_data:
        show_data = st.checkbox("Show Filtered Dataset", True)

        if show_data:
            st.markdown("##### Student Records")
            st.write("This table shows Student Data loaded from students.csv.")
            if len(filtered_df) > 0:
                st.dataframe(style_risk_table(filtered_df), width="stretch")
            else:
                st.warning("No students match the current filters.")

            csv = filtered_df.to_csv(index=False)

            st.download_button(
                label="Download Filtered Data",
                data=csv,
                file_name="filtered_student_data.csv",
                mime="text/csv"
            )
        else:
            st.info("Filtered dataset is hidden.")

    with tab_charts:
        st.markdown("##### Charts")
        chart_col1, chart_col2, chart_col3 = st.columns(3)

        with chart_col1:
            st.markdown("**Student Scores**")
            if len(filtered_df) > 0:
                fig_score = px.bar(
                    filtered_df.sort_values("Score", ascending=False),
                    x="Student Name", y="Score", color="Risk Level",
                    color_discrete_map=RISK_COLORS,
                    text="Score",
                )
                fig_score.add_hline(y=60, line_dash="dot", line_color="#B91C1C", opacity=0.5)
                fig_score.add_hline(y=75, line_dash="dot", line_color="#A16207", opacity=0.5)
                fig_score.update_layout(
                    plot_bgcolor="white", margin=dict(t=10, b=10, l=10, r=10), height=360,
                    legend_title_text="Risk Level",
                )
                st.plotly_chart(fig_score, width="stretch")
            else:
                st.warning("No data available for score chart.")

        with chart_col2:
            st.markdown("**Risk Level Distribution**")
            if len(filtered_df) > 0:
                risk_count = filtered_df["Risk Level"].value_counts().reset_index()
                risk_count.columns = ["Risk Level", "Count"]
                fig_risk = px.pie(
                    risk_count, names="Risk Level", values="Count", hole=0.55,
                    color="Risk Level", color_discrete_map=RISK_COLORS,
                )
                fig_risk.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=360)
                st.plotly_chart(fig_risk, width="stretch")
            else:
                st.warning("No data available for risk chart.")

        # New in Lab 03: course count chart
        with chart_col3:
            st.markdown("**Course Count**")
            if len(filtered_df) > 0:
                course_count = filtered_df["Course"].value_counts().reset_index()
                course_count.columns = ["Course", "Count"]
                fig_course = px.bar(
                    course_count, x="Course", y="Count", text="Count",
                    color_discrete_sequence=[PRIMARY],
                )
                fig_course.update_layout(
                    plot_bgcolor="white", margin=dict(t=10, b=10, l=10, r=10), height=360,
                )
                st.plotly_chart(fig_course, width="stretch")
            else:
                st.warning("No data available for course chart.")

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )

# =============================================================
# Student Data
# =============================================================
elif selected_page == "Student Data":
    header("Student Data", "This page displays and inspects the dataset loaded from students.csv.")

    total_students = len(students_df)
    average_score = students_df["Score"].mean()
    average_attendance = students_df["Attendance"].mean()
    high_risk_students = students_df[
        students_df["Risk Level"] == "High Risk"
    ].shape[0]

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Total Students", total_students, PRIMARY)
    with k2:
        kpi_card("Average Score", round(average_score, 2), "#2563EB")
    with k3:
        kpi_card("Average Attendance", str(round(average_attendance, 2)) + "%", "#7C3AED")
    with k4:
        kpi_card("High Risk Students", high_risk_students, "#B91C1C")

    # New in Lab 03: data inspection
    st.markdown("####")
    st.markdown("##### Data Inspection")
    st.write("Rows and Columns:", students_df.shape)
    st.write("Column Names:")
    st.write(students_df.columns.tolist())
    st.write("First 5 Rows:")
    st.dataframe(style_risk_table(students_df.head()), width="stretch")

    st.markdown("####")
    st.markdown("##### Full Student Dataset")
    search = st.text_input("Search by Student Name", "")
    display_df = students_df.copy()
    if search:
        display_df = display_df[display_df["Student Name"].str.contains(search, case=False)]
    st.dataframe(style_risk_table(display_df), width="stretch")

    st.markdown(
        "**Legend:** " + risk_badge("Low Risk") + " &nbsp; "
        + risk_badge("Medium Risk") + " &nbsp; " + risk_badge("High Risk"),
        unsafe_allow_html=True,
    )

# =============================================================
# RISK CHECKER
# =============================================================
elif selected_page == "Risk Checker":
    header("Single Student Risk Checker", "Enter a score and attendance to check the risk level.")

    left, right = st.columns([1, 1])

    with left:
        with st.container(border=True):
            with st.form("risk_checker_form"):
                input_name = st.text_input("Student Name")
                input_score = st.number_input("Score", 0, 100, 50)
                input_attendance = st.number_input("Attendance", 0, 100, 50)
                submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        with right:
            with st.container(border=True):
                st.markdown("#### Result for **" + (input_name or "Student") + "**")
                st.markdown(risk_badge(risk_result), unsafe_allow_html=True)
                st.write("")
                st.write("Score")
                st.progress(int(input_score))
                st.caption(str(input_score) + " / 100")
                st.write("Attendance")
                st.progress(int(input_attendance))
                st.caption(str(input_attendance) + " / 100")

                st.write("")
                if risk_result == "Low Risk":
                    st.success("Risk Level: Low Risk")
                elif risk_result == "Medium Risk":
                    st.warning("Risk Level: Medium Risk")
                else:
                    st.error("Risk Level: High Risk")

# =============================================================
# ABOUT
# =============================================================
else:
    header("About", "Project and course information.")
    st.write("This app is part of Lab 03.")
    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.write("**Course:** Web App Development for Data Science")
        st.write("**Project Theme:** EduRisk Analytics")
        st.write("**Topic:** Data Loading, Layout, and Frontend Prototype")

        st.markdown("##### Tools Used")
        t1, t2, t3, t4 = st.columns(4)
        for col, name in zip((t1, t2, t3, t4), [
            "Python", "Streamlit", "Pandas", "Plotly"
        ]):
            with col:
                st.markdown(
                    "<div class='tool-card'>"
                    "<div class='tool-name'>" + name + "</div></div>",
                    unsafe_allow_html=True,
                )

    st.info(
        "This frontend prototype loads real data from students.csv "
        "and displays it using Streamlit and Pandas."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )