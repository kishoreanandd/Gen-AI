import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AK International School",
    page_icon="🎓",
    layout="centered"
)

# Lavender background and styling
st.markdown("""
<style>
    .stApp {
        background-color: #E6E6FA;
    }

    .school-name {
        text-align: center;
        color: #5B3F8C;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .title {
        text-align: center;
        color: #35245C;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)


# School name at the top
st.markdown(
    '<div class="school-name">🏫 AK International School</div>',
    unsafe_allow_html=True
)

# Main title
st.markdown(
    '<div class="title">🎓 Student Grade System</div>',
    unsafe_allow_html=True
)


# Student name
student_name = st.text_input(
    "🎓 Enter Student Name",
    placeholder="Enter student name"
)


# Form for mark and button
with st.form("grade_form"):

    mark = st.number_input(
        "📝 Enter Mark",
        min_value=0.0,
        max_value=100.0,
        value=None,
        step=1.0,
        placeholder="Enter mark between 0 and 100"
    )

    calculate = st.form_submit_button(
        "Calculate Grade",
        use_container_width=True
    )


# Calculate grade
if calculate:

    if student_name.strip() == "":
        st.error("Please enter the student name.")

    elif mark is None:
        st.error("Please enter the mark.")

    else:

        if mark >= 90:
            grade = "A"
        elif mark >= 80:
            grade = "B"
        elif mark >= 70:
            grade = "C"
        elif mark >= 60:
            grade = "D"
        else:
            grade = "E"

        # Show result
        st.success(
            f"Student: {student_name} | Mark: {mark:.0f} | Grade: {grade}"
        )

        # Message
        if grade == "A":
            st.balloons()
            st.success("🎉 Excellent! Outstanding performance!")

        elif grade == "B":
            st.success("🎉 Great job! Keep up the good work!")

        elif grade == "C":
            st.info("👏 Good effort! Keep working hard.")

        elif grade == "D":
            st.info("💪 You passed! Keep practicing to improve.")

        else:
            st.warning(
                "🌟 Don't give up! Keep practicing. "
                "You can do better next time!"
            )