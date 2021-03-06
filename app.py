import numpy as np
import cv2
import streamlit as st
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, VideoProcessorBase, WebRtcMode

# load model
emotion_dict = ["Angry","Disgust","Fear","Happy","Neutral","Sad","Surprise"]

classifier =load_model("custom_model_result.h5")

# load weights into new model
classifier.load_weights("custom_model_result.h5")

#load face
try:
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
except Exception:
    st.write("Error loading cascade classifiers")
# Change
RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
# change end

#  change - class VideoTransformer(VideoTransformerBase):
class Faceemotion(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        #image gray
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            image=img_gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img=img, pt1=(x, y), pt2=(
                x + w, y + h), color=(255, 0, 0), thickness=2)
            roi_gray = img_gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                prediction = classifier.predict(roi)[0]
                maxindex = int(np.argmax(prediction))
                finalout = emotion_dict[maxindex]
                output = str(finalout)
            label_position = (x, y)
            cv2.putText(img, output, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return img

def main():
    
    # Face Analysis Application #
    st.title(" Welcome to Real Time Face Emotion Detection ")
    activiteis = ["Home","About","Contact Us","Debug here"]
    choice = st.sidebar.selectbox("Select Activity", activiteis)
    
  
    if choice == "Home":
        html_temp_home1 = """<div style="background-color:DarkRed";padding:10px">
                                            <h4 style="color:white;text-align:center;">
                                            Start Your Real Time Face Emotion Detection.</h4>
                                            </div>
                                            </br>"""

        st.markdown(html_temp_home1, unsafe_allow_html=True)

        selectbox = st.selectbox("Select Yes to continue",["Please Select","Yes", "No"])
        #st.write(f"You selected {selectbox}")
        if selectbox == "Yes":
            st.subheader("Webcam Live Feed")
            st.write("1. Click Start to access your webcam")
            st.write("2. This predicts one's different emotions.")
            st.write("3. When finished, click STOP to end.")
            #  change - webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)
            webrtc_streamer(key="example", mode=WebRtcMode.SENDRECV, rtc_configuration=RTC_CONFIGURATION,video_processor_factory=Faceemotion)
            
        elif selectbox == "No":
            st.info("This is fun, try once!. You'll love it")
            st.caption("Thanks for Visiting!")
        else:
            pass
    
    elif choice == "About":

        st.subheader("About This App")
        html_temp4 = """
                                    <div style="background-color:DarkRed;padding:10px">
                                    <h4 style="color:white;text-align:center;">Sharath Diwakar created this demo application. </h4>
                                    </div>
                                    <br></br>
                                    <br></br>"""
        st.markdown(html_temp4, unsafe_allow_html=True)
        st.caption("Thank You for Visiting")

    elif choice == "Contact Us":
        st.header("Contact Details")
        with st.form(key='my_form'):
            text_input = st.text_input(label='Enter Your Message Here')
            submit_button = st.form_submit_button(label='Submit')

                              
        st.subheader("""Email Ids""")
        st.info(""">* Sharath Diwakar : mailmesharathd@gmail.com""")

        st.subheader(""" LinkedIn Profile""")     
        st.info(""">* [Sharath Diwakar] (https://www.linkedin.com/in/sharathdiwakar2020/)""")
         
        html_temp_copyright = """
        <body style="background-color:red;">
        <div style="background-color:DarkRed ;padding:0.25px">
        <h3 style="color:white;text-align:center;">Copyright ?? 2022 | Sharath Diwakar </h3>
        </div>
        </body>
        """
        st.markdown(html_temp_copyright, unsafe_allow_html=True)

    elif choice == "Debug here":
        st.error('''Could not start the video source??''')
        st.info('''
                    > * Click on start to access webcam.
                    > * Allow browser to access webcam
                    > * If you have more than one device, select the device.
                    > * Make sure, any other application not using the webcam.
                    > * Change the privacy settings of the webcam.
                    > * Still unable to access, Contact me.
                    
                 ''')  
    else:
        pass

    # Set footer
    footer="""<style> a:link , a:visited{color: blue;background-color: transparent;text-decoration: underline;} 
    a:hover,  a:active {color: red;background-color: transparent;text-decoration: underline;}
    .footer {position: fixed;left: 0;bottom: 0;width: 100%;background-color: white;color: black;text-align: center;}
    </style><div class="footer"><p>Developed by Sharath Diwakar</p> </div>"""
    st.markdown(footer,unsafe_allow_html=True)
    


if __name__ == "__main__":
    main()
