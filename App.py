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
orgz= st.text_input('Enter the name of the organization.')
desig = st.text_input('Enter the designation of the person who has prepared the report.')

if st.button('Submit'):
    with st.spinner('Processing.....'):
        prompt = f"""
            <ROLE>
            You are a senior structural engineer with over 20 years of professional experience in
            civil and structural engineering, specializing in building inspections, defect diagnosis,
            and remediation planning.

            <OBJECTIVE>
            Analyze the structural defects visible in the images provided by the user and prepare a
            comprehensive, professional Structural Defect Assessment Report suitable for submission
            to clients, engineers, and regulatory authorities.

            <CONTEXT>
            The user has uploaded one or more images captured at a construction or operational site.
            These images may contain one or multiple structural defects.

            REPORT STRUCTURE AND CONTENT:

            * Report Title
            - Use the exact report title provided by the user: "{title}"

            * Report Preparation Details
            - Prepared By:
                - Name: {name}
                - Designation: {desig}
                - Organization: {orgz}
            - Report Generation Date: {dt.datetime.now().date()}

            * Introduction
            - Briefly describe the purpose of the report and the scope of the assessment based on
                visual inspection of the uploaded images.

            * Identification and Classification of Structural Defects
            - Identify and clearly classify each visible defect (e.g., cracks, spalling, corrosion,
                honeycombing, settlement, moisture ingress, etc.).
            - If multiple defects are present, address each defect separately under its own heading.

            * Defect Description and Impact Assessment
            For each identified defect:
            - Provide a concise technical description.
            - Explain the potential short-term and long-term impact on structural integrity,
                durability, and safety.

            * Severity and Nature of Defects
            - Assess the severity level of each defect as:
                - Low
                - Medium
                - High
            - Indicate whether the defect is:
                - Avoidable
                - Inevitable
            - Justify the assessment briefly.

            * Recommended Remedial Measures
            For each defect:
            - Propose short-term repair measures.
            - Propose long-term corrective or preventive solutions.
            - Provide:
                - Estimated repair cost (in INR)
                - Estimated time required for implementation

            * Preventive and Precautionary Measures
            - Recommend construction, material, workmanship, or maintenance practices that can
                help prevent recurrence of similar defects in future projects.

            FORMAT AND PRESENTATION GUIDELINES:
            - Do NOT include any HTML tags such as <br>, <p>, or similar.
            - The report should be written in a formal, professional tone.
            - Use clear headings, bullet points, and tables wherever appropriate.
            - The output should be suitable for direct conversion to a Word document.
            - Ensure the report length does not exceed three pages when converted to a standard
            Word document format.

            IMPORTANT INSTRUCTIONS:
            - Base your analysis strictly on visible evidence from the images.
            - Do not assume conditions that cannot be reasonably inferred from the images.
            - Maintain clarity, conciseness, and technical accuracy throughout the report.
            - The report generated should be in word format.
            - Use bullet points and tabular format where ever possible.
            - Make sure the report does not exceeds 3 pages.
            """
        response = model.generate_content([prompt,*uploaded_image],generation_config={'temperature':0.9})
        st.write(response.text)

        
    if st.download_button(
        label = 'Click to Download',
        data = response.text,
        file_name='structual_defect_report.txt',
        mime= 'text/plain'):
        st.success('Your File is Downloaded')
        