from geomdl import BSpline
from geomdl import exchange
from geomdl.visualization import VisVTK as vis, VisMPL

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

# Import and use Matplotlib's colormaps
from matplotlib import cm

# Plot the control point grid and the evaluated surface
vis_comp = vis.VisSurface()
surf.vis = vis_comp
surf.render(colormap=cm.cool)
#####################################################################
key_values = surf.evaluate_list([[0, 1], [1, 0]])
print(key_values)

