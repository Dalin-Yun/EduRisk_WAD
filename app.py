# EduRisk Analytics — Student Performance & Risk Analysis

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="EduRisk Analytics | Lab 03",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# LOAD CSS
def load_css():
    css_path = Path(__file__).resolve().parent / "style.css"

    if css_path.is_file():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found: {css_path.name}. Using Streamlit's default styling.")

load_css()

# 2. LOAD STUDENT DATA
@st.cache_data
def load_student_data():
    csv_path = Path(__file__).resolve().parent / "students.csv"

    if not csv_path.is_file():
        st.error(f"Student data file not found: {csv_path.name}")
        st.stop()

    return pd.read_csv(csv_path)

student_df = load_student_data()

# 3. RISK LEVEL FUNCTION
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    return "Low Risk"

# Add risk level to dataset
required_columns = {"Student Name", "Score", "Attendance", "Course"}
missing_columns = required_columns.difference(student_df.columns)

if missing_columns:
    st.error("Missing required column(s) in students.csv: " + ", ".join(sorted(missing_columns)))
    st.stop()

student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1,
)

# Colour the Risk Level column in tables (CSS cannot style Streamlit's table cells)
def color_risk(value):
    colors = {
        "High Risk": "background-color:#FEE2E2; color:#991B1B",
        "Medium Risk": "background-color:#FEF3C7; color:#854D0E",
        "Low Risk": "background-color:#DCFCE7; color:#166534",
    }
    return colors.get(value, "")

def styled_table(df):
    return df.style.map(color_risk, subset=["Risk Level"]).hide(axis="index")

# Bar chart helper: Altair lets us set Times New Roman inside the chart
def bar_chart(data, x_col, y_col, color, angle=0):
    chart = (
        alt.Chart(data)
        .mark_bar(color=color, cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X(
                f"{x_col}:N",
                sort=None,
                title=None,
                axis=alt.Axis(labelAngle=angle, labelOverlap=False, labelLimit=200),
            ),
            y=alt.Y(f"{y_col}:Q", title=y_col, scale=alt.Scale(domainMin=0), axis=alt.Axis(tickMinStep=1)),
            tooltip=[alt.Tooltip(f"{x_col}:N"), alt.Tooltip(f"{y_col}:Q")],
        )
        .properties(height=300)
        .configure(font="Times New Roman")
        .configure_axis(
            labelFont="Times New Roman",
            titleFont="Times New Roman",
            labelFontSize=13,
            titleFontSize=14,
        )
    )
    return chart

# 4. SUMMARY STATISTICS
total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
high_risk_students = int((student_df["Risk Level"] == "High Risk").sum())

# 5. SIDEBAR NAVIGATION
# Emojis are added only for display (format_func), so the page names below stay unchanged.
PAGE_LABELS = {
    "Home": " Home",
    "Dashboard": " Dashboard",
    "Student Data": " Student Data",
    "Risk Checker": " Risk Checker",
    "About": " About",
}

with st.sidebar:
    st.title("🎓 EduRisk Menu")
    st.caption("Student Performance & Risk Analysis")
    st.divider()

    selected_page = st.radio(
        "Select Page",
        list(PAGE_LABELS.keys()),
        format_func=lambda page: PAGE_LABELS[page],
        label_visibility="visible",
    )

# 6. HOME PAGE
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Frontend Prototype with CSV Data Loading")
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads student data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )

    st.success("✅ Lab 03 app is running successfully!")

    st.info(
        "💡 Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )

# 7. DASHBOARD PAGE
elif selected_page == "Dashboard":
    st.title("📊 Dashboard Prototype")
    st.write(
        "A quick overview of student scores, attendance, course distribution, and academic risk."
    )

    st.subheader("Dashboard Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", f"{total_students:,}")

    with col2:
        st.metric("Average Score", f"{average_score:.1f}" if pd.notna(average_score) else "N/A")

    with col3:
        st.metric(
            "Average Attendance",
            f"{average_attendance:.1f}%" if pd.notna(average_attendance) else "N/A",
        )

    with col4:
        st.metric("High Risk", f"{high_risk_students:,}")

    st.divider()
    st.subheader("Student Records")
    st.caption("Student records loaded from students.csv, including the calculated risk level.")

    st.table(styled_table(student_df))

    st.divider()
    st.subheader("Student Performance Charts")
    chart_col1, chart_col2 = st.columns(2, gap="large")

    with chart_col1:
        st.markdown("**Student Score Chart**")
        st.caption("Compare scores across students.")
        score_chart = student_df[["Student Name", "Score"]]
        st.altair_chart(
            bar_chart(score_chart, "Student Name", "Score", "#38BDF8", angle=-90),
            use_container_width=True,
        )

    with chart_col2:
        st.markdown("**Course Count**")
        st.caption("See how students are distributed across courses.")
        course_count = student_df["Course"].value_counts().rename_axis("Course").reset_index(name="Students")
        st.altair_chart(
            bar_chart(course_count, "Course", "Students", "#176B9A", angle=-90),
            use_container_width=True,
        )

    st.markdown("**Risk Level Count**")
    st.caption("Each risk category has a distinct color for easier comparison.")

    risk_order = ["Low Risk", "Medium Risk", "High Risk"]
    risk_count = (
        student_df["Risk Level"]
        .value_counts()
        .reindex(risk_order, fill_value=0)
        .rename_axis("Risk Level")
        .reset_index(name="Students")
    )

    risk_colors = alt.Scale(
        domain=["High Risk", "Medium Risk", "Low Risk"],
        range=["#DC2626", "#A16207", "#16A34A"],
    )

    risk_chart = (
        alt.Chart(risk_count)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("Risk Level:N", sort=risk_order, title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Students:Q", title="Number of Students", scale=alt.Scale(domainMin=0)),
            color=alt.Color("Risk Level:N", scale=risk_colors, legend=None),
            tooltip=[
                alt.Tooltip("Risk Level:N", title="Risk Category"),
                alt.Tooltip("Students:Q", title="Students"),
            ],
        )
        .properties(height=300)
        .configure(font="Times New Roman")
        .configure_axis(labelFont="Times New Roman", titleFont="Times New Roman", labelFontSize=13, titleFontSize=14)
    )
    st.altair_chart(risk_chart, use_container_width=True)

    st.info(
        "💡 **Ethics reminder:** Use risk indicators to guide timely support and conversations. "
        "They should not be used to label, shame, or punish students."
    )


# 9. STUDENT DATA PAGE
elif selected_page == "Student Data":
    st.title("🗂️ Student Data")
    st.write("Inspect the dataset loaded from `students.csv`.")

    data_col1, data_col2 = st.columns(2)
    with data_col1:
        st.metric("Rows", f"{student_df.shape[0]:,}")
    with data_col2:
        st.metric("Columns (including Risk Level)", f"{student_df.shape[1]:,}")

    st.subheader("Column Names")
    st.code(", ".join(student_df.columns.astype(str)), language=None)

    with st.expander("Preview the first five rows", expanded=True):
        st.table(styled_table(student_df.head()))

    st.subheader("Full Student Dataset")
    st.table(styled_table(student_df))

    csv_bytes = student_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download student data (CSV)",
        data=csv_bytes,
        file_name="student_data_with_risk.csv",
        mime="text/csv",
    )

# 9. RISK CHECKER PAGE
elif selected_page == "Risk Checker":
    st.title("🔍 Single Student Risk Checker")
    st.write("Enter one student's score and attendance to estimate their current risk category.")

    with st.form("risk_checker_form", clear_on_submit=False):
        input_name = st.text_input("Student Name", placeholder="Enter student name")
        input_score = st.number_input("Score", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
        input_attendance = st.number_input(
            "Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=1.0,
        )
        submitted = st.form_submit_button("Check Risk", use_container_width=True)

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.divider()
        st.subheader("Assessment Summary")
        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric("Student", input_name.strip() or "Not provided")
        with result_col2:
            st.metric("Score", f"{input_score:g}/100")
        with result_col3:
            st.metric("Attendance", f"{input_attendance:g}%")

        if risk_result == "Low Risk":
            st.success("🟢 Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("🟡 Risk Level: Medium Risk")
        else:
            st.error("🔴 Risk Level: High Risk")

        st.caption(
            "This result follows the app's simple score/attendance rules; it is not a diagnosis or a complete assessment of a student."
        )

# 10. ABOUT PAGE
else:
    st.title("ℹ️ About")
    st.write(
        "EduRisk Analytics is a Lab 03 prototype for Web App Development for Data Science."
    )

    st.subheader("Project Information")
    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.markdown("**Course**")
        st.write("Web App Development for Data Science")
        st.markdown("**Project Theme**")
        st.write("EduRisk Analytics")

    with info_col2:
        st.markdown("**Lab**")
        st.write("Lab 03")
        st.markdown("**Main Features**")
        st.write("CSV data loading, layout, charts, and student risk checking")

    st.divider()
    st.subheader("Responsible Use")
    st.info(
        "🤝 Academic risk indicators should be interpreted carefully and used to support "
        "student learning, wellbeing, and success—not to make unfair or automatic decisions."
    )