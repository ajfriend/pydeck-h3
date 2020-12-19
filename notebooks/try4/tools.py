import matplotlib.pyplot as plt
import toolz
import pandas as pd

import pydeck as pdk
import h3


MB_KEY = 'pk.eyJ1IjoiYWpmcmllbmQiLCJhIjoiY2pmbmRjczJmMTVkMzJxcW92Y2E4cHZjdCJ9.Jf-gFXU7FOIQxALzPajbdg'


def compute_view(hexes, tilt=False):
    """
    Computes a view based on transforming hexagons
    to their lat/lng points.

    Parameters
    ----------
    hexes : Iterable[str]
        An iterable of H3 hexagons in string representation.
        Set, list, tuple, pandas.Series, etc.
    tilt : bool
        Tilt view if True

    Returns
    -------
    pydeck.View
    """

    view = pdk.data_utils.compute_view(
        [h3.h3_to_geo(h)[::-1] for h in hexes]
    )

    if tilt:
        view.pitch = 45

    return view

def get_tooltip(row):
    """probably want to make sure the hexid is the first key!
    """
    keys = list(row.keys()) # wanna check all the keys? not just the first

    keys = [k for k in keys if not k.startswith('_')]

    s = '<br/>'.join(
        '<b>{}</b>: {}'.format(k, '{'+k+'}')
        for k in keys
    )

    return {"html": s}


#plot2d(rows, default_color='yellow', col_hex=None, col_color=None, color_map='blah')


# maybe this is just a transform function (doesn't call the map)
# it just transforms a row form to the row form with _pdk
def plot2d(
    rows,
    col_hex,

    col_color = None,
    color = (245, 206, 66),  # default/fallback

    line_width = 1,
    col_line_width = None,  # less common: want to have different line widths by hex

    opacity = .7,
    cmap = None,
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
def _plot2d(rows, opacity=.7):
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
        get_hexagon = '_pdk.h3cell',  ## this is better. _pdk is the *real* data, forget about the user input dict, that's metadata. think about the things we actually need for the plot
        get_fill_color = '_pdk.fill_color',
        get_line_width = '_pdk.line_width',
        opacity = opacity,
    )

    view = compute_view({r['_pdk']['h3cell'] for r in rows})
    tooltip = get_tooltip(rows[0])

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        tooltip = tooltip,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
    )

    return d


def plot3d(rows, col_hex, line_width=2.0, opacity=.7, default_color=(245, 206, 66)):
    # make a copy so we can modify the row dictionaries
    rows = [
        dict(row)
        for row in rows
    ]

    # need a color processing step
    _pdk = {
        'fill_color': default_color,
        'elevation': 20,
    }

    for row in rows:
        row['_pdk'] = _pdk

    return _plot3d(rows, col_hex)


def _plot3d(rows, opacity=.7, wireframe=False, elevation_scale=20):

    view = compute_view({r['_pdk']['h3cell'] for r in rows}, tilt=True)
    tooltip = get_tooltip(rows[0])

    layer = pdk.Layer(
        'H3HexagonLayer',
        rows,
        pickable = True,
        extruded = True,

        get_hexagon = '_pdk.h3cell',
        get_fill_color = '_pdk.fill_color',
        get_elevation = '_pdk.elevation',
        elevation_scale = elevation_scale,

        wireframe = wireframe,
        opacity = opacity,
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        tooltip = tooltip,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
    )

    return d

