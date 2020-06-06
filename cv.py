import time
import numpy as np
import cv2
from PIL import ImageGrab

from lane_detection import detect_lanes
from game_interaction import direct_input

def straight() -> None:
    """
    Moves the vehicle forward.
    :return: None
    """
    direct_input.PressKey(direct_input.W)
    direct_input.ReleaseKey(direct_input.A)
    direct_input.ReleaseKey(direct_input.D)

def left() -> None:
    """
    Take a left turn.
    :return: None
    """
    direct_input.PressKey(direct_input.A)
    direct_input.PressKey(direct_input.W)
    time.sleep(0.1)
    direct_input.ReleaseKey(direct_input.W)
    direct_input.ReleaseKey(direct_input.D)
    direct_input.ReleaseKey(direct_input.A)

def right() -> None:
    """
    Take a right turn.
    :return: None
    """
    direct_input.PressKey(direct_input.D)
    direct_input.PressKey(direct_input.W)
    time.sleep(0.1)
    direct_input.ReleaseKey(direct_input.A)
    direct_input.ReleaseKey(direct_input.W)
    direct_input.ReleaseKey(direct_input.D)

def slow_down() -> None:
    """
    Slow down the vehicle speed.
    :return: None
    """
    direct_input.ReleaseKey(direct_input.W)
    direct_input.ReleaseKey(direct_input.A)
    direct_input.ReleaseKey(direct_input.D)


if __name__ == "__main__":
    print("Beginning algorithm...")

    for i in reversed([*range(6)]):
        print(i)
        time.sleep(1)

    END = time.time()
    while True:
        SCREEN = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
        print("Frame took ", time.time() - END, " seconds")
        END = time.time()
        NEW_SCREEN, LEFT_SLOPE, RIGHT_SLOPE = detect_lanes.image_processing_pipeline(SCREEN)
        cv2.imshow('processed', NEW_SCREEN)

        # Comment out the line below if want to see only lines drawn image
        # cv2.imshow('window', cv2.cvtColor(SCREEN, cv2.COLOR_BGR2RGB))

        print(LEFT_SLOPE, RIGHT_SLOPE)
        # if LEFT_SLOPE < 0 and RIGHT_SLOPE < 0:
        #     print("Command: RIGHT")
        #     # right()
        # elif LEFT_SLOPE > 0 and RIGHT_SLOPE > 0:
        #     print("Command: LEFT")
        #     # left()
        # else:
        #     print("Command: STRAIGHT")
        #     # straight()

        if abs(LEFT_SLOPE) > abs(RIGHT_SLOPE):
            print("Command: RIGHT")
            right()
        elif abs(RIGHT_SLOPE) > abs(LEFT_SLOPE):
            print("Command: LEFT")
            left()
        else:
            print("Command: STRAIGHT")
            straight()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    