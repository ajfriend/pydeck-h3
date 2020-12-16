
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
