import os, sys
import cv2
import glob
from illumination_boost import *


vc = cv2.VideoCapture(0)
while True:
    ret, img = vc.read()
    _lambda = 2
    out = illumination_boost(img, _lambda)
    result = cv2.hconcat([img, out])

    cv2.imshow('Webcam and Boosted', result)
    if cv2.waitKey(1) == ord('q'):
        break
vc.release()
cv2.destroyAllWindows()