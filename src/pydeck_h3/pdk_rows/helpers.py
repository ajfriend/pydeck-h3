from .util import get_scaled_cmap


def color_helper(rows, color, cmap='YlOrRd'):

    if isinstance(color, tuple):
        # assume it is an RGB 3-tuple or an RGBA 4-tuple
        colors = (color for _ in rows)
    else:
        a = min(row[color] for row in rows)
        b = max(row[color] for row in rows)

        cmap = get_scaled_cmap(cmap, a, b)

        colors = (cmap(row[color]) for row in rows)

    return {'_pdk_fill_color': colors}


def line_width_helper(rows, line_width=1):

    if isinstance(line_width, str):
        line_widths = (row[line_width] for row in rows)
    else:
        line_widths = (line_width for _ in rows)

    return {'_pdk_line_width': line_widths}


def height_helper(rows, height=None):
    if height is None:
        return dict()
    elif isinstance(height, str):
        heights = (row[height] for row in rows)
    else:
        heights = (height for _ in rows)

    return {'_pdk_elevation': heights}


def hex_helper(rows, col_hex):
    hexes = (row[col_hex] for row in rows)

    return {'_pdk_h3cell': hexes}
