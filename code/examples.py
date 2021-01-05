import cv2


def example1():
    IMG_NAME = "imbs/0.png"
    img, img_gray, thresh = split_img(IMG_NAME)
    show_img(img)
    # img, img_gray, thresh = cutting_pixels(img, img_gray, thresh)
    letter_str = letter_identifier(img_gray, thresh)
    responce = requester(letter_str)
    fin_str = output_res(responce)
    print(fin_str)


def example2():
    # simple angle turning
    IMG_NAME = "imb_practice/p1.png"
    img, img_gray, thresh = split_img(IMG_NAME)
    show_img(img)
    img = rotate_img(img, thresh)
    show_img(img)


def example3():
    # angle turning and detecting barcode
    IMG_NAME = "imb_practice/p2.png"
    img, img_gray, thresh = split_img(IMG_NAME)
    show_img(img)
    img = rotate_img(img, thresh)
    img, img_gray, thresh = convert_colors(img, img_gray, thresh)
    res = detect_barcode(thresh)
    if res:
        FRAME_SIZE = 3
        cv2.rectangle(img, (res[0] - FRAME_SIZE, res[1] - FRAME_SIZE), \
            (res[2] + FRAME_SIZE, res[3] + FRAME_SIZE), (0, 255, 0), 2)
    show_img(img)