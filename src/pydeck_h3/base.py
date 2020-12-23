"""
Basic 2D and 3D plotting; takes in a list of dictionaries
"""

import pydeck as pdk

from .params import get_plot_params
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

    params_layer, params_deck = get_plot_params(
        pdk_rows,
        opacity = opacity,
        wireframe = wireframe,
        elevation_scale = elevation_scale,
        hide_underscored = hide_underscored,
    )

    return _plot(pdk_rows, params_layer, params_deck)


def _plot(pdk_rows, opts_layer, opts_deck):
    layer = pdk.Layer('H3HexagonLayer', pdk_rows, **opts_layer)
    deck = pdk.Deck([layer], **opts_deck)

    return deck
