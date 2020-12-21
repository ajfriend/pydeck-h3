import matplotlib.pyplot as plt
import toolz
import pandas as pd

import pydeck as pdk
import h3


MB_KEY = 'pk.eyJ1IjoiYWpmcmllbmQiLCJhIjoiY2pmbmRjczJmMTVkMzJxcW92Y2E4cHZjdCJ9.Jf-gFXU7FOIQxALzPajbdg'



#plot2d(rows, default_color='yellow', col_hex=None, col_color=None, color_map='blah')


# maybe this is just a transform function (doesn't call the map)
# it just transforms a row form to the row form with _pdk
# just a transform will be easier to test
def plot2d(
    rows,
    col_hex,

    # bah, need a record type. importing a function should automatically import its record type constructor (in something like ML, or C even!)
    color = (245, 206, 66),  # dispatch on string vs tuple. or give the user a utility function u.color('yellow'). if string given, assumed that's the name of a column
    cmap = 'YlOrRd',  # let this thing take in a function (if we want global coloring, the function has to do the pre-normalization itself; the function will only look at one element at a time)

    line_width = 1, # dispatch on numeric vs string vs function
    opacity = .7,
):
    """
    line_width: int, float, or str to denote column name

    can have hte color be rgb or rgba tuples

    opacity is multiplicative
    """

    # make a copy so we can modify the row dictionaries
    rows = [
        dict(row)
        for row in rows
    ]
    for row in rows:
        row['_pdk'] = {
            'h3cell': row[col_hex],
            'fill_color': default_color,
            'line_width': line_width,
        }

    return _plot2d(rows, opacity)


# this all ya really need?
def _plot2d(rows, opacity=.7, hide_underscored=True):
    """
    _pdk.h3cell: str
    _pdk.line_width: int, float
    _pdk.fill_color: rgb or rgba tuples

    opacity is multiplicative

    all values in the dict not starting with `_` will be printed int he tooltip
    """

    layer = pdk.Layer(
        'H3HexagonLayer',
        rows,
        pickable = True,
        extruded = False,
        opacity = opacity,

        get_hexagon    = '_pdk_h3cell',
        get_fill_color = '_pdk_fill_color',
        get_line_width = '_pdk_line_width',
    )

    hexes = {r['_pdk_h3cell'] for r in rows}
    tooltip = get_tooltip(rows[0], hide_underscored=hide_underscored)

    d = pdk.Deck(
        [layer],
        initial_view_state = compute_view(hexes),
        tooltip = tooltip,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
    )

    return d


def _plot3d(rows, opacity=.7, wireframe=False, elevation_scale=20, hide_underscored=True):

    layer = pdk.Layer(
        'H3HexagonLayer',
        rows,
        pickable = True,
        extruded = True,
        elevation_scale = elevation_scale,
        wireframe = wireframe,
        opacity = opacity,

        get_hexagon    = '_pdk_h3cell',
        get_fill_color = '_pdk_fill_color',
        get_elevation  = '_pdk_elevation',
    )

    hexes = {r['_pdk_h3cell'] for r in rows}
    tooltip = get_tooltip(rows[0], hide_underscored=hide_underscored)

    d = pdk.Deck(
        [layer],
        initial_view_state = compute_view(hexes, tilt=True),
        tooltip = tooltip,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
    )

    return d

