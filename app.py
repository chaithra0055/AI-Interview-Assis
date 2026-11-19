
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Assistant Interview",
    layout="centered"
)

st.title("AI Interview Assistant")
st.caption("Launched By Bhavana S O")

# Groq API connection
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("API Key missing. Add GROQ_API_KEY to Streamlit secrets.")
    st.stop()

# User inputs
role = st.selectbox(
    "Job Title",
    ["Machine Learning Engineer", "Senior Software Engineer",
     "DevOps Engineer", "Data Analyst", "Other"]
)

if role == "Other":
    role = st.text_input("Enter your Job Title")

model = st.selectbox(
    "Model",
    ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
)

level = st.selectbox(
    "Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

mode = st.radio(
    "Activity",
    ["Generate Questions", "Generate Code Questions",
     "Evaluate Answers", "Improve Answers"]
)

# Mode-specific inputs
if mode in ["Generate Questions", "Generate Code Questions"]:
    count = st.slider("Number of Questions", 1, 10, 5)

if mode == "Generate Code Questions":
    topic = st.selectbox(
        "Topic", ["SQL", "AIML", "Python", "DSA", "Java", "C/C++"]
    )

if mode in ["Evaluate Answers", "Improve Answers"]:
    questions = st.text_area("Enter Interview Question")
    answer = st.text_area("Enter Your Answer", height=150)

# Generate response
if st.button("Generate AI Response", type="primary"):

    if not role or not role.strip():
        st.warning("Please enter a valid job title.")
        st.stop()

    if mode in ["Evaluate Answers", "Improve Answers"]:
        if not questions.strip() or not answer.strip():
            st.warning("Please enter both question and answer.")
            st.stop()

    # Create task
    if mode == "Generate Questions":
        task = f"""
        Generate {count} frequently asked interview questions
        for a {role} position at {level} level.
        Include theory and scenario-based questions.
        Give hints. Do not provide answers.
        """

    elif mode == "Generate Code Questions":
        task = f"""
        Generate {count} coding interview questions on {topic}
        for a {role} position.
        Difficulty: {level}.
        Include problem statements, input/output examples,
        constraints and hints. Do not provide solutions.
        """

    elif mode == "Evaluate Answers":
        task = f"""
        Interview Question: {questions}
        Candidate Answer: {answer}

        Evaluate based on:
        1. Conceptual Understanding
        2. Relevance
        3. Communication Skills
        4. Completeness

        Give each criterion a score out of 5.
        Calculate total score out of 20.
        Explain strengths, weaknesses and improvements.
        """

    else:
        task = f"""
        Interview Question: {questions}
        Original Answer: {answer}

        Improve the answer using professional vocabulary,
        correct grammar, better sentence structure and
        technical accuracy.

        Provide:
        1. Original Answer
        2. Improved Answer
        3. Important Word Replacements
        4. Grammar Corrections
        5. Suggestions for Improvement

        Maintain the original meaning.
        """

    # API request
    with st.spinner("Generating your response..."):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                        Act as a senior HR and technical interviewer.
                        Job Role: {role}
                        Difficulty: {level}
                        """
                    },
                    {
                        "role": "user",
                        "content": task
                    }
                ],
                temperature=0.7,
                max_tokens=1800
            )

            output = response.choices[0].message.content

            if output:
                st.subheader("AI Response")
                st.markdown(output)

                st.download_button(
                    "Download Response",
                    data=output,
                    file_name="Interview_Response.txt",
                    mime="text/plain"
                )
            else:
                st.warning("No response received. Please try again.")

        except Exception as e:
            st.error("Unable to generate response.")
            st.info(f"Error details: {e}")

st.caption("Powered by Streamlit and Groq API")
