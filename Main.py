import numpy as np
import cv2
import FaceDetect
import EyeDetect
import CursorMove
import pyautogui
import dlib

# VideoCapture is the command in OpenCV for caturing video
# (0) donates the default webcam of the computer
# by changing 0 to 1 (or greater if available), we can use different webcam
cap = cv2.VideoCapture(1)

# Initializations
predictor = dlib.shape_predictor("C:\Python27\Lib\site-packages\dlib\shape_predictor_68_face_landmarks.dat")
expected = [43, 44]
poi = (0, 0)
poi_hist = (0, 0)
loop = 0
flag = 0
pyautogui.moveTo(960, 540) # centerpoint for (1920, 1080) screen size

while True:
    # Capture the video frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    # faces = FaceDetect.facedetect(gray)
    faces = FaceDetect.facedetect(frame)
    print("Face Detected!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        temp = frame[y:y + h, x:x + w]
        cropface = temp.copy()
        cropface, roi_eye, flag = EyeDetect.eyedetect(cropface, flag)
        # Dlib rectangle
        dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        detected_landmarks = predictor(frame, dlib_rect).parts()
        landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])
        # copy the frame so we can add features for a better view
        image = frame.copy()

        for idx, point in enumerate(landmarks):
            pos = (point[0, 0], point[0, 1])
            # print pos
            # annotate the positions
            if idx in expected:
                cv2.putText(image, str(idx), pos,
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.4,
                            color=(0, 0, 255))
                if loop <= 5:
                    pass
                else:
                    if idx == 43: # 43 -> expeceted
                        poi = pos;
                    # draw points on the landmark positions
                    cv2.circle(image, pos, 3, color=(0, 255, 255))

    dist, direc = EyeDetect.distcalc(poi, poi_hist)
    x_vec, y_vec = CursorMove.findCoord(dist, direc)
    # Add cursor control (move and click)
    CursorMove.move(x_vec, y_vec)
    if flag != 0 and flag < 12:
        print("Hold for one click:", flag, "(5 -> single click; 11 -> double click)")
        if flag == 5:
            CursorMove.click(flag)
            print("Clicked")
        elif flag == 11:
            CursorMove.click(flag)

    # Save variable for this iterationq
    poi_hist = poi
    loop += 1
    # cv2.imshow("Faces found", frame)
    cv2.imshow("Lanqdmarks found", image)
    cv2.imshow("Eye", cropface)
    # Since the video will keep playing
    # Add 'r' to reset the program
    if cv2.waitKey(1) & 0xFF == ord('r'):
        pyautogui.moveTo(960, 540)
    # Add 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print "The System has run ", loop, " times"

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()