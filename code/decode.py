import cv2
import requests

def letter_identifier(img_gray, thresh):
    # locate each bar and transform pixels (bars) to letters ('A', 'F', 'D', 'T')
    eps = 1
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    result = []
    height, width = img_gray.shape
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w == width:
            continue
        if ((h >= height * (1/3) - eps) and (h <= height * (1/3) + eps)):
            result.append((x, "T"))
        elif ((h >= height - eps) and (h <= height + eps)):
            result.append((x, "F"))
        else:
            if ((y >= -1 * eps) and (y <= eps)):
                result.append((x, "A"))
            else:
                result.append((x, "D"))

    result.sort()
    # Join letters
    res_str = "".join([el[1] for el in result])
    print(len(res_str))
    assert len(res_str) == 65
    return res_str

def requester(res_str):
    # Send request to "Postal Pro" to decode IMB
    url = 'https://postalpro.usps.com/ppro-tools-api/imb/decode?imb=' + res_str
    try:
        response = requests.request('GET', url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    response = response.json()

    # Check for errors
    if response["code"] != '00':
        errText = "Error: {}\nErr_msg: {}".format(response["code"], 
                                            response["errorMessage"])
        raise(Exception(errText))
    return response
