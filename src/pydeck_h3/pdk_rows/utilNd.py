import toolz

from .util import transpose
from .helpers import color_helper, height_helper, hex_helper, line_width_helper


def make_pdk_rows(
    rows,
    col_hex, # how's this gonna generalize when we have hex sets?

    color = (245, 206, 66), # tuple or string
    cmap = 'YlOrRd', #string or callable, but this function doesn't check
    line_width = 1,
    height = None,
):
    # maybe an identity helper???
    cols = [
        hex_helper(rows, col_hex),
        color_helper(rows, color, cmap=cmap),
    ]

    if height is None:
        cols += [line_width_helper(rows, line_width=line_width)]
    else:
        cols += [height_helper(rows, height=height)]


    cols = toolz.merge(*cols)
    _rows = transpose(cols)

    pdk_rows = [
        {
            **row,
            **_row
        }
        for row, _row in zip(rows, _rows)
    ]

    return pdk_rows




