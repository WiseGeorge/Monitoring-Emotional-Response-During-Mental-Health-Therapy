from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from FastEmotionalMonitoring import FaceDetection

FaceDetection = FaceDetection()

# class VideoTransformer(VideoTransformerBase):
#     def transform(self, frame):
#         img = frame.to_ndarray(format="bgr24")
#         #img = frame
#         img, bboxs, result, emotions = FaceDetection.findFaces(img,True)
#         return img
    
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.emotions = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img, bboxs, result, emotions = FaceDetection.findFaces(img,True)
        self.emotions = emotions
        return img

    def get_emotions(self):
        return self.emotions