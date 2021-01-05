import cv2
import numpy as np


def rotate_img(image, angle):
    # rotates image
    # https://stackoverflow.com/questions/9041681/opencv-python-rotate-image-by-x-degrees-around-specific-point
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def get_angle(img, thresh):
    # finds needed angle
    MIN_OF_ROTATED_CONTOURS = 65
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    angle_list = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)  

        min_rect = cv2.minAreaRect(contour)
        if (min_rect[2] != round(min_rect[2])):
            angle_list.append(min_rect[2])
    if len(angle_list) <= MIN_OF_ROTATED_CONTOURS:
        return contours[0], 0
    print("All contours: ", len(contours), "Angle list: ", len(angle_list))
    return contours[0], get_angle_from_lst(angle_list)


def get_angle_from_lst(angle_list):
    # having list of angles, filters them and returns true angle
    if not angle_list:
        return 0
    angle_dict = dict()
    for i in range(len(angle_list)):
        el = round(angle_list[i])
        if el not in angle_dict:
            angle_dict[el] = 1
        else:
            angle_dict[el] += 1
    
    clean_list = []
    percentage = 70
    max_val = angle_dict[max(angle_dict, key=angle_dict.get)]
    for i in range(len(angle_list)):
        el = angle_list[i]
        round_el = round(el)
        if angle_dict[round_el] > (1 - percentage / 100) * max_val:
            clean_list.append(el)
    return sum(clean_list) / len(clean_list)
