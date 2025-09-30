import streamlit as st

st.set_page_config(page_title="Guided Flow Chatbot")
st.title("Guided Flow Chatbot")

# Define the flow of questions with validation
questions = [
    {
        "q": "👋 Welcome! Let's start. What is your name?",
        "key": "name",
        "validate": lambda x: x.replace(" ", "").isalpha(),
        "error": "Name should only contain alphabets."
    },
    {
        "q": "Great! How many years of experience do you have in Data Science?",
        "key": "experience",
        "validate": lambda x: x.isdigit() and 0 <= int(x) <= 50,
        "error": "Please enter a valid number of years (0–50)."
    },
    {
        "q": "Nice. Which programming language are you most comfortable with?",
        "key": "language",
        "validate": lambda x: x.isalpha(),
        "error": "Programming language should only contain alphabets."
    },
    {
        "q": "Which ML algorithm do you like the most?",
        "key": "algorithm",
        "validate": lambda x: x.replace(" ", "").isalpha(),
        "error": "Algorithm name should only contain alphabets."
    },
    {
        "q": "Awesome! Finally, what is your career goal in Data Science?",
        "key": "goal",
        "validate": lambda x: len(x.strip()) > 5,
        "error": "Career goal should be a meaningful statement (at least 5 characters)."
    },
]

# Initialize state
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "error_msg" not in st.session_state:
    st.session_state.error_msg = None

# Ask current question
if st.session_state.current_step < len(questions):
    question_obj = questions[st.session_state.current_step]
    st.write(question_obj["q"])
    user_input = st.text_input("Your answer:", key=f"q_{st.session_state.current_step}")

    if user_input:
        if question_obj["validate"](user_input):  # ✅ Validation
            st.session_state.answers[question_obj["key"]] = user_input
            st.session_state.current_step += 1
            st.session_state.error_msg = None
            st.rerun()
        else:
            st.session_state.error_msg = question_obj["error"]

    if st.session_state.error_msg:
        st.error(st.session_state.error_msg)

# Show summary if done
else:
    st.success("Thanks for answering all questions! Here’s your summary:")

    st.markdown(
        f"""
        ### Your Responses
        - **Name:** {st.session_state.answers['name']}
        - **Experience:** {st.session_state.answers['experience']} years
        - **Programming Language:** {st.session_state.answers['language']}
        - **Favorite Algorithm:** {st.session_state.answers['algorithm']}
        - **Career Goal:** {st.session_state.answers['goal']}
        """
    )

    if st.button("🔄 Restart"):
        st.session_state.answers = {}
        st.session_state.current_step = 0
        st.session_state.error_msg = None
        st.rerun()
