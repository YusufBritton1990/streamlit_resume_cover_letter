import streamlit as st
import os
import openai as ai
from PyPDF2 import PdfReader

# if running locally, make folder/file: .streamlit/secrets.toml
ai.api_key = st.secrets["OPENAI_API_KEY"] #running on streamlit
  

resume_text = st.text_input('Pasted resume elements')

with st.form('input_form'):
    # other inputs
    job_desc = st.text_input('Pasted job description')
    user_name = st.text_input('Your name')
    company = st.text_input('Company name')
    manager = st.text_input('Hiring manager')
    role = st.text_input('Job title/role')
    referral = st.text_input('How did you find out about this opportunity?')
    ai_temp = st.number_input('AI Temperature (0.0-1.0) Input how creative the API can be',value=.99)

    # submit button
    # submitted = st.form_submit_button("Generate Cover Letter")
    submitted = st.form_submit_button("Generate Resume")

if submitted:

  # Prompts
  cover_letter_completion = ai.ChatCompletion.create(
    #model="gpt-3.5-turbo-16k", 
    model = "gpt-3.5-turbo",
    temperature=ai_temp,
    messages = [
    {"role": "user", "content" : f"You will need to generate a cover letter based on specific resume and a job description"},
    {"role": "user", "content" : f"My resume text: {resume_text}"},
    {"role": "user", "content" : f"The job description is: {job_desc}"},
    {"role": "user", "content" : f"The candidate's name to include on the cover letter: {user_name}"},
    {"role": "user", "content" : f"The job title/role : {role}"},
    {"role": "user", "content" : f"The hiring manager is: {manager}"},
    {"role": "user", "content" : f"How you heard about the opportunity: {referral}"},
    {"role": "user", "content" : f"The company to which you are generating the cover letter for: {company}"},
    {"role": "user", "content" : f"The cover letter should have two content paragraphs"},
    {"role": "user", "content" : f""" 
    In the first paragraph focus on the following: you will convey who you are, what position you are interested in, and where you heard
    about it, and summarize what you have to offer based on the above resume
    """},
    {"role": "user", "content" : f""" 
    In the second paragraph focus on why the candidate is a great fit drawing parallels between the experience included in the resume 
    and the qualifications on the job description.
    """},

    {"role": "user", "content" : f""" 
    note that contact information may be found in the included resume text and use and/or summarize specific resume context for the letter
    """},
    {"role": "user", "content" : f"Use {user_name} as the candidate"},

    {"role": "user", "content" : f"Generate a specific cover letter based on the above. Generate the response and include appropriate spacing between the paragraph text"}
    ]
  )

  resume_completion = ai.ChatCompletion.create(
    #model="gpt-3.5-turbo-16k", 
    model = "gpt-3.5-turbo",
    temperature=ai_temp,
    messages = [
      {"role": "user", "content" : f"Re-write my resume, changing my bullet points to this job description for a {role} role at {company}"},
      {"role": "user", "content" : f"Write resume achievements with metrics based on these job responsibilities"},
      {"role": "user", "content" : f"The resume is: {resume_text}"},
      {"role": "user", "content" : f"The job description is: {job_desc}"}
    ]
  )

  st.markdown("""
  Cover Letter
  """
  )

  cover_letter_response_out = cover_letter_completion['choices'][0]['message']['content']
  st.write(cover_letter_response_out)

  st.markdown("""
  Resume
  """
  )

  resume_response_out = resume_completion['choices'][0]['message']['content']
  st.write(resume_response_out)

  # Download buttons
  # include an option to download a txt file
  st.download_button('Download the cover_letter', cover_letter_response_out)
  st.download_button('Download the resume', resume_response_out)



  