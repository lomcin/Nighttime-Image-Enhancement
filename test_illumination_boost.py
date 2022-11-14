import os, sys
import cv2
import glob
from illumination_boost import *

all_files = glob.glob('./input_images/*.jpg')

for filepath in all_files:
    print(filepath)
    image = cv2.imread(filepath)
    _lambda = 4
    out = illumination_boost(image, _lambda)

    result = cv2.hconcat([image, out])
    cv2.imwrite('output_images/'+filepath[filepath.find('\\')+1:-4]+'_comparison.jpg', result)