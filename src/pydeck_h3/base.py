"""
Basic 2D and 3D plotting; takes in a list of dictionaries
"""

import pydeck as pdk

from .params import get_deck_params, get_layer_params
from .pdk_rows.utilNd import make_pdk_rows


def plot(
    rows,
    col_hex,

    color = (245, 206, 66),
    cmap = 'YlOrRd',
    line_width = 1,
    height = None,

    opacity = .7,
    wireframe = False,
    elevation_scale = 20,
    hide_underscored = True,
):
    pdk_rows = make_pdk_rows(
        rows,
        col_hex,
        color = color,
        cmap = cmap,
        line_width = line_width,
        height = height,
    )

    # todo: too easy to mix up `rows` and `pdk_rows`; get a mysterious "missing key" error when it looks for the _pdk_ keys
    layer_params = get_layer_params(
        pdk_rows,
        opacity=opacity,
        wireframe=wireframe,
        elevation_scale=elevation_scale,
    )

    deck_params = get_deck_params(pdk_rows, hide_underscored=hide_underscored)

    layer = pdk.Layer('H3HexagonLayer', pdk_rows, **layer_params)
    deck = pdk.Deck([layer], **deck_params)

    return deck
