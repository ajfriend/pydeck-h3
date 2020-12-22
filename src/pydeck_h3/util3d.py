import toolz

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


def make_pdk_rows(
    rows,
    col_hex,

    color = (245, 206, 66), # tuple or string
    cmap = 'YlOrRd', #string or callable, but this function doesn't check

    height = None,
    line_width = 1,
):
    # have functions that return a dict with key like _pdk_fill_color: iterator
    # then we can just zip up all the iterators at the end
    #
    cols = toolz.merge(
        # maybe an identity helper???
        color_helper(rows, color, cmap='YlOrRd'),
        line_width_helper(rows, line_width=1),
        height_helper(rows, height=None),
        hex_helper(rows, col_hex),
    )

    # pdk_rows = [
    #     {
    #         **row,
    #         '_pdk_h3cell': row[col_hex],
    #         '_pdk_fill_color': color,
    #         '_pdk_line_width': line_width,
    #     }
    #     for row, color, line_width in zip(rows, colors, line_widths)
    # ]

    return cols




