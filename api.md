
set
hexid -> float/int
hexid -> {'val1': bah, 'val2': bah}
rows of ('hexid_col': hexid, 'val1': 3, 'val2': .4)

all 4 of these get mapped to: hexid -> {'val1': bah, 'val2': bah}

plot_hexset(hexes, fill_color=(245, 206, 66), opacity=.7, line_width=1)
plot_hexvals(hexvals, cmap='YlOrRd', opacity=.7, line_width=1)
plot_hexvals3D(hexvals, cmap='YlOrRd', opacity=.7, wireframe=True, elevation_scale=20)
plot_hexvals4D(
    cellmap,
    col_hex = 'hex',
    col_color = 'val1',
    col_height = 'val2',
    cmap = 'YlOrRd',
    elevation_scale = 20,
    opacity = .7,
    wireframe = True,
):

## **internal** interface

everything takes in a hexvals: hexid -> dict

hexvals/hexmap/hexdict? best name?

def plot_hexmap(hexmap, color=None, height=None)

if both None: set
if color not none: 
if height not none: 3d

but how to distinguish color name 'YlGn' from column name? don't worry! this is the *internal api*! we can make it mean whatever we want

what if it **just** takes in a hexmap? look at the first `_pdk` dict to see what we need

## new plan

takes in list of dicts (rows)


plot2d(rows, default_color='yellow', col_hex=None, col_color=None, color_map='blah')

todo: easy way to make the colors consistent across maps?

