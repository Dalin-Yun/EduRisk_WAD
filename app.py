# ============================================================
# EduRisk Analytics - Lab 02
# Student Performance and Risk Analysis
# ============================================================

import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="EduRisk Analytics - Lab 02",
    page_icon="🎓",
    layout="wide",
)

# ------------------------------------------------------------
# 2. CUSTOM CSS DESIGN
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Main font */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: "Times New Roman", Times, serif !important;
    }

    /* Keep Streamlit icons using their original icon font */
    .material-icons,
    .material-symbols-rounded,
    .material-symbols-outlined,
    [data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded", "Material Icons" !important;
        font-weight: normal !important;
        font-style: normal !important;
    }

    /* App background */
    .stApp,
    [data-testid="stMain"] {
        background-color: #F0F9FF;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #123B5D;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] label {
        font-size: 17px;
    }

    /* Main headings */
    h1, h2, h3 {
        color: #123B5D !important;
        font-family: "Times New Roman", Times, serif !important;
        font-weight: bold;
    }

    /* Normal text */
    p, label, span, div {
        font-family: "Times New Roman", Times, serif;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #38BDF8;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(18, 59, 93, 0.08);
    }

    [data-testid="stMetricLabel"] {
        color: #176B9A !important;
        font-size: 16px;
    }

    [data-testid="stMetricValue"] {
        color: #123B5D !important;
        font-size: 28px;
        font-weight: bold;
    }

    /* Buttons */
    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        background-color: #176B9A;
        color: #FFFFFF;
        border: 1px solid #176B9A;
        border-radius: 8px;
        padding: 8px 20px;
        font-family: "Times New Roman", Times, serif;
        font-size: 16px;
        font-weight: bold;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #123B5D;
        color: #FFFFFF;
        border: 1px solid #123B5D;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #38BDF8;
        color: #123B5D;
        border: 1px solid #38BDF8;
        border-radius: 8px;
        font-family: "Times New Roman", Times, serif;
        font-weight: bold;
    }

    .stDownloadButton > button:hover {
        background-color: #176B9A;
        color: #FFFFFF;
        border-color: #176B9A;
    }

    /* Input fields */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"],
    .stSlider {
        border-radius: 8px;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #BAE6FD;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #BAE6FD;
        border-radius: 12px;
    }

    /* Divider */
    hr {
        border-color: #BAE6FD;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Forms */
    [data-testid="stForm"] {
        background-color: #FFFFFF;
        border: 1px solid #BAE6FD;
        border-radius: 12px;
        padding: 20px;
    }

    /* Checkbox */
    [data-testid="stCheckbox"] label {
        color: #123B5D;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #BAE6FD;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 3. SAMPLE STUDENT DATA
# ------------------------------------------------------------
student_df = pd.DataFrame(
    {
        "Student Name": [
            "Dara", "Sophea", "Vuthy", "Malis",
            "Rithy", "Sreyneang", "Chan", "Bopha",
        ],
        "Course": [
            "Data Science", "Computer Science", "Data Science",
            "IT", "Computer Science", "IT", "Data Science",
            "Computer Science",
        ],
        "Score": [85, 55, 72, 90, 48, 68, 78, 60],
        "Attendance": [90, 65, 70, 95, 50, 72, 80, 58],
        "Study Hours": [12, 5, 8, 15, 3, 7, 10, 4],
    }
)

# ------------------------------------------------------------
# 4. RISK LEVEL FUNCTION
# ------------------------------------------------------------
def get_risk_level(score, attendance):
    """Classify academic risk based on score and attendance."""
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    return "Low Risk"


# Add a Risk Level column to the dataset
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1,
)

# ------------------------------------------------------------
# 5. SUMMARY STATISTICS
# ------------------------------------------------------------
total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = int((student_df["Score"] < 60).sum())

# ------------------------------------------------------------
# 6. SIDEBAR NAVIGATION
# ------------------------------------------------------------
st.sidebar.title("🎓 EduRisk Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Dashboard", "Student Data", "Risk Checker", "About"],
)

# ------------------------------------------------------------
# 7. HOME PAGE
# ------------------------------------------------------------
if page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Student Performance and Risk Analysis")

    st.write(
        "Welcome to EduRisk Analytics! This application helps analyze "
        "student academic performance and identify students who may need support."
    )

    st.success("Welcome to the EduRisk Analytics application!")

    if st.button("Click me"):
        st.success("Welcome!")

# ------------------------------------------------------------
# 8. DASHBOARD PAGE
# ------------------------------------------------------------
elif page == "Dashboard":
    st.title("📊 Student Performance Dashboard")
    st.write("Explore student performance and academic risk levels.")
    st.markdown("---")

    # Dashboard filters
    st.subheader("Filter Student Data")
    col1, col2 = st.columns(2)

    with col1:
        selected_course = st.selectbox(
            "Select Course",
            ["All"] + sorted(student_df["Course"].unique().tolist()),
        )

    with col2:
        selected_risk = st.selectbox(
            "Select Risk Level",
            ["All"] + sorted(student_df["Risk Level"].unique().tolist()),
        )

    min_attendance = st.slider(
        "Minimum Attendance (%)",
        min_value=0,
        max_value=100,
        value=0,
    )

    min_score = st.slider(
        "Minimum Score",
        min_value=0,
        max_value=100,
        value=0,
    )

    # Apply selected filters
    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    filtered_df = filtered_df[
        (filtered_df["Attendance"] >= min_attendance)
        & (filtered_df["Score"] >= min_score)
    ]

    st.markdown("---")

    # Dashboard metrics
    st.subheader("Performance Overview")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Total Students", len(filtered_df))

    with metric_col2:
        score_value = (
            f"{filtered_df['Score'].mean():.2f}"
            if not filtered_df.empty
            else "N/A"
        )
        st.metric("Average Score", score_value)

    with metric_col3:
        attendance_value = (
            f"{filtered_df['Attendance'].mean():.2f}%"
            if not filtered_df.empty
            else "N/A"
        )
        st.metric("Average Attendance", attendance_value)

    with metric_col4:
        low_score_count = int((filtered_df["Score"] < 60).sum())
        st.metric("Low Score Students", low_score_count)

    st.markdown("---")

    # Display filtered records
    st.subheader("Filtered Student Records")
    show_data = st.checkbox("Display filtered student data")

    if show_data:
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

    # Download filtered data
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data",
        data=csv_data,
        file_name="filtered_student_data.csv",
        mime="text/csv",
    )

    st.markdown("---")

    # Charts
    st.subheader("Student Performance Charts")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("**Student Scores**")
        if not filtered_df.empty:
            score_chart = filtered_df.set_index("Student Name")[["Score"]]
            st.bar_chart(score_chart)
        else:
            st.info("No data available for the selected filters.")

    with chart_col2:
        st.write("**Risk Level Distribution**")
        if not filtered_df.empty:
            risk_chart = (
                filtered_df["Risk Level"]
                .value_counts()
                .reindex(
                    ["Low Risk", "Medium Risk", "High Risk"],
                    fill_value=0,
                )
            )
            st.bar_chart(risk_chart)
        else:
            st.info("No data available for the selected filters.")

# ------------------------------------------------------------
# 9. STUDENT DATA PAGE
# ------------------------------------------------------------
elif page == "Student Data":
    st.title("👨‍🎓 Student Data")
    st.write("View all student academic records.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Average Score", f"{average_score:.2f}")

    with col3:
        st.metric("Average Attendance", f"{average_attendance:.2f}%")

    st.markdown("---")
    st.subheader("Complete Student Dataset")

    st.dataframe(
        student_df,
        use_container_width=True,
        hide_index=True,
    )

# ------------------------------------------------------------
# 10. RISK CHECKER PAGE
# ------------------------------------------------------------
elif page == "Risk Checker":
    st.title("🔍 Student Risk Checker")
    st.write("Enter student information to check the academic risk level.")
    st.markdown("---")

    with st.form("risk_checker_form"):
        student_name = st.text_input("Student Name")

        score = st.number_input(
            "Student Score",
            min_value=0,
            max_value=100,
            value=50,
        )

        attendance = st.number_input(
            "Student Attendance (%)",
            min_value=0,
            max_value=100,
            value=50,
        )

        submitted = st.form_submit_button("Check Risk Level")

    if submitted:
        if student_name.strip() == "":
            st.warning("Please enter the student name.")
        else:
            risk = get_risk_level(score, attendance)

            st.subheader("Risk Assessment Result")
            st.write(f"**Student Name:** {student_name}")
            st.write(f"**Score:** {score}")
            st.write(f"**Attendance:** {attendance}%")

            if risk == "Low Risk":
                st.success(f"Risk Level: {risk}")
            elif risk == "Medium Risk":
                st.warning(f"Risk Level: {risk}")
            else:
                st.error(f"Risk Level: {risk}")

# ------------------------------------------------------------
# 11. ABOUT PAGE
# ------------------------------------------------------------
elif page == "About":
    st.title("ℹ️ About EduRisk Analytics")

    st.write(
        "EduRisk Analytics is a student performance analysis application "
        "developed to explore academic data and identify students who may "
        "need additional academic support."
    )

    st.markdown("---")
    st.subheader("Application Information")

    st.write("**Application Name:** EduRisk Analytics")
    st.write("**Course:** Web Application Development for Data Science")
    st.write("**Technology:** Python, Streamlit, and Pandas")

    st.markdown("---")
    st.subheader("Purpose")

    st.write(
        "The purpose of this application is to display student performance "
        "information and classify academic risk levels based on student scores "
        "and attendance."
    )

    st.info(
        "This application is intended for educational analysis. "
        "Risk levels should be used as indicators for support, not as final "
        "judgments about students."
    )
