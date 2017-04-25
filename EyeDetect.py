import numpy as np
import cv2


def eyedetect(image, flag):
    eye_cascade = cv2.CascadeClassifier('C:\opencv\sources\data\haarcascades\haarcascade_righteye_2splits.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    halfgray = gray[:, 1:120]

    eyes = eye_cascade.detectMultiScale(halfgray, 1.5, 5)
    if np.shape(eyes) == (0L,):
        roi_eyes = np.zeros((2, 4))
        flag += 1
    else:
        oneeye = eyes[0, :]
        oneeye[2] = 90
        oneeye[3] = 90
        [ex, ey, ew, eh] = oneeye
        ex = ex - 10
        ey = ey - 10
        if ex < 0:
            ex = 0
        if ey < 0:
            ey = 0
        cv2.rectangle(image, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        roi_eyes = image[(ey):(ey+eh), (ex):(ex+ew)]
        flag = 0
    return image, roi_eyes, flag


def pupilthreshold(image):
    # Apply adaptive mean thresholding
    # (Because the lighting condition will change)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im = cv2.medianBlur(gray, 5)
    ret, thres_im = cv2.threshold(im, 35, 255, cv2.THRESH_BINARY_INV)
    return thres_im


def distcalc(x, y):
    # Calculate the distance between two point in a image
    x = np.squeeze(x)
    y = np.squeeze(y)
    dis_x = x[0] - y[0]
    dis_y = x[1] - y[1]
    temp = dis_x**2 + dis_y**2
    distance = np.sqrt(temp)
    if distance == 0:
        uni_vec = (0, 0)
    else:
        uni_vec = (y - x) / distance
    return distance, uni_vec