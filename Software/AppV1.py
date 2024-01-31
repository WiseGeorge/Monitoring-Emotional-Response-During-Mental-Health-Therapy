import numpy as np
import cv2
import streamlit as st
from tensorflow import keras
from keras.models import model_from_json
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes
from VideoTransform import VideoTransformer as VT
from FastEmotionalMonitoring import FaceDetection
from streamlit_option_menu import option_menu
import pandas as pd
import altair as alt
import time
from PIL import Image
from datetime import date
from scipy import stats
import Patient_Manager as pm


FaceDetection = FaceDetection()


def patient_form():
    with st.form(key='patient_form'):
        st.write('Please enter patient information:')
        first_name = st.text_input('First Name')
        last_name = st.text_input('Last Name')
        patient_id = st.text_input('Patient ID')
        description = st.text_area('Description')
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            st.write(f'Patient information submitted: {first_name} {last_name}, ID: {patient_id}, Description: {description}')
            return True, (first_name, last_name, patient_id, description)
        else:
            return False, None
        

def plot_emotions(emotions):
    # Convierte el diccionario de emociones en un DataFrame
    data = pd.DataFrame(emotions.items(), columns=['Emotion', 'Value'])
    # Agrega una columna con los colores para cada emoción
    colors = {
    'angry': 'red',
    'disgust': 'green',
    'fear': 'purple',
    'happy': 'yellow',
    'neutral': 'gray',
    'sad': 'blue',
    'surprise': 'orange'
}

    data['Color'] = data['Emotion'].map(colors)
    
    # Crea un gráfico de barras con Altair
    chart = alt.Chart(data).mark_bar().encode(
        x='Emotion',
        y='Value',
        color=alt.Color('Color', scale=None)
    )
    
    # Muestra el gráfico en la aplicación Streamlit
    st.altair_chart(chart, use_container_width=True)




# Page Config
st.set_page_config(page_title='Dashboard', page_icon = '😀', layout='wide')

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Images
image1 = Image.open("../Images/mental.jpg")
image2 = Image.open("../Images/brain.jpg")
image3 = Image.open("../Images/psi.png")
image4 = Image.open("../Images/pro1.jpg")



with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Home","Emotion Tracking", "Patient Information (🛠️)","About"],
        icons = ["house","bar-chart-line-fill", "activity","window-dock","book", "envelope"],
        menu_icon = "image-alt ",
        default_index = 0,
        orientation = "vertical",
    )

if selected=='Home':
    st.title("**Monitoring Emotional Response During Mental Health Therapy**")
    st.write('---')
    st.image(image4, use_column_width=True)
    st.write('## 🚧 Work in Progress 🚧')
    st.write('- Welcome to the **Experimental Version** of our application.')
    
    st.write("""##### We're building an innovative system that monitors emotional responses during mental health sessions. This system is powered by Python, OpenCV, Deepface, and Streamlit. It's designed to detect and analyze patient emotions in real-time during a session, offering invaluable insights for mental health professionals. Our advanced technology stack ensures accurate and efficient monitoring of emotional responses. We're also working on integrating a spreadsheet system for specialists to record patient data. The data collected will be used to generate personalized reports for each patient, providing a comprehensive overview of the information obtained.""")
    
    st.write('### 📚 Fast Facial Emotion Monitoring (FFEM)')
    st.write("""Our application utilizes the FFEM package, a powerful tool developed by the authors for Facial Emotion Recognition (FER). FFEM employs sophisticated techniques and algorithms to detect and classify emotions from facial expressions.
    \nFFEM: https://pypi.org/project/FFEM/. 
    \nDesigned with user-friendliness in mind, FFEM simplifies the complex task of FER, making it accessible and straightforward for users. Whether you're a researcher, a developer, or someone interested in FER, FFEM can be an invaluable tool for your projects.""")
    
    st.write('### ⏳ Coming Soon: Patient Information Section')
    st.write('Stay tuned! We are currently developing the Patient Information section to enhance our application.')

if selected=='Emotion Tracking':
    col1,col2,col3 = st.columns([3,6,3])
    with col2:
        st.header("Webcam Live Feed")
        st.write("Click on start to use webcam and detect your face emotion")
        VTT = VT()
        webrtc_streamer(key="example", video_transformer_factory=VT, video_html_attrs=VideoHTMLAttributes( autoPlay=True, controls=True, style={"width": "100%"}, muted=True ))
        if VTT.get_emotions() is not None:
            st.write(VTT.get_emotions())

if selected=='Patient Information (🛠️)':
    st.header('🛠️This Section is Under Construction.')
    with st.sidebar:
        sp = st.selectbox('Patient Manager',['Personal Information','Results Analysis'])
    if sp == 'Personal Information':
        col1,col2,col3 = st.columns([3,6,3])
        with col2:
            with st.expander('Personal'):
                patient_form()
    if sp == 'Results Analysis':
        pass

if selected == 'About':
    st.write("""
        # About the Autor
        - #### Developer: Jorge Felix Martinez Pazos
        - #### University of Informatics Science, La Habana, Cuba
        - #### Gmail: jorgito16040@gmail.com
        - #### Telegram: https://t.me/Wise_George
        - #### Linkedin: https://www.linkedin.com/in/wisegeorgie/
        - #### GitHub: https://github.com/Jorgito58
    """)



