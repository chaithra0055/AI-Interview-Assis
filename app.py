
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Assistant Interview",
    layout="centered"
)

st.title("AI Interview Assistant")
st.caption("Launched By Bhavana SO")

# API connection
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error("API Key is missing. Add GROQ_API_KEY in Streamlit secrets.")
    st.stop()

# Job role
role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineer",
        "DevOps Engineer",
        "Data Analyst",
        "Other"
    ]
)

if role == "Other":
    role = st.text_input("Enter your Job Title", placeholder="Enter job title")

# Model selection
gen_model = st.selectbox(
    "Model",
    ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
)

# Difficulty
level = st.selectbox(
    "Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

# Activity
mode = st.radio(
    "Activity",
    [
        "Generate Questions",
        "Generate Code Questions",
        "Evaluate Answers",
        "Improve Answers"
    ]
)

# Inputs based on activity
if mode == "Generate Questions":
    count = st.slider("Number of Questions", 1, 10, 5)

elif mode == "Generate Code Questions":
    topic = st.selectbox(
        "Topics",
        ["SQL", "AIML", "Python", "DSA", "Java", "C/C++"]
    )
    count = st.slider("Number of Questions", 1, 10, 5)

else:
    questions = st.text_area("Enter Interview Questions here")
    answer = st.text_area("Enter your answer", height=160)

# Generate button
if st.button("Generate AI Response", type="primary"):

    # Validate inputs
    if not role.strip():
        st.warning("Please enter a valid job title.")
        st.stop()

    if mode in ["Evaluate Answers", "Improve Answers"]:
        if not questions.strip() or not answer.strip():
            st.warning("Please enter both the interview question and your answer.")
            st.stop()

    # Create prompts
    if mode == "Generate Questions":
        task = (
            f"Generate {count} frequently asked interview questions "
            f"for a {role} position. Include theory-based and "
            f"scenario-based questions. Do not provide answers. "
            f"Give hints for each question."
        )

    elif mode == "Generate Code Questions":
        task = (
            f"Generate {count} frequently asked coding interview questions "
            f"on {topic} for a {role} position. "
            f"Difficulty: {level}. Include practical coding problems, "
            f"input/output examples, constraints and hints. "
            f"Do not provide solutions. Be accurate."
        )

    elif mode == "Evaluate Answers":
        task = (
            f"Question: {questions}\n"
            f"My Answer: {answer}\n"
            "Evaluate my answer based on:\n"
            "1. Conceptual Understanding\n"
            "2. Relevance\n"
            "3. Communication Skills\n"
            "4. Length and Completeness\n"
            "Give each criterion a rating out of 5. "
            "Calculate the total score out of 20. "
            "Explain strengths, weaknesses and suggestions for improvement."
        )

    elif mode == "Improve Answers":
        task = (
            f"Question: {questions}\n"
            f"My Answer: {answer}\n"
            "Improve my answer based on the following criteria:\n"
            "1. Use professional vocabulary and better word choices.\n"
            "2. Correct grammar and spelling mistakes.\n"
            "3. Improve sentence structure and clarity.\n"
            "4. Improve technical accuracy and conceptual understanding.\n"
            "5. Make the answer concise, clear and interview-ready.\n"
            "6. Maintain the original meaning.\n\n"
            "Provide the output in this format:\n"
            "1. Original Answer\n"
            "2. Improved Answer\n"
            "3. Important Word Replacements\n"
            "4. Grammar Corrections\n"
            "5. Suggestions for Improvement"
        )

    # Background information
    background = (
        f"Job Role: {role}\n"
        f"Difficulty Level: {level}\n"
        "Act as a senior HR and technical interviewer.\n"
    )

    # Generate AI response
    with st.spinner("Generating your answer..."):
        try:
            response = client.chat.completions.create(
                model=gen_model,
                messages=[
                    {
                        "role": "system",
                        "content": background
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

            st.subheader("AI Response")
            st.markdown(output)

            st.download_button(
                "Download Response",
                output,
                file_name="Interview_Response.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"API connection was unsuccessful: {e}")
            st.info("Please check your API key, model availability and rate limits.")

st.caption("Powered by Streamlit and Groq API")
