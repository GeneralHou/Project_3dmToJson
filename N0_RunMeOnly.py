import N1_Trans3dm2json
import N2_ExtractCorner_real
import N3_ExtractCorner_pixel
import N4_TransScale

'''when processing different surface, change the name below and click run then'''
surface_name = '4-000'  # the pure name of the surface/grid

# create directory to store all coordinates .json files
output_dir = 'Surface' + '_' + surface_name

# to generate nurbs .json file
N1_Trans3dm2json.trans_3dm_2_json(surface_name)

# extract real corner points
N2_ExtractCorner_real.extract_corner(surface_name)

# extract pixel corner points
N3_ExtractCorner_pixel.extract_corner(surface_name)

# translate and scale the coordinates in coordinates.json to real coordinates
N4_TransScale.trans_scale(surface_name)
