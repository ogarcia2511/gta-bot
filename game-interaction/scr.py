import numpy as np 
from PIL import ImageGrab
import cv2
import time

def capture():
    start = time.time()
    while(True):
        scr = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
        cv2.imshow('window',cv2.cvtColor(scr, cv2.COLOR_BGR2RGB))
        end = time.time()
        print(str((1 / (end - start))), " fps")
        start = time.time()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break    

if __name__ == "__main__":
    capture()