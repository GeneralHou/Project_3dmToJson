import json
# the data amount of S19 is 17*33
# the real left bottom is: [0.00, -20.00]
# pixel coordinates of  S19: left_bottom = [39, 640], right_top = [1628, 243]

def trans_scale(surface_name):
    output_dir = 'Surface_' + surface_name
    '''coordinates'''
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

    # align the pixel coordinates to real coordinates
    def align_coordinates(coordinate):
        pixel_lf_bt = pixel_corner_coordinates[0]
        real_lf_bt = real_corner_coordinates[0]
        mv_x = pixel_lf_bt[0] - real_lf_bt[0]
        mv_y = pixel_lf_bt[1] - real_lf_bt[1]
        align_crd = {}
        for i in range(len(coordinate)):
            temp = [coordinate[i][0] - mv_x, coordinate[i][1] - mv_y]
            align_crd[i] = temp
        return align_crd


    '''Trans'''
    aligned_coordinates = align_coordinates(coordinates)
    print('■■Aligned coordinates(Total %d):' % len(aligned_coordinates),
          'The first 10 is:\n', {x:y for x, y in aligned_coordinates.items() if x < 10})

    '''Scale'''
    aligned_corner = align_coordinates(pixel_corner_coordinates)
    print('■■Aligned corner:', aligned_corner)
    scale_factor = [
        (aligned_corner[1][x]-aligned_corner[0][x])/(real_corner_coordinates[1][x]-real_corner_coordinates[0][x])
        for x in [0, 1]]  # calculate the scale factor in x and y direction,respectively
    print('■■The scale factor [x,y]:', scale_factor)

    scaled_coordinates = {}
    for i in range(len(aligned_coordinates)):
        temp_x = (aligned_coordinates[i][0] - aligned_corner[0][0]) / scale_factor[0] + real_corner_coordinates[0][0]
        temp_y = (aligned_coordinates[i][1] - aligned_corner[0][1]) / scale_factor[1] + real_corner_coordinates[0][1]
        scaled_coordinates[i] = [round(temp_x, 2), round(temp_y, 2), 0]
    print('■■Scaled coordinates(Total %d):' % len(scaled_coordinates),
          'The first 10 is:\n', {x:y for x, y in scaled_coordinates.items() if x < 10})

    json_str = json.dumps(scaled_coordinates, indent=4)
    save_dir = output_dir + '/' + 'coordinates_TSed.json'
    with open(save_dir, 'w') as json_file:
        json_file.write(json_str)


if __name__ == '__main__':
    trans_scale(surface_name='4-000')