import cv2
import numpy as np
import imutils
import json


# make it easier to show image later
def shw_img(image):
    cv2.imshow('', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# extract the conor points
def extract_extreme_points(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([35, 43, 46])  # extract the low value of color
    high_hsv = np.array([77, 255, 255])  # extract the high value of color
    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=high_hsv)

    # blur the mask to improve the contour detect precision
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # compute the center of the contour
    corner_coordinates = []
    for c in cnts:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        corner_coordinates.append([cX, cY])
    return corner_coordinates

def extract_corner(surface_name):
    output_dir = 'Surface_' + surface_name
    # img pre-process
    file_name = output_dir + '/' + surface_name + '_crop.png'
    img = cv2.imread(file_name)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

    # find contours
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # draw contours
    bgr_white = np.ones((img.shape[0], img.shape[1]), dtype=np.uint8) * 255
    cnt_img = cv2.drawContours(bgr_white, contours, contourIdx=1, color=(0, 0, 0), thickness=1)
    save_grid_bound_name = output_dir + '/' + 'grid_bound.png'
    cv2.imwrite(save_grid_bound_name, cnt_img)

    # the extreme points( LTop LBottom RTop RBottom )
    # reference: https://www.cnblogs.com/DOMLX/p/8763369.html
    cnt_img = np.float32(cnt_img)
    dst = cv2.cornerHarris(cnt_img, 6, 11, 0.06)
    dst = cv2.dilate(dst, None)
    img[dst > 0.01 * dst.max()] = [0, 255, 0]

    corner_coordinates = extract_extreme_points(img)

    # the order of extracted coordinates is random, and below is used to make sure it is in the order I want
    Left, Right = sorted(corner_coordinates)[:2], sorted(corner_coordinates)[-2:]
    LT, LB = sorted(Left, key=lambda x: x[1])[0], sorted(Left, key=lambda x: x[1])[1]
    RT, RB = sorted(Right, key=lambda x: x[1])[0], sorted(Right, key=lambda x: x[1])[1]
    dict_corner_coordinates = {x: y for x, y in zip(['LT', 'LB', 'RT', 'RB'], [LT, LB, RT, RB])}
    dict_corner_coordinates['img_H'] = img.shape[0]
    # the code of the line above is used to prepare for change the y coordinate direction of cv2

    print('Four Coordinates:\n', dict_corner_coordinates)
    json_str = json.dumps(dict_corner_coordinates, indent=4)
    save_dir = output_dir + '/' + 'corner_coordinates_pixel.json'
    with open(save_dir, 'w') as json_file:
        json_file.write(json_str)


if __name__ == '__main__':
    extract_corner(surface_name='4-000')