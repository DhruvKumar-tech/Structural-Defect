import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# Configure the model
gemini_api_key = os.getenv('GOOGLE_API_KEY2')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Create Sidebar for image upload
st.sidebar.title(':red[Upload the Images Here:]')
uploaded_image = st.sidebar.file_uploader('Images',type=['jpeg','png','jfif','jpg'],accept_multiple_files=True)
uploaded_image = [Image.open(ing) for ing in uploaded_image] 
if uploaded_image:
    st.sidebar.success('Image has been uploaded succesfully')
    st.sidebar.subheader(':blue[Uploaded Images]')
    st.sidebar.image(uploaded_image)

# Lets create the main page
st.title(':orange[STRUCTUAL DEFECT:-] :green[AI Assisted Structural Defect Identifier]')
st.markdown('#### :blue[This application takes images of the structual defects from the construction site and prepare the AI assisted report.]')
title = st.text_input('Enter the Title of the report:')
name = st.text_input('Enter the name of person who has prepared the report.')
organization = st.text_input('Enter the name of the organization.')
desig = st.text_input('Enter the designation of the person who has prepared the report.')

if st.button('Submit'):
    with st.spinner('Processing.....'):
        prompt = f'''
            <role> You are an expert structural engineer with 20 + years of experience.
            <Goal> You need to prepare a detailed report on the structural defect shown in the images provided by the user.
            <Context> Images are shared by the user has been attached.
            <Format> Follow the steps belowfollo:
            * Add title at the top of the report. The title provided by the user {title}
            * Next add name, designation and organization of a person who has prepared the report also include the report generation date: 
            Following are the details provided by the user
            name: {name}
            designation: {desig}
            organization: {organization}
            date: {dt.datetime.now().date()}
            * Identify and classify the defect for eg: crack, spalling, 
            * There could be more than one defects in images. Identify all defects seperately
            * For each defect identified, provide a short description of the defect and its potential empact on the structure
            * For each defect measure the sevierity as low medium or high. Along mention if the defect is inviatable and avoidable
            * Provide the short term and long term solution for the repair
            * What precaunary measures can be taken to avoid these in future
            
            <Instruction>
            * Do not include format like br and others.
            * The report generated should be in word format.
            * Use bullet points and tabular format where ever possible.
            * Make sure the report does not exceeds 3 pages.'''
        response = model.generate_content([prompt,*uploaded_image],generation_config={'temperature':0.9})
        st.write(response.text)

        
    if st.download_button(
        label = 'Click to Download',
        data = response.text,
        file_name='structual_defect_report.txt',
        mime= 'text/plain'):
        st.success('Your File is Downloaded')
        