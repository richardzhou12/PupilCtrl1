import numpy as np
import pyautogui
import math

def findCoord(dist, vec):
    # Define 5 range scale for cursor movement according to distance length
    if dist <= 0.5:
        x = 0
        y = 0
    elif dist <= 0.75: # change constant accordingly
        x = 1 * 125
        y = 1 * 70
    elif dist <= 1:
        x = 2 * 125
        y = 2 * 70
    elif dist <= 2:
        x = 3 * 125
        y = 3 * 70
    elif dist <= 2.5:
        x = 4 * 125
        y = 4 * 70
    elif dist <= 3:
        x = 5 * 125
        y = 5 * 70
    else:
        x = 0
        y = 0

    # Multiple the scaled value with unit vector
    x_vec = x * vec[0]
    y_vec = y * vec[1]
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
        pyautogui.moveRel(-x, y)
        afterpos = pyautogui.position()
    return position, afterpos
