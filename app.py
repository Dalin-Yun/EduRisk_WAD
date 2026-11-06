# EduRisk Analytics — Student Performance & Risk Analysis
# Lab 04: Forms, Validation, and Session State

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="EduRisk Analytics - Lab 05",
    page_icon="🎓",
    layout="wide"
)

# LOAD CSS
def load_css():
    """Load style.css from the same folder as app.py."""
    css_path = Path(__file__).resolve().parent / "style.css"

    if css_path.is_file():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        # The app still works if the optional stylesheet is missing.
        st.warning(
            f"CSS file not found: {css_path.name}. "
            "Using Streamlit's default styling."
        )


load_css()


# 2. LOAD STUDENT DATA
@st.cache_data
def load_student_data(file_path):
    """Read the CSV file and cache it until the file changes."""
    return pd.read_csv(file_path)


DATA_PATH = Path(__file__).resolve().parent / "students.csv"

if not DATA_PATH.is_file():
    st.error("students.csv was not found. Please place it in the same folder as app.py.")
    st.stop()

try:
    student_df = load_student_data(str(DATA_PATH))
except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
    st.error(f"Could not read students.csv. Please check the file format. Details: {error}")
    st.stop()


# 3. CHECK DATA AND CALCULATE RISK LEVELS
required_columns = {"Student Name", "Score", "Attendance", "Course"}
missing_columns = required_columns.difference(student_df.columns)

if missing_columns:
    st.error(
        "Missing required column(s) in students.csv: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

# Convert score and attendance to numeric values so calculations are reliable.
for column in ("Score", "Attendance"):
    student_df[column] = pd.to_numeric(student_df[column], errors="coerce")

if student_df[["Score", "Attendance"]].isna().any().any():
    st.error(
        "The Score and Attendance columns must contain numeric values. "
        "Please fix empty or non-numeric values in students.csv."
    )
    st.stop()

if not student_df["Score"].between(0, 100).all():
    st.error("Every Score value in students.csv must be between 0 and 100.")
    st.stop()

if not student_df["Attendance"].between(0, 100).all():
    st.error("Every Attendance value in students.csv must be between 0 and 100.")
    st.stop()


def get_risk_level(score, attendance):
    """Apply the simple score/attendance rules used in this lab."""
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    return "Low Risk"


# Add a risk label to each row in the dataset.
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1,
)


# 4. INITIALIZE SESSION STATE
# Session State keeps recent checks across Streamlit reruns in this browser session.
if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

if "latest_risk_result" not in st.session_state:
    st.session_state["latest_risk_result"] = None


# 5. TABLE STYLING HELPERS
def color_risk(value):
    """Return a background and text color for each risk category."""
    colors = {
        "High Risk": "background-color: #FEE2E2; color: #991B1B;",
        "Medium Risk": "background-color: #FEF3C7; color: #854D0E;",
        "Low Risk": "background-color: #DCFCE7; color: #166534;",
    }
    return colors.get(value, "")


def styled_table(dataframe):
    """Style the Risk Level column when it is present."""
    if "Risk Level" not in dataframe.columns:
        return dataframe
    return dataframe.style.map(color_risk, subset=["Risk Level"]).hide(axis="index")


# 6. CHART HELPER
def bar_chart(data, x_col, y_col, color="#247A6B", angle=0):
    """Create a consistently styled bar chart with Altair."""
    chart = (
        alt.Chart(data)
        .mark_bar(
            color=color,
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5,
        )
        .encode(
            x=alt.X(
                f"{x_col}:N",
                sort=None,
                title=None,
                axis=alt.Axis(
                    labelAngle=-90,
                    labelAlign="right",
                    labelFontSize=11,
                    labelPadding=8,
                    ticks=False,
                ),
            ),
            y=alt.Y(
                f"{y_col}:Q",
                title=y_col,
                scale=alt.Scale(domainMin=0),
                axis=alt.Axis(tickMinStep=1),
            ),
            tooltip=[
                alt.Tooltip(f"{x_col}:N"),
                alt.Tooltip(f"{y_col}:Q"),
            ],
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


# 7. SIDEBAR NAVIGATION
# Keep the actual page names unchanged; emojis are only for display.
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
    )


# 8. HOME PAGE
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Interactive Dashboard with Visualization and Filters")
    st.write("Welcome to Lab 05.")
    st.write(
        "In this lab, the app improves the Dashboard page using "
        "grouped summaries, interactive filters, Streamlit charts, and Plotly charts."
    )
    st.success("Lab 05 app is running successfully!")

# 9. DASHBOARD PAGE

# 9. DASHBOARD PAGE
elif selected_page == "Dashboard":
    st.title("Interactive Student Performance Dashboard")

    st.write(
        "Use filters to explore student performance by course, risk level, "
        "and attendance. The dashboard updates based on your selections."
    )

    # Dashboard Filters
    st.subheader("Dashboard Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    # Course Filter
    with filter_col1:
        course_options = ["All"] + sorted(student_df["Course"].unique())

        selected_course = st.selectbox(
            "Filter by Course",
            course_options
        )

    # Risk Level Filter
    with filter_col2:
        risk_options = ["All"] + sorted(student_df["Risk Level"].unique())

        selected_risk = st.selectbox(
            "Filter by Risk Level",
            risk_options
        )

    # Attendance Slider
    with filter_col3:
        minimum_attendance = st.slider(
            "Minimum Attendance",
            0,
            100,
            0
        )

    # Create Filtered DataFrame
    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[
            filtered_df["Course"] == selected_course
        ]

    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk Level"] == selected_risk
        ]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= minimum_attendance
    ]

    # Handle Empty Filter Results
    if filtered_df.empty:
        st.warning(
            "No students match the selected filters. "
            "Please adjust the filters."
        )

    # Calculate Filtered Metrics
    st.subheader("Filtered Dashboard Metrics")
    filtered_total_students = len(filtered_df)

    if filtered_total_students > 0:
        filtered_average_score = filtered_df["Score"].mean()

        filtered_average_attendance = filtered_df["Attendance"].mean()

        filtered_high_risk_students = filtered_df[
            filtered_df["Risk Level"] == "High Risk"
        ].shape[0]

    else:
        filtered_average_score = 0
        filtered_average_attendance = 0
        filtered_high_risk_students = 0

    # Display Metric Cards
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Students", filtered_total_students)

    with metric_col2:
        st.metric("Average Score", round(filtered_average_score, 2))
        
    with metric_col3:
        st.metric(
            "Average Attendance",
            f"{round(filtered_average_attendance, 2)}%"
        )

    with metric_col4:
        st.metric("High Risk", filtered_high_risk_students)

    # Course Summary Table
    st.subheader("Course Summary")

    if filtered_total_students > 0:
        course_summary = filtered_df.groupby("Course").agg(
            Students=("Student Name", "count"),
            Average_Score=("Score", "mean"),
            Average_Attendance=("Attendance", "mean"),
            Average_Study_Hours=("Study Hours", "mean")
        ).reset_index()

        st.dataframe(
            course_summary,
            use_container_width=True
        )
    else:
        st.info("No course summary available for the selected filters.")

    # Risk Level Summary Table
    st.subheader("Risk Level Summary")

    if filtered_total_students > 0:
        risk_summary = filtered_df["Risk Level"].value_counts().reset_index()
        risk_summary.columns = ["Risk Level", "Students"]

        st.dataframe(
            risk_summary,
            use_container_width=True
        )
    else:
        st.info("No risk summary available for the selected filters.")

    # Streamlit Charts Section
    st.subheader("Streamlit Charts")

    chart_col1, chart_col2 = st.columns(2)

    # Student Score Chart
    with chart_col1:
        st.write("Student Scores")

        if filtered_total_students > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.info("No score chart available.")

    # Students by Course Chart
    with chart_col2:
        st.write("Students by Course")

        if filtered_total_students > 0:
            course_count = filtered_df["Course"].value_counts()
            st.bar_chart(course_count)
        else:
            st.info("No course count chart available.")

    # Plotly Charts Section
    st.subheader("Interactive Plotly Charts")

    plotly_col1, plotly_col2 = st.columns(2)

    # Risk Level Distribution
    with plotly_col1:
        st.write("Risk Level Distribution")

        if filtered_total_students > 0:
            risk_summary_chart = (
                filtered_df["Risk Level"]
                .value_counts()
                .reset_index()
            )

            risk_summary_chart.columns = ["Risk Level", "Students"]

            fig_risk = px.bar(
                risk_summary_chart,
                x="Risk Level",
                y="Students",
                color="Risk Level",
                title="Risk Level Distribution",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(
                fig_risk,
                use_container_width=True
            )
        else:
            st.info("No risk distribution chart available.")

    # Student Scores by Risk Level
    with plotly_col2:
        st.write("Student Scores by Risk Level")

        if filtered_total_students > 0:
            fig_score = px.bar(
                filtered_df,
                x="Student Name",
                y="Score",
                color="Risk Level",
                title="Student Scores by Risk Level",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(
                fig_score,
                use_container_width=True
            )
        else:
            st.info("No score chart available.")

    # Filtered Student Records
    st.subheader("Filtered Student Records")

    if filtered_total_students > 0:
        st.dataframe(
            styled_table(filtered_df),
            use_container_width=True
        )
    else:
        st.info("No student records to display.")

    # Ethical Visualization Reminder
    st.warning(
        "Ethics Reminder: Visualizations should support students and guide "
        "academic support decisions, not label or punish students."
    )

# 10. STUDENT DATA PAGE
elif selected_page == "Student Data":
    st.title("Student Data")
    st.write("This page displays and inspects the dataset loaded from students.csv.")

    st.subheader("Data Inspection")
    st.write("Rows and columns:", student_df.shape)
    
    st.write("Column Names: ")
    st.write(student_df.columns.tolist())

    st.subheader("First 5 Rows: ")
    st.dataframe(styled_table(student_df.head()), use_container_width=True)

    st.subheader("Full Student Dataset")
    st.dataframe(styled_table(student_df), use_container_width=True)

# 11. RISK CHECKER PAGE
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")
    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )

    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )

    # A form waits until Check Risk is clicked before processing the inputs.
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", min_value=0, max_value=100, value=50)
        input_attendance = st.number_input(
            "Attendance", min_value=0, max_value=100, value=50
        )
        submitted = st.form_submit_button("Check Risk", use_container_width=True)

    # Validate first; only calculate and save when the name is valid.
    if submitted:
        if input_name.strip() == "":
            st.session_state["latest_risk_result"] = None
            st.warning("Please enter the student name.")
        else:
            risk_result = get_risk_level(input_score, input_attendance)

            result = {
                "Student Name": input_name.strip(),
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result,
            }

            # Save the successful check once; the history survives reruns.
            st.session_state["risk_history"].append(result)
            st.session_state["latest_risk_result"] = result

    # Show the latest successful result even after unrelated reruns.
    latest_result = st.session_state["latest_risk_result"]
    if latest_result is not None:
        st.divider()
        st.subheader("Assessment Summary")

        result_col1, result_col2, result_col3 = st.columns(3)
        result_col1.metric("Student", latest_result["Student Name"])
        result_col2.metric("Score", f'{latest_result["Score"]:g}/100')
        result_col3.metric("Attendance", f'{latest_result["Attendance"]:g}%')

        risk_result = latest_result["Risk Level"]
        if risk_result == "Low Risk":
            st.success("🟢 Risk Level: Low Risk")
            st.write("Student appears on track.")
        elif risk_result == "Medium Risk":
            st.warning("🟡 Risk Level: Medium Risk")
            st.write("Monitor progress and provide guidance.")
        else:
            st.error("🔴 Risk Level: High Risk")
            st.write("Student may need additional support.")

        st.caption(
            "This result follows the app's simple score/attendance rules; "
            "it is not a diagnosis or a complete assessment of a student."
        )

    # Keep history visible independently of the submit button.
    st.divider()
    st.subheader("Recent Risk Checks")

    if st.session_state["risk_history"]:
        history_df = pd.DataFrame(st.session_state["risk_history"])
        st.dataframe(styled_table(history_df), use_container_width=True)

        # Keep Clear History outside the form so it works independently.
        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.session_state["latest_risk_result"] = None
            st.success("Risk check history cleared.")
            st.rerun()
    else:
        st.info("No risk checks yet.")

    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as a final judgment about a student."
    )


# 12. ABOUT PAGE
else:
    st.title("About")
    
    st.write("This app is part of Lab 05.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Visualization and Interactivity")

    st.info(
        "This version improves the Dashboard page using grouped summaries,"
        "interactive filters, Streamlit charts, and Plotly charts."
    )
    st.warning(
        "Ethics Reminder: Student performance visualizations should be used "
        "responsibly to support learning and student success."
    )