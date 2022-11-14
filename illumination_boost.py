import numpy as np
from scipy import special
import scipy
import cv2

def  illumination_boost(Xrgb, _lambda):
    # Enhances an image illumination using the method proposed at
    # Nighttime image enhancement using a new illumination boost algorithm
    # by Al-Ameen, Zohair
    #
    # Parameters:
    #   Xrgb: RGB Image
    #   _lambda: Factor used in the equations I_3 and I_4
    # Convert image to double, even if it is already a double
    # print('before double: ', Xrgb)
    Xrgb = Xrgb.astype(np.float32)/255.0
    # print('after double: ', Xrgb)
    X = Xrgb
    # Xchannels = cv2.split(Xrgb)

    # I_5s = list()
    # for X in Xchannels:

    # Process the image with a logarithmic scaling function
    I_1 = (np.max(np.max(np.max(X))) / np.log(np.max(np.max(np.max(X))) + 1)) * np.log(X + 1)

    # Use a non-complex exponential function to modify the local constrast and attenuate the high-intensities of the input image
    I_2 = 1.0 - np.exp(-X)
    # print(I_2)
    # print(type(I_2), I_2.shape, I_2.dtype)

    # Use a LIP model, adapting it to the nature of the image, using the _lambda parameter
    I_3 = (I_1 + I_2) / (_lambda + (I_1 * I_2))
    # print(I_3)
    # print(type(I_3), I_3.shape, I_3.dtype)

    # Compute a modified CDF-HSD function to increase the brightness of dark regions in the image
    I_4 = special.erf(_lambda * np.arctan(np.exp(I_3)) - 0.5 * I_3, dtype=np.float32)

    # Apply a normalisation function, as I_4 is not in a well-defined range (almost white)
    I_5 = (I_4 - np.min(np.min(np.min(I_4)))) / (np.max(np.max(np.max(I_4))) - np.min(np.min(np.min(I_4))))

    # print('final: ', I_5)

        # I_5s.append(I_5)

    # I_res = cv2.merge(I_5s)
    I_res = (I_5*255.0).astype(np.uint8)

    return I_res