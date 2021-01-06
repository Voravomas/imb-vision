import cv2
from etc import split_img, convert_colors, conv_thresh, show_img
from turn import get_angle, rotate_img
from detect import detect_barcode
from crop import crop_all
from decode import letter_identifier, requester


def output_res(response):
    # Clear received data
    info = response["info"]

    barcode_id = info[:2]
    spec_services = info[2:5]
    mailer_id = info[5:11]
    serial_num = info[11:]
    delivery_zip = response["zip"]

    # Print decoded info and image
    fin_result = ("Barcode ID:\t\t\t\t{}\nSpecial Services:\t\t\t{}\n" + \
                "Mailer ID:\t\t\t\t{}\nSerial Number:\t\t\t\t{}\n" + \
                "Delivery Point ZIP Code:\t\t{}").format(barcode_id, spec_services, 
                                                    mailer_id, serial_num, 
                                                    delivery_zip)
    return fin_result

def pipeline(IMG_PATH):
    # break image into 3 parts
    img, img_gray, thresh = split_img(IMG_PATH)
    contour, angle = get_angle(img, thresh)
    img, img_gray, thresh = split_img(IMG_PATH)

    #show what image was taken
    show_img(img)

    # rotate image if needed
    img = rotate_img(img, angle)

    # detect barcode
    img, img_gray, thresh = convert_colors(img, img_gray, thresh)
    res = detect_barcode(thresh)
    if not res:
        print("NOT FOUND")
        return -1
    # crop image
    FRAME_SIZE = 3
    img, img_gray, thresh = crop_all(img, img_gray, thresh, res, FRAME_SIZE)
    #thresh for final presentation
    pic_thresh = thresh
    thresh = conv_thresh(img)
    # decode image to letters
    letter_str = letter_identifier(img_gray, thresh)
    # send request and process it
    responce = requester(letter_str)
    fin_str = output_res(responce)
    # show result
    print(fin_str)
    show_img(pic_thresh)


def main():
    IMG_PATH = "../pictures/imb_practice/p2.png"
    pipeline(IMG_PATH)

main()