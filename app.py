import os
import streamlit as st

from claim_assisstant import get_claim_answer


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Claim Wise",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# REFERENCE QUESTION CALLBACK
# =========================================================

def select_question(question):
    st.session_state.question_box = question


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ---------------------------------------------------------
   PAGE
--------------------------------------------------------- */

.stApp {
    background-color: #f7f8fc;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}


/* ---------------------------------------------------------
   HEADER
--------------------------------------------------------- */

.header-title {
    font-size: 38px;
    font-weight: 700;
    color: #202636;
    margin-bottom: 5px;
}

.header-subtitle {
    font-size: 19px;
    color: #626b7d;
    margin-bottom: 8px;
}

.header-description {
    font-size: 14px;
    color: #8a91a2;
}


/* ---------------------------------------------------------
   SECTION HEADINGS
--------------------------------------------------------- */

.section-title {
    font-size: 23px;
    font-weight: 650;
    color: #202636;
    margin-bottom: 15px;
}


/* ---------------------------------------------------------
   REFERENCE BUTTONS
--------------------------------------------------------- */

div.stButton > button {
    border-radius: 12px;
    border: 1px solid #dfe3ec;
    background-color: white;
    color: #454d60;
    font-size: 14px;
    text-align: left;
    min-height: 45px;
    padding: 8px 14px;
    margin-bottom: 5px;
}

div.stButton > button:hover {
    border-color: #6575e8;
    background-color: #f3f5ff;
    color: #4f5fd0;
}


/* ---------------------------------------------------------
   MAIN BUTTON
--------------------------------------------------------- */

div.stButton > button[kind="primary"] {
    background-color: #6575e8;
    color: white;
    border: none;
    font-weight: 600;
    text-align: center;
    min-height: 48px;
}

div.stButton > button[kind="primary"]:hover {
    background-color: #5365df;
    color: white;
}


/* ---------------------------------------------------------
   ANSWER
--------------------------------------------------------- */

.answer-box {
    background-color: white;
    border: 1px solid #e1e5ed;
    border-left: 5px solid #6575e8;
    border-radius: 14px;
    padding: 20px;
    margin-top: 10px;
    color: #343b4d;
    font-size: 16px;
    line-height: 1.7;
}


/* ---------------------------------------------------------
   FOOTER
--------------------------------------------------------- */

.footer {
    text-align: center;
    color: #9aa1b2;
    font-size: 12px;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "question_box" not in st.session_state:
    st.session_state.question_box = ""


# =========================================================
# HEADER
# =========================================================

header_image, header_text = st.columns(
    [1.1, 4],
    vertical_alignment="center"
)


# ---------------------------------------------------------
# ROBOT IMAGE
# ---------------------------------------------------------

with header_image:

    robot_path = os.path.join(
        os.path.dirname(__file__),
        "robot.png"
    )

    if os.path.exists(robot_path):

        st.image(
            robot_path,
            width=180
        )

    else:

        st.markdown(
            "# 🤖"
        )

        st.caption(
            "Add robot.png to the project folder"
        )


# ---------------------------------------------------------
# CLAIM WISE TEXT
# ---------------------------------------------------------

with header_text:

    st.markdown(
        '<div class="header-title">'
        "Hi, I'm Claim Wise 👋"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="header-subtitle">'
        "Your Insurance Claim Assistant"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="header-description">'
        "I turn complex claim information into simple answers."
        "</div>",
        unsafe_allow_html=True
    )


st.divider()


# =========================================================
# MAIN PAGE
# =========================================================

left_column, right_column = st.columns(
    [2.2, 1],
    gap="large"
)


# =========================================================
# LEFT SIDE
# =========================================================

with left_column:

    st.markdown(
        '<div class="section-title">'
        "💬 Ask me"
        "</div>",
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # CLAIM ID
    # -----------------------------------------------------

    claim_id = st.text_input(
        "Claim ID",
        placeholder="Example: CLM00001"
    )


    # -----------------------------------------------------
    # QUESTION
    # -----------------------------------------------------

    question = st.text_area(
        "Question",
        placeholder="Ask anything about your claim...",
        height=110,
        key="question_box"
    )


    # -----------------------------------------------------
    # GET EXPLANATION
    # -----------------------------------------------------

    get_answer = st.button(
        "🤖 Get Explanation",
        type="primary",
        use_container_width=True
    )


    # =====================================================
    # PROCESS QUESTION
    # =====================================================

    if get_answer:

        if not claim_id.strip():

            st.warning(
                "Please enter your Claim ID."
            )

        elif not question.strip():

            st.warning(
                "Please enter your question."
            )

        else:

            with st.spinner(
                "Claim Wise is thinking..."
            ):

                answer = get_claim_answer(
                    claim_id,
                    question
                )


            # -------------------------------------------------
            # EXPLANATION
            # -------------------------------------------------

            st.markdown(
                '<div class="section-title" '
                'style="margin-top:30px;">'
                "🤖 Explanation"
                "</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="answer-box">
                    {answer}
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# RIGHT SIDE
# =========================================================

with right_column:

    st.markdown(
        '<div class="section-title">'
        "💡 Try asking"
        "</div>",
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # QUESTION 1
    # -----------------------------------------------------

    st.button(
        "📋 What is my claim status?",
        use_container_width=True,
        on_click=select_question,
        args=("What is my claim status?",)
    )


    # -----------------------------------------------------
    # QUESTION 2
    # -----------------------------------------------------

    st.button(
        "💰 What is my deductible?",
        use_container_width=True,
        on_click=select_question,
        args=("What is my deductible?",)
    )


    # -----------------------------------------------------
    # QUESTION 3
    # -----------------------------------------------------

    st.button(
        "🏥 What does my policy cover?",
        use_container_width=True,
        on_click=select_question,
        args=("What does my policy cover?",)
    )


    # -----------------------------------------------------
    # QUESTION 4
    # -----------------------------------------------------

    st.button(
        "💳 What is my approved amount?",
        use_container_width=True,
        on_click=select_question,
        args=("What is my approved amount?",)
    )


    # -----------------------------------------------------
    # QUESTION 5
    # -----------------------------------------------------

    st.button(
        "🚑 What is my ambulance coverage?",
        use_container_width=True,
        on_click=select_question,
        args=("What is my ambulance coverage?",)
    )


    # -----------------------------------------------------
    # QUESTION 6
    # -----------------------------------------------------

    st.button(
        "❓ Why was my claim rejected?",
        use_container_width=True,
        on_click=select_question,
        args=("Why was my claim rejected?",)
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    '<div class="footer">'
    "Claim Wise • AI-powered Insurance Claim Explanation Assistant"
    "</div>",
    unsafe_allow_html=True
)