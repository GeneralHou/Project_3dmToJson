import cv2
import json

def missing_coordinates(surface_name):
    output_dir = 'Surface_' + surface_name

    def shw_img(image):
        cv2.imshow('', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    img = cv2.imread(F'{output_dir}/{surface_name}_crop.png')


    with open(f'{output_dir}/coordinates.json', 'r') as f:
        result = json.load(f)
        # int(k) is used to change the key from '1' to 1
        # use 'img_H - v[1]' to change y coordinate direction
        coordinates = {int(k): v for k, v in result.items()}


    with open(f'{output_dir}/coordinates_missing.json', 'r') as f:
        miss_key = json.load(f)

    for item in miss_key:
        cv2.circle(img, tuple(coordinates[item]), 2, (0,0,255), 2)

    shw_img(img)

if __name__ == '__main__':
    missing_coordinates(surface_name='S19_0')