from geomdl import BSpline
from geomdl import exchange
from geomdl.visualization import VisMPL

# Create a BSpline surface instance
surf = BSpline.Surface()

# Set degrees
surf.degree_u = 3
surf.degree_v = 3

# Set control points, shape:5*5
surf.set_ctrlpts(*exchange.import_txt("230208Geomdl_ctrls.cpt", two_dimensional=True))

# Set knot vectors

surf.knotvector_u = [0.00, 0.00, 0.00, 0.00, 83.332890012955080, 166.66578002591020, 166.66578002591020,
                     166.66578002591020, 166.66578002591020]
surf.knotvector_v = [0.00, 0.00, 0.00, 0.00, 68.7135279106180, 179.51076247267970, 179.51076247267970,
                     179.51076247267970, 179.51076247267970]

# Set evaluation delta
surf.delta = 0.025

# Evaluate surface points
surf.evaluate()

# Visualization
vis_config = VisMPL.VisConfig(legend=True, axes=True, figure_dpi=600, trims=False)

vis_obj = VisMPL.VisSurface(vis_config)
surf.vis = vis_obj
surf.render()
#####################################################################
key_values = surf.evaluate_list([[0, 0], [1, 0], [0, 1], [1, 1]])
print('u=0, v=0:', key_values[0])
print('u=1, v=0:', key_values[1])
print('u=0, v=1:', key_values[2])
print('u=1, v=1:', key_values[3])

