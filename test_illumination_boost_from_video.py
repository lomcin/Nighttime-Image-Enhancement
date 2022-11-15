import os, sys
import cv2
import glob
import time
from illumination_boost_lut import *


# last frame received timestamp
prev_frame_time = 0
 
# current frame received timestamp
new_frame_time = 0

# last frame processed timestamp
prev_proc_frame_time = 0
 
# current frame processed timestamp
new_proc_frame_time = 0

# Chosen font
font = cv2.FONT_HERSHEY_SIMPLEX

# Lambda parameter
_lambda = 2

# Capturing video from camera
vc = cv2.VideoCapture('video.mp4')

while True:
    ret, img = vc.read()

    if img is not None:

        new_frame_time = time.time()

        prev_proc_frame_time = time.time()
        out = illumination_boost(img, _lambda)
        new_proc_frame_time = time.time()
        processing_time = str(int(1000*(new_proc_frame_time - prev_proc_frame_time))) + ' ms'

        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = str(int(fps)) + ' fps'
    
        # putting the FPS count on the original image
        cv2.putText(img, fps, (7, 20), font, 0.5, (100, 255, 0), 1, cv2.LINE_AA)

        # putting the processing time on the out image
        cv2.putText(out, processing_time, (7, 20), font, 0.5, (255, 100, 0), 1, cv2.LINE_AA)

        result = cv2.hconcat([img, out])

        cv2.imshow('Original image and Boosted', result)
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break
vc.release()
cv2.destroyAllWindows()