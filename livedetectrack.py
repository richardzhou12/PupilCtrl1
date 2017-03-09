import numpy as np
import cv2

# VideoCapture is the command in OpenCV for caturing video
# (0) donates the default webcam of the computer
# by changing 0 to 1 (or greater if available), we can use different webcam
cap = cv2.VideoCapture(0)

# Function of the face and eye detection
def eyedetect(image):
    # Face and eye cascading detection using opencv command (Harr-cascade detection)
    face_cascade = cv2.CascadeClassifier('C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:\opencv\sources\data\haarcascades\haarcascade_eye.xml')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # RGB to Gray

    global faces
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]  # Rectangle frame (gray image) of the face
        roi_color = image[y:y + h, x:x + w]  # Rectangle frame (RGB image) of the face
        eyes = eye_cascade.detectMultiScale(roi_gray)  # Detect eyes from the rectangle frame of face
    return faces

print 'Place user\'s face in front of camera'
while True:
    # Capture the video frame-by-frame
    ret, frame = cap.read()

    faces = eyedetect(frame)

    if np.shape(faces) == (1L, 4L):
        print 'Face Detection Successful'
        print 'Face Position: ', faces
        break

# setup initial location of window
r,h,c,w = 250,350,400,275  # simply hardcoded the values
track_window = (c,r,w,h)

# Setup the termination criteria, either 10 iteration or move by at least 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

# set up the ROI for tracking
faces = np.squeeze(faces)
roi = frame[faces]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

while True:
    # Capture the video frame-by-frame
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    # apply meanshift to get the new location
    ret, track_window = cv2.meanShift(dst, track_window, term_crit)

    # Draw it on image
    x, y, w, h = track_window
    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
    cropim = frame[y:y + h, x:x + w]

    # Display the resulting frame
    # Use 'imshow' command for each frame
    cv2.imshow('Image',frame)
    cv2.imshow('Face',cropim)

    # Since the video will keep playing
    # Add 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()