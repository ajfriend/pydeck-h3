import matplotlib.pyplot as plt
import toolz
import pandas as pd

import matplotlib.pyplot as plt


def get_scaled_cmap(cmap='YlOrRd', lower=0.0, upper=1.0):

    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)

    if lower == upper:
        pass # what to do!

    def foo(value):
        assert lower <= value <= upper

        if lower == upper:
            value = 1.0
        else:
            value = (value - lower)/float(upper - lower)

        out = cmap(value, bytes=True)
        out = map(int, out)

        r, g, b, a = out

        return r,g,b,a

    return foo


def make_pdk_rows(
    rows,
    col_hex,

    color = (245, 206, 66), # tuple or string
    cmap = 'YlOrRd', #string or callable, but this function doesn't check

    line_width = 1,
):
    if isinstance(color, tuple):
        colors = (color for _ in rows)
    else:
        a = min(row[color] for row in rows)
        b = max(row[color] for row in rows)
        cmap = get_scaled_cmap(cmap, a, b)
        colors = (cmap(row[color]) for row in rows)

    if isinstance(line_width, str):
        line_widths = (row[line_width] for row in rows)
    else:
        line_widths = (line_width for _ in rows)

    pdk_rows = [
        {
            **row,
            '_pdk_h3cell': row[col_hex],
            '_pdk_fill_color': color,
            '_pdk_line_width': line_width,
        }
        for row, color, line_width in zip(rows, colors, line_widths)
    ]

    return pdk_rows




