import numpy as np
import pyautogui
import math

def findCoord(dist, vec):
    # Define 4 range scale for cursor movement according to distance length

    if dist <= 4.5:
        dist = 0
    elif dist <= 9:
        dist *= 10
    elif dist <= 20:
        dist *= 25
    else:
        dist = 0

    # Multiple the scaled value with unit vector
    x_vec = dist * vec[0]
    y_vec = dist * vec[1]
    return x_vec, y_vec

def move(x, y):
    if math.isnan(x):
        position = (0, 0)
        afterpos = (0, 0)
    elif math.isnan(y):
        position = (0, 0)
        afterpos = (0, 0)
    else:
        position = pyautogui.position()
        # The x-direction is reversed in the camera
        pyautogui.moveRel(x, -y)
        afterpos = pyautogui.position()
    return position, afterpos

def click(flag):
    if flag == 0:
        pass
    elif flag == 5:
        pyautogui.click()
    elif flag == 10:
        pyautogui.click()
        pyautogui.click()
    else:
        pass