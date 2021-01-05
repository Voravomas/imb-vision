import cv2


def cv_size(img):
    # get size of image
    return tuple(img.shape[1::-1])


def convert_colors(img, img_gray, thresh):
    # convert colors
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret2, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)
    return img, img_gray, thresh


def show_img(img):
    # show image
    cv2.imshow("image", img)
    cv2.waitKey(0)


def split_img(path):
    # split image on img, img_grey and thresh
    img = cv2.imread(path)
    # Otsu's thresholding
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret2, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return img, img_gray, thresh


def conv_thresh(img):
    # inverse img to thresh
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret2, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh