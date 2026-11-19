import streamlit as st
from groq import Groq
st.set_page_config(page_title = "interview assistent",page_icon='😍',layout = 'centered')
st.title("AI Inteview Assistant")
st.caption("Pactice and Prepare for your Placements here")
st.caption("Launched by Bhavana S O ")
try:
  client = Groq(api_key = st.secrets["GROQ_API_KEY"])
except(KeyError,FileNotFound):
                st.error("API KEY is missing.Add it in Advanced settings")
                st.stop()
role=st.selectbox('Job title',['Machine Learning Engineer','Senior Software Engineer','Data Analyst','prompt Engineer','Other'])
if role == 'Other':
  st.text_input('Enter your Job Title','XXXXXXXXX')
gen_model = st.selectbox('Model',['openai/gpt-oss-120b','openai/gpt-oss-20b'])
level=st.selectbox('Difficult Level',['Beginner','intermediate','Advanced'])
mode = st.radio('Activity',['Generate Questions','Generate Code Questions','Evaluate Answers','Improve Answer'])
if mode == 'Generate Questions':
  count = st.slider("Number of Questions",1,10,5)
elif mode == 'Generate Code Questions':
  topic = st.selectbox('Topics',['SQL','AIML','Python','DAS','DBMS'])
  count = st.slider("Number of Questions",1,10,5)
else:
  question = st.text_area('Enter Interview Questions here')
  answer = st.text_area('Enter your answer',height=160)

if st.button("Generate AI Response", type='primary'):
  if mode in ['Evaluate Answers','Improve Answer'] and (not question.strip() or not answer.strip()):
    st.warning("Please enter a valid Question and Answer")
    st.stop()

  if mode == "Generate Questions":
    task = "Generate"+ str(count)+" Frequently asked interview questions, 3 theory 2 senario questions .do not give me ans give me hint"
  elif mode == "Generate Code Questions":
    task = "Generate" + str(count) +" Frequently asked coding qustions on topic "+topic+"and give hints to solve them"
  elif mode == 'Evaluate Answers':
    task = "Question :"+ question + " My Answer "+ answer + "Evaluate this answer based on concept ,relevent,communication ,and is suitable for the question ,length of the ans"
  elif mode == 'Improve Answer':
    task = "Question :"+ question + " My Answer "+ answer + "Improve the ans and check whether it include key words and important points ,accuracy "
  background = "Job role :" + role + "Difficulti level " +level
  with st.spinner("Generating your answer..."):
    try:
      req = client.chat.completions.create(
        model = gen_model,
        messages = [{"role":"system",
                     "content":"Act as a Senior Interviewer,both HR and Technical expert"},
                    {"role":"user",
                     "content":background + task}],
        temperature = 0.7,
        max_tokens = 2000
      )
      output=req.choices[0].message.content
      st.subheader("AI Response")
      st.markdown(output)
      st.download_button("Download Response",output,file_name= "Interview_Response.txt",mime="text/plain")
    except Exception as e:
      st.error ("API connection was unsuccessful",e)
      st.info("Please check your API Key and rate limits")
st.caption("Powered by Streamlit.io and GitHub. Using LLM API")
