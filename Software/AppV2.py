import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import altair as alt
import time
from PIL import Image
from datetime import date
import cv2
from scipy import stats
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from FastEmotionalMonitoring import FaceDetection
import Patient_Manager as pm

#pm.create_patients_table()


class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        #img = frame
        img, bboxs, result, emotions = FaceDetection.findFaces(img,True)
        return img



pTime = 0
cTime = 0

#Streamlit Config Functions
#image = Image.open("../Images/Icon.jpg")
st.set_page_config(page_title='Dashboard', page_icon = '😀', layout='wide')
# Initialize the session state variable
if 'webcam_in_use' not in st.session_state:
    st.session_state['webcam_in_use'] = False

def get_available_cameras():
    available_cameras = []
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

def plotc_emotions(emotions):
    # Convert the emotions dictionary into a DataFrame
    data = pd.DataFrame(emotions.items(), columns=['Emotion', 'Value'])
    
    # Map emotions to x and y coordinates
    coordinates = {
        'angry': (-1, 1),
        'disgust': (-1, -1),
        'fear': (1, -1),
        'happy': (1, 1),
        'neutral': (0, 0),
        'sad': (-1, 0),
        'surprise': (1, 0)
    }
    
    data['x'] = data['Emotion'].map(lambda e: coordinates[e][0])
    data['y'] = data['Emotion'].map(lambda e: coordinates[e][1])
    
    # Create a scatter plot with Altair
    chart = alt.Chart(data).mark_point().encode(
        x='x',
        y='y',
        size='Value'
    )
    
    # Display the chart in the Streamlit app
    st.altair_chart(chart, use_container_width=True)



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
        

# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         </style>
#     """
# st.markdown(hide_menu_style, unsafe_allow_html=True)


image1 = Image.open("../Images/mental.jpg")
image2 = Image.open("../Images/brain.jpg")
image3 = Image.open("../Images/psi.png")
image4 = Image.open("../Images/pro1.jpg")


st.title("**Monitoring Emotional Response During Mental Health Therapy**")


st.write('---')

with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Home","Emotion Tracking", "About"],
        icons = ["house","bar-chart-line-fill", "activity","window-dock","book", "envelope"],
        menu_icon = "image-alt ",
        default_index = 0,
        orientation = "vertical",
    )

st.image(image4, use_column_width=True)

if selected=='Home':
    pass

if selected=='Emotion Tracking':
    detval = 0.5
    with st.sidebar:
        cams = get_available_cameras()
        cam = st.selectbox('Available Cameras',cams)
        detector_backend = st.selectbox('**Select Detector Backend**', ['Mediapipe', 'OpenCV', 'RetinaFace', 'MTCNN', 'SSD', 'DLIB'])
        detector_backend = detector_backend.lower()
    detector = FaceDetection()
    
    mcont = st.container()
    form_container = st.container()
   
    with mcont:
        col1,col2,col3 = st.columns([3,6,3])
        with col2:
            st.write('### **⬇️⬇️Real Time Emotion Tracking⬇️⬇️**')
            stframe = st.empty()
            st.write('---')
            

    with st.sidebar:
        st.subheader('Patient Information')
        with st.expander('Form'):
            succ, metadata = patient_form()
            if succ:
                print(metadata)
                dictpat = {
                            'id': metadata[3],
                            'firstname': metadata[0],
                            'lastname': metadata[1],
                            'description': metadata[2],
                            }
                df = pd.DataFrame(dictpat,index=[0,1,2,3])
                df.to_json(f'../PatientsTemporalData/patient.json')


        webcam_button_label = 'Webcam'
        webcam_button = st.button(webcam_button_label,type='primary')
        stother = st.empty()

        if webcam_button:
            if st.session_state['webcam_in_use']:
                # Stop the webcam
                st.session_state['webcam_in_use'] = False
            else:
                # Start the webcam
                cap = cv2.VideoCapture(cam)
                st.session_state['webcam_in_use'] = True
                emotions = ''
                
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))

                while cap.isOpened():
                    
                    succes, img = cap.read()
                    if not succes:
                        continue
                    img, bboxes, emotion, emotionss = detector.findFaces(img,True,detector_backend=detector_backend)
                    print(emotionss)
                    emotions += f'{emotion}, '
                    emotionList = [word.strip() for word in emotions.split(',')]
                    my_array = np.array(emotionList)
                    mode = stats.mode(my_array)
                    df = pd.DataFrame(emotionList)
                    
                    df.to_json(f'../PatientsTemporalData/emotion.json')

                    # Time Management
                    cTime = time.time()
                    fps = 1/(cTime-pTime)
                    pTime = cTime
                    
                    #cv2.putText(img, f'FPS: {int(fps)}', (10,30), cv2.FONT_HERSHEY_PLAIN, 2.5, (75,255,55),2)
        
                    stframe.image(img, channels='BGR',use_column_width=True)
                    stother.metric('FPS',int(fps))
                    
                    ### Plot Graphics -----------------
                    # with st.sidebar:
                    #     with stother:
                    #         plot_emotions(emotionss)
                   
                    cv2.waitKey(1)  

                    if not st.session_state['webcam_in_use']:
                        emotionList = [word.strip() for word in emotions.split(',')]
                        my_array = np.array(emotionList)
                        mode = stats.mode(my_array)
                        print(metadata)
                        print(emotionList)
                        df = pd.read_json(('PatientsTemporalData/patient.json'))
                        df.to_excel('work.xlsx')
                        #df = pd.DataFrame(dictpat)
                        #df.to_json(f'Patient{id}.json')
                        pm.insert_patient(metadata[3],metadata[0], metadata[1],metadata[2],emotions, mode)
                        break
        