import os
import time
import cv2
import detectLanes

if __name__ == "__main__":
    for file_name in os.listdir('input'):
        if file_name.endswith('.png'):
            in_path = os.path.join('input', file_name)
            image = cv2.imread(in_path)
            start = time.time()
            processed_img = detectLanes.image_processing_pipeline(image)
            print("Time taken to process ", file_name, ": ", time.time() - start)

            out_path = os.path.join('output', file_name)
            cv2.imwrite(out_path, processed_img)
