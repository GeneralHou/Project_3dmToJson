import json
import cv2

# the data amount of S19 is 17*33
# the real left bottom is: [0.00, -20.00]
# pixel coordinates of  S19: left_bottom = [39, 640], right_top = [1628, 243]

def shw_img(img, title='default'):
    cv2.namedWindow(title, 0)
    w, h = min(1920, img.shape[1]), min(1080, img.shape[0])
    cv2.resizeWindow(title, w, h) # w and h
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def trans_scale(surface_name):
    output_dir = 'Surface_' + surface_name
    '''''''''LOAD COORDINATES'''''''''
    # 2 raw pixel corner points: left_bottom, right_top
    with open(f'{output_dir}/corner_coordinates_pixel.json', 'r') as f:
        result = json.load(f)
    img_H = result['img_H']  # this line is used to change the direction of y in cv2
    pixel_corner_coordinates_temp = [result['LB'], result['RT']]
    # use 'img_H - y' to change y coordinate direction
    pixel_corner_coordinates = [[x, img_H - y] for x, y in pixel_corner_coordinates_temp]

    # do not change the name of varies, but just the value
    # raw pixel coordinates
    with open(f'{output_dir}/coordinates.json', 'r') as f:
        result = json.load(f)
    # int(k) is used to change the key from '1' to 1
    # use 'img_H - v[1]' to change y coordinate direction
    coordinates = {int(k): [v[0], img_H-v[1]] for k, v in result.items()}

    # 2 real corner points: left_bottom, right_top
    with open(f'{output_dir}/corner_coordinates_real.json', 'r') as f:
        result = json.load(f)
    real_corner_coordinates = [result['LB'], result['RT']]

    '''''''''AID FUNCTION'''''''''
    # align the pixel coordinates to real coordinates
    def align_coordinates(coordinate):
        align_crd = {}
        for i in range(len(coordinate)):
            temp = [coordinate[i][0] - mv_x, coordinate[i][1] - mv_y]
            align_crd[i] = temp
        return align_crd


    '''''''''ADJUST TRANS DISTANCE'''''''''
    # calculate move distance in two directions
    pixel_lf_bt = pixel_corner_coordinates[0]
    real_lf_bt = real_corner_coordinates[0]
    mv_x = pixel_lf_bt[0] - real_lf_bt[0]
    mv_y = pixel_lf_bt[1] - real_lf_bt[1]
    print(f'■■■PART ONE: The default translate in x and y direction: {mv_x}, {mv_y}')
    # adjust the trans distance (when we can't fully project and get z coordinate)
    print("Adjust the trans distance above when can't fully project to get z coordinate.")
    print("Coordinate system is same as Gaussian coordinate in Rhino.")
    adjust_x = input("Adjust in x direction['Enter' to confirm or quit]:")
    adjust_y = input("Adjust in y direction['Enter' to confirm or quit]:")
    if adjust_x: mv_x = mv_x - float(adjust_x)  # if do not make any adjust, 'if' is False
    if adjust_y: mv_y = mv_y - float(adjust_y)

    # calculate this part(most import)
    aligned_coordinates = align_coordinates(coordinates)


    '''''''''ADJUST SCALE FACTOR'''''''''
    # pixel coordinate prepare for scale
    aligned_corner = align_coordinates(pixel_corner_coordinates)

    # calculate scale factor
    scale_factor_x = (aligned_corner[1][0]-aligned_corner[0][0])/(real_corner_coordinates[1][0]-real_corner_coordinates[0][0])
    scale_factor_y = (aligned_corner[1][1]-aligned_corner[0][1])/(real_corner_coordinates[1][1]-real_corner_coordinates[0][1])
    print(f'\n■■■PART TWO: The default scale factor in x and y direction: {scale_factor_x}, {scale_factor_y}')
    # Adjust the scale factor above when can't fully project to get z coordinate
    print("Adjust the scale factor above when can't fully project to get z coordinate.")
    new_factor_x = input("Adjust in x direction['Enter' to confirm or quit]:")
    new_factor_y = input("Adjust in y direction['Enter' to confirm or quit]:")
    new_factor_x = float(new_factor_x) if new_factor_x else scale_factor_x  # if do not make any adjust, 'if' is False
    new_factor_y = float(new_factor_y) if new_factor_y else scale_factor_y

    # calculate this part(most import)
    scaled_coordinates = {}
    for i in range(len(aligned_coordinates)):
        temp_x = (aligned_coordinates[i][0] - aligned_corner[0][0]) / new_factor_x + real_corner_coordinates[0][0]
        temp_y = (aligned_coordinates[i][1] - aligned_corner[0][1]) / new_factor_y + real_corner_coordinates[0][1]
        scaled_coordinates[i] = [round(temp_x, 2), round(temp_y, 2), 0]
    
    
    '''''''''SAVE FINAL RESULT'''''''''
    json_str = json.dumps(scaled_coordinates, indent=4)
    save_dir = output_dir + '/' + 'coordinates_TSed.json'
    with open(save_dir, 'w') as json_file:
        json_file.write(json_str)


if __name__ == '__main__':
    trans_scale(surface_name='4-000')