how to use Project_3dmToJson:
virtual environment(in my shcool desktop): nurbs

※※※※※※※
Please prepare three files:   
***.3dm   
***_crop.png(from FindCoordinate)
coordinates.json

Step1: before start, please put '.3dm' under the directory of 'Trans3dm3json
       
Step2: then create a directory named 'Surface_surface_name' in the same level directory of this file(N0_RunMeOnly.py)
       e.g.: if the surface_name is D23(or S19), then the name of the directory should be: Surface_D23(or Surface_S19)

Step3: put the corresponding .png(the synthesized grid image after crop) and the coordinates.json under the directory above

Step3: open N0_RunMeOnly.py and change the string pass to variable "surface_name"

Step4: clik Run

--------------------------------
■■■■To get the 3d coordinates:
we need to interact with ■rhino■ using the corresponding code, namely run N5_project2Space.py in Rhino.
in Rhino: type 'runpythonscipt'


--------------------------------
■■■■In order to get the corresponding 3d .html file, we need to put the "coordinates_space.json" under "20230102FindCoordinate" and run "N7_UseCoordTopoDrawGrid_3D.py"

