import pydeck as pdk
import numpy as np
import pandas as pd
import h3


MB_KEY = 'pk.eyJ1IjoiYWpmcmllbmQiLCJhIjoiY2pmbmRjczJmMTVkMzJxcW92Y2E4cHZjdCJ9.Jf-gFXU7FOIQxALzPajbdg'


import toolz

from .pdk_rows.util import transpose
from .pdk_rows.helpers import color_helper


def make_pdk_rows(
    rows,
    color,
    cmap = 'YlOrRd', #string or callable, but this function doesn't check
):
    cols = [
        color_helper(rows, color, cmap=cmap),
    ]


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



def plot(data, col_hex='hexset', col_color='color', cmap='YlOrRd', line_width=100, opacity=0.7):
    """
    data is a list of dictionaries
    OR: if it is a dataframe, it is converted to a list of dictionaries

    !!! currently mutates input! (maybe no longer..)
    """

    if isinstance(data, pd.DataFrame):
        data = data.to_dict('records')

    # just to make it so we don't mutate `data`
    data = [
        dict(row)
        for row in data
    ]

    # if we don't find a color column, just add random values
    # todo: super hacky, gotta fix and make not mutate
    if col_color not in data[0].keys():
        for row in data:
            row[col_color] = int(np.random.randint(len(data)))

    # sets don't parse to json, so make sure the hexset is a row
    for row in data:
        row[col_hex] = list(row[col_hex])

    data = make_pdk_rows(data, col_color, cmap=cmap)

    layer = pdk.Layer(
        'H3ClusterLayer',
        data,
        pickable = True,
        stroked = True,
        filled = True,
        extruded = False,
        get_hexagons = col_hex,
        get_fill_color = '_pdk_fill_color',
        get_line_width = line_width,
        opacity = opacity,
    )

    hexes = set.union(*[
        set(row[col_hex])
        for row in data
    ])

    #todo: can we improve on this? we don't need to send the whole list, probably just the min/max in lat/lng right?
    view = pdk.data_utils.compute_view(
        [h3.h3_to_geo(h)[::-1] for h in hexes]
    )


    deck = pdk.Deck(
        layers = [layer],
        initial_view_state = view,
        map_style = 'light',
    )

    return deck


def plot3d(data, col_hex='hexset', col_color='color', cmap='YlOrRd', opacity=0.7, elevation_scale=100):
    """
    data is a list of dictionaries.

    !!! currently mutates input!
    """

    if isinstance(data, pd.DataFrame):
        data = data.to_dict('records')

    # just to make it so we don't mutate `data`
    data = [
        dict(row)
        for row in data
    ]

    # sets don't parse to json, so make sure the hexset is a row
    for row in data:
        row[col_hex] = list(row[col_hex])

    data = make_pdk_rows(data, col_color, cmap=cmap)

    layer = pdk.Layer(
        'H3ClusterLayer',
        data,
        pickable = True,
        stroked = True,
        filled = True,
        extruded = True,
        get_hexagons = col_hex,
        get_fill_color = '_pdk_fill_color',
        opacity = opacity,
        elevation_scale = elevation_scale,
        get_elevation = col_color,
    )

    hexes = set.union(*[
        set(row[col_hex])
        for row in data
    ])

    #todo: can we improve on this? we don't need to send the whole list, probably just the min/max in lat/lng right?
    view = pdk.data_utils.compute_view(
        [h3.h3_to_geo(h)[::-1] for h in hexes]
    )
    view.pitch = 45


    deck = pdk.Deck(
        layers = [layer],
        initial_view_state = view,
        map_style = 'light',
    )

    return deck
