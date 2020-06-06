import time
import numpy as np
import cv2
from os import path
from PIL import ImageGrab

from game_interaction import screen, keylogger

DIR = "./neural_network/training/"
FILE = "train-1.npy"
FULLPATH = path.join(DIR, FILE)
data = []

def key_to_arr(keys):
    out = [0, 0, 0]

    # left = 0, straight = 1, right = 2

    if 'A' in keys:
        out[0] = 1
    elif 'W' in keys:
        out[1] = 1
    elif 'D' in keys:
        out[2] = 1

    return out

def set_file():
    if path.exists(FULLPATH):
        data = list(np.load(FULLPATH))

def save_to_file(data):
    np.save(FULLPATH, data)

if __name__ == "__main__":
    print("Beginning data generation...")

    for i in reversed([*range(6)]):
        print(i)
        time.sleep(1)

    while True:
        SCREEN = screen.capture((0, 40, 800, 640))
        SCREEN = cv2.cvtColor(SCREEN, cv2.COLOR_BGR2GRAY)
        SCREEN = cv2.resize(SCREEN, (160, 120))
        KEYS = keylogger.get()
        OUTPUT = key_to_arr(KEYS)

        data.append([SCREEN, OUTPUT])

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        if len(data) % 1000 == 0:
            print("Data Points: ", len(data))
            save_to_file(data)
