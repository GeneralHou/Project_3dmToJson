# This script should work together with Rhino
# cd to Trans3dm2json 
# open the corresponding ***.3dm file                  -------extremely important
# change surface_name = *** (the final line of code)   -------extremely important
# load and run this script in Rhino

# Please DO NOT run this in Pycharm ~

import rhinoscriptsyntax as rs
import json

def Project2Space(surface_name):
    # load the planar coordinates
    json_path = './' + 'Surface_' + surface_name + '/' + 'coordinates_TSed.json'
    with open(json_path, 'r') as f:
        result = json.load(f)
    coordinates = {int(k): tuple(v) for k, v in result.items()}


    # get the surface
    all_sur = rs.filter.surface  # use filter to get all surfaces
    sur_ids = rs.ObjectsByType(all_sur, select=True)  # get ids of surfaces
    surface = sur_ids[0]  # get first one (actually we only have one)

    # begin to project
    projected = {}
    miss_n = 0
    miss_coord_key = []
    for i in range(len(coordinates)):
        result = rs.ProjectPointToSurface(coordinates[i], surface, (0,0,-1))
        if len(result) > 0:
            result = result[0]  # without this line, it will have bug when running the code next line
            projected[i] = [round(result.X,2), round(result.Y,2), round(result.Z,2)]
        else:
            # miss_coord_key.append(i)
            # miss_n += 1
            factor = 0.01
            while True:
                expand_direct = [[0,1,0], [1,0,0], [0,-1,0], [-1,0,0]]
                for direct in expand_direct:
                    shift = [sft * factor for sft in direct]
                    new_coord = [v1+v2 for v1,v2 in zip(coordinates[i], shift)]
                    result = rs.ProjectPointToSurface(new_coord, surface, (0,0,-1))
                    if len(result) > 0:
                        result = result[0]
                        projected[i] = [round(result.X,2), round(result.Y,2), round(result.Z,2)]
                        break
                if len(result) > 0: break
                factor += 0.01

    json_str = json.dumps(projected, indent=4)
    save_dir = './' + 'Surface_' + surface_name + '/' + 'coordinates_space.json'
    with open(save_dir, 'w') as json_file:
        json_file.write(json_str)
    
    if miss_coord_key != []:
        json_str = json.dumps(miss_coord_key, indent=4)
        save_dir = './' + 'Surface_' + surface_name + '/' + 'coordinates_missing.json'
        with open(save_dir, 'w') as json_file:
            json_file.write(json_str)

    print('General Hou remind you: ALL WORK DONE!')
    print('The generated coordinates_space.json is in directory: Surface_%s' %surface_name)
    print('total_n', len(coordinates), 'missing_n:', miss_n)


if __name__ == '__main__':
    Project2Space(surface_name='S19_0')
