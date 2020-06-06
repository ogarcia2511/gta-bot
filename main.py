import time
import numpy as np
import cv2
from PIL import ImageGrab

from lane_detection import detect_lanes
from game_interaction import direct_input, screen
from neural_network import alexnet

WIDTH = 160
HEIGHT = 120
LR = 1e-3

# def straight() -> None:
#     """
#     Moves the vehicle forward.
#     :return: None
#     """
#     direct_input.PressKey(direct_input.W)
#     direct_input.ReleaseKey(direct_input.A)
#     direct_input.ReleaseKey(direct_input.D)

# def left() -> None:
#     """
#     Take a left turn.
#     :return: None
#     """
#     direct_input.PressKey(direct_input.W)
#     direct_input.PressKey(direct_input.A)
#     direct_input.ReleaseKey(direct_input.D)

# def right() -> None:
#     """
#     Take a right turn.
#     :return: None
#     """
#     direct_input.PressKey(direct_input.W)
#     direct_input.PressKey(direct_input.D)
#     direct_input.ReleaseKey(direct_input.A)

# def slow_down() -> None:
#     """
#     Slow down the vehicle speed.
#     :return: None
#     """
#     direct_input.ReleaseKey(direct_input.W)
#     direct_input.ReleaseKey(direct_input.A)
#     direct_input.ReleaseKey(direct_input.D)

def straight():

    direct_input.PressKey(direct_input.W)
    direct_input.ReleaseKey(direct_input.A)
    direct_input.ReleaseKey(direct_input.D)

def left():
    direct_input.PressKey(direct_input.W)
    direct_input.PressKey(direct_input.A)
    direct_input.ReleaseKey(direct_input.D)
    time.sleep(0.05)
    direct_input.ReleaseKey(direct_input.A)

def right():
    direct_input.PressKey(direct_input.W)
    direct_input.PressKey(direct_input.D)
    direct_input.ReleaseKey(direct_input.A)
    time.sleep(0.05)
    direct_input.ReleaseKey(direct_input.D)
    

if __name__ == "__main__":
    print('Loading model...')
    model = alexnet.alexnet(WIDTH, HEIGHT, LR)
    model.load("./neural_network/models/gta-bot.model") # insert model name here

    print("Beginning algorithm...")

    for i in reversed([*range(6)]):
        print(i)
        time.sleep(1)

    END = time.time()
    while True:
        SCREEN = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
        print("Frame took ", time.time() - END, " seconds")
        END = time.time()

        SCREEN = cv2.cvtColor(SCREEN, cv2.COLOR_BGR2GRAY)
        SCREEN = cv2.resize(SCREEN, (160, 120))
        cv2.imshow('', SCREEN)

        prediction = model.predict([SCREEN.reshape(160, 120, 1)])[0]
        print(prediction)

        threshold = .90
        override = .95

        if prediction[1] > override:
            straight()
        elif prediction[0] > threshold:
            left()
        elif prediction[2] > threshold:
            right()
        else:
            straight()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break