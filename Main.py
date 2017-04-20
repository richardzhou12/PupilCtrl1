import numpy as np
import cv2
import FaceDetect
import EyeDetect
import CursorMove
import pyautogui

# VideoCapture is the command in OpenCV for caturing video
# (0) donates the default webcam of the computer
# by changing 0 to 1 (or greater if available), we can use different webcam
cap = cv2.VideoCapture(1)
print 'Place user\'s face in front of camera'
while True:
    # Capture the video frame-by-frame
    ret, frame = cap.read()

    faces = FaceDetect.facedetect(frame)

    if np.shape(faces) == (1L, 4L):
        print 'Face Detection Successful'
        print 'Face Initial Position: ', faces
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

# Initialization for the loop
roi_eye_hist = np.zeros((1, 4))
pupil_hist = np.zeros((1, 4))
center_hist = np.zeros((1, 2))
loop = 0

# Initialize cursor position
pyautogui.moveTo(640,320) # centerpoint for (1280, 720) screen size

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
    cropface = frame[y:y + h, x:x + w]

    cropface, roi_eye, flag = EyeDetect.eyedetect(cropface)

    # If there are not detection for eye in this iteration
    # Use the saved location from last iteration
    if flag == 0:
        roi_eye = roi_eye_hist
        pupil = pupil_hist
        print 'Eye Signal Lost'
    else:
        # Pupil Thresholding
        pupil = EyeDetect.pupilthreshold(roi_eye)
        # Find the centroid of the pupil
        cimage, contours, hierarchy = cv2.findContours(pupil, 1, 2)
        if len(contours) > 0:
            cnt = contours[0]
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(pupil, center, radius, 170, 2)
            # Calculate the distance movement from each frame
            dist, direc = EyeDetect.distcalc(center, center_hist)
            center_hist = center
            #print (dist, direc)
            x_vec, y_vec = CursorMove.findCoord(dist, direc)
            print (x_vec, y_vec)
            #CursorMove.move(x_vec, y_vec)
        else:
            print "Sorry No contour Found."

    roi_eye_hist = roi_eye
    pupil_hist = pupil

    # Record the loop number
    loop = loop + 1

    # Display the resulting frame
    # Use 'imshow' command for each frame
    cv2.imshow('Image', frame)
    cv2.imshow('Face', cropface)
    cv2.imshow('Eye', roi_eye)
    cv2.imshow('Pupil', pupil)


    # Since the video will keep playing
    # Add 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print "The System has run ", loop, " times"
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
