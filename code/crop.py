import cv2
import numpy as np


def crop_all(img, img_grey, thresh, coords, frame_size):
    # func that crops img, img_grey, thresh by coords and then applies more
    # crop to make img as small as possible
    img = img[(coords[1] - frame_size):(coords[3] + frame_size),
                (coords[0] - frame_size):(coords[2] + frame_size)]
    img_grey = img_grey[(coords[1] - frame_size):(coords[3] + frame_size),
                (coords[0] - frame_size):(coords[2] + frame_size)]
    thresh = thresh[(coords[1] - frame_size):(coords[3] + frame_size),
                (coords[0] - frame_size):(coords[2] + frame_size)]
    white_pixels = np.array(np.where(thresh == 0))
    
    mn = np.min(white_pixels, axis=1)
    mx = np.max(white_pixels, axis=1)
    img = img[mn[0]:mx[0], mn[1]:mx[1]]
    img_grey = img_grey[mn[0]:mx[0], mn[1]:mx[1]]
    thresh = thresh[mn[0]:mx[0], mn[1]:mx[1]]
    return img, img_grey, thresh
