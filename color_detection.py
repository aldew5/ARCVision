import numpy as np
import cv2


def detect_red(image):
    # define the lower and upper BGR (represented in reverse order) for red
    red_boundary = ([17, 15, 100], [50, 56, 200])


    lower = np.array(red_boundary[0], dtype="uint8")
    upper = np.array(red_boundary[1], dtype="uint8")
        
    # find the colors within the specified boundaries and apply the mask
    # binary mask with values of 255 for pixels that fall in the specified range and
    # values of 0 for pixels that do not
    mask = cv2.inRange(image, lower, upper)
    # convert into an output image
    output = cv2.bitwise_and(image, image, mask=mask)
    
    cnt = 0
    for row in mask:
        for i in row:
            if i == 255:
                cnt += 1
    return cnt >= 3000





