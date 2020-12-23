import toolz

from .util import transpose
from .helpers import color_helper, height_helper, hex_helper


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
        #line_width_helper(rows, line_width=1),
        height_helper(rows, height=height),
        hex_helper(rows, col_hex),
    )

    _rows = transpose(cols)

    pdk_rows = [
        {
            **row,
            **_row
        }
        for row, _row in zip(rows, _rows)
    ]

    return pdk_rows




