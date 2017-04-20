import numpy as np
import cv2


def facedetect(image):
    # Face and eye cascading detection using opencv command (Harr-cascade detection)
    face_cascade = cv2.CascadeClassifier('C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # RGB to Gray

    faces = face_cascade.detectMultiScale(gray, 1.5, 5)
    return faces
