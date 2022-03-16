# use this command to install CV2 package if not already installed: pip install cv2-python
import cv2
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import numpy as np
import os

global mood


class EmotionDetect_HaarCacasde:

    def __init__(self):
        self.fC = None
        self.eC = None
        self.eL = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.emotion = None
        self.emotionWeights = None

    def model_loading(self):
        dir = os.getcwd()
        print("Current Working Directory:", dir)

        self.fC = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eC = load_model(dir + '\\model.h5')

    def emotion_detect_run(self):

        cap = cv2.VideoCapture(0)  # start webcam capture

        while True:  # endless loop until key 'q' is pressed

            _, frame = cap.read()  # assign webcam input images to object frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert input image to grayscale for model
            faces = self.fC.detectMultiScale(gray)  # create array of faces detected through haarcascade

            for (x, y, w, h) in faces:  # for all image dimensions in each image in the faces array
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # draw box around detected face(s)
                roi_gray = gray[y:y + h, x:x + w]  # assign Region Of Interest strictly to whatever is inside above box
                roi_gray = cv2.resize(roi_gray, (48, 48),
                                      interpolation=cv2.INTER_AREA)  # resize Region Of Interest to 48x48 to work with model

                if np.sum([roi_gray]) != 0:  # if a face(s) is detected
                    roi = roi_gray.astype(
                        'float') / 255.0  # normalize by dividing Region of Intererst of by 255 (the greatest possible value when dealing with grayscale, 255=white)
                    roi = img_to_array(roi)  # place captured Region of Interest image into an array to be used by model
                    roi = np.expand_dims(roi,
                                         axis=0)  # make sure Region of Interest array is in mxn format (1xn in this case)

                    prediction = self.eC.predict(roi)[
                        0]  # use model to predict if Region of Interest image presents specific emotion
                    label = self.eL[
                        prediction.argmax()]  # take the highest probabilty of emotion detected and get self.eL index and assign it to label. ex: higest number index in [0.1335, 0.0066, 0.1249, 0.0045, 0.4689, 0.24390, .01795] is index 4 or "Neutral"
                    self.emotionWeights = prediction  # assign model prediction weights for emotion classification for extraction use
                    self.emotion = label  # assign that emotion from self.eL to self.emotion for extraction use
                    # print(self.emotion)
                    label_position = (x, y)
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                2)  # print label name near Region of Interest
                else:
                    cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                2)  # print 'No faces' if no faces are detected
            # cv2.imshow('Emotion Detector', frame)  # show box drawn and emotion identified around face(s) detected
            #if cv2.waitKey(1) & 0xFF == ord('q'):  # press 'q' key to terminate program
            break

        print('Emotion Detection Haar Cascade Finished Running')
