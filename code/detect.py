import cv2


def find_corr_seq(lst):
    # find most freq number
    freq_dict = dict()
    for i in range(len(lst)):
        el = lst[i]
        if el not in freq_dict:
            freq_dict[el] = 1
        else:
            freq_dict[el] += 1
    
    max_freq_key = max(freq_dict, key=freq_dict.get)
    max_freq_val = freq_dict[max_freq_key]
    
    PERCENTAGE = 50
    NUM_OF_BARS = 64
    count = 0
    for el in lst:
        if (1 - PERCENTAGE / 100) * max_freq_key <= el <= (1 + PERCENTAGE / 100) * max_freq_key:
            count += 1
        else:
            count = 0
        if count == NUM_OF_BARS:
            return max_freq_key
    return 0


def in_terms(num, avg):
    # if number is in +- equal to average by %
    PERCENTAGE = 40
    if ((1 - PERCENTAGE / 100) * avg) < num < ((1 + PERCENTAGE / 100) * avg):
        return True
    return False


def is_barcode(lst, avg):
    # if each elm in lst +- equal to average
    for el in lst:
        if not in_terms(el, avg):
            return False
    return True
  

def find_start_stop_space(pix_lst, space_lst, avg):
    # func that finds stating whitespace and finishing one between bars
    # we assume that there are 100% a barcode here
    SPACE_SIZE = 64
    was_black = False
    if pix_lst[0] == 255:
        cur_space = 1
    else:
        cur_space = 0
    # rejecting if pixel is white or not first black pixel in seq
    for i, pixel in enumerate(pix_lst):
        if pixel == 255 or was_black:
            if pixel == 255:
                if was_black:
                    cur_space += 1
                was_black = False
            continue
        # finding barcode sequence
        was_black = True
        # finding if it is barcode seq
        res = is_barcode(space_lst[cur_space: cur_space + SPACE_SIZE], avg)
        if res:
            st_space = cur_space
            fin_space = cur_space + SPACE_SIZE
            break
    return st_space, fin_space


def get_start_fin_coord(row_line, white_list, avg):
    # get starting and finishing pixels
    start, finish = find_start_stop_space(row_line, white_list, avg)

    # didn't find needed seq
    if finish == 0:
        return False

    # calculate exact pixel x for start and finish
    cur_sp = 0  # what is sp - space
    prev = row_line[0]
    pix_st = 0
    pix_fin = 0
    for i in range(1, len(row_line) - 1): # NOT SURE -1
        cur = row_line[i]
        if cur != prev and cur == 0:
            cur_sp += 1
        if cur_sp < start:
            pix_st += 1
        if cur_sp <= (finish + 1):
            pix_fin += 1
        if cur_sp == finish: # if it is time to end
            if (cur == 0 and i == (len(row_line) - 1)) or \
                (cur == 0 and row_line[i + 1] == 255):
                break
        prev = cur
    return pix_st, pix_fin
            


def detect_barcode(img):
    # main func for finding barcode on img
    num_rows = img.shape[0]
    num_cols = img.shape[1]
    CLR_SWCH = 64
    # 255 - white, but 1
    # 0 - black
    # find rows, where b/w color changes >= 65 times
    possible_rows = []
    for row in range(num_rows):
        count = 0
        prev = 255
        for col in range(num_cols):
            if img[row][col] != prev:
                count += 1
                prev = img[row][col]
        if count >= CLR_SWCH:
            possible_rows.append(row)
    
    if not possible_rows:
        return []
    
    # calculating distance between black bars
    poss_dict = dict()
    for poss_row in possible_rows:
        width_list = []
        cur_width = 0
        for col in range(num_cols):
            pixel = img[poss_row][col]
            if pixel == 255:  # white
                cur_width += 1
            elif cur_width != 0:
                width_list.append(cur_width)
                cur_width = 0
        width_list.append(cur_width)
        poss_dict[poss_row] = width_list

    found = False
    distance = -1
    found_row = -1
    for key, val in poss_dict.items():
        res = find_corr_seq(val)
        if res != 0:
            distance = res
            found_row = key
            st_fin = get_start_fin_coord(img[found_row], poss_dict[found_row], distance)
            if st_fin:
                found = True
                break
    if found:
        start_x, fin_x = st_fin
        
        # using math, and having one dot, total length and knowing that h = 0.08w
        # calculating rectangle
        w = fin_x - start_x
        x_s = start_x
        y_s = found_row - round(0.33 * (0.08 * w))
        x_f = fin_x
        y_f = found_row + round(0.66 * (0.08 * w))
        return [x_s, y_s, x_f, y_f]
    return []
