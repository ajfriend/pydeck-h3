"""
Basic 2D and 3D plotting; takes in a list of dictionaries
"""

import pydeck as pdk
import pandas as pd
import json

from .params import get_deck_params, get_layer_params
from .pdk_rows.utilNd import make_pdk_rows
from .dispatch import dispatch


def plot_rows(
    rows,
    *,
    col_hex = 'h3cell',

    color = (245, 206, 66),
    cmap = 'YlOrRd',
    line_width = 1,
    height = None,

    opacity = .7,
    wireframe = False,
    elevation_scale = 20,
    hide_underscored = True,
):
    """
    Parameters
    ----------
    rows : DataFrame or list of dictionaries with keys for hex, color, height, etc.
    """

    #rows = json.loads(json.dumps(rows))

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
        opacity = opacity,
        wireframe = wireframe,
        elevation_scale = elevation_scale,
    )

    deck_params = get_deck_params(pdk_rows, hide_underscored=hide_underscored)

    layer = pdk.Layer('H3HexagonLayer', pdk_rows, **layer_params)
    deck = pdk.Deck([layer], **deck_params)

    return deck


def plot(data, **kwargs):
    """

    todo: but how to describe default values?
    todo: where am i actually "using" the default param behavior?
    todo: test/issue for the numpy int error?

    Parameters
    ----------
    data : list[dict], set, list[str], tuple[str], dict[str->number], pandas.DataFrame, pandas.Series
        Data to plot
    col_hex : str
        In the case of record data (list[dict] or DataFrame), name of column containing H3 cell index
    color : 3-tuple[int], 4-tuple[int], str
        If a tuple, gives the RGB/RGBA color to color all hexes; values in [0, 255]
        If str, gives the name of the column with number values that should be mapped to colors
    cmap : str or callable
    line_width : number or str
    height : None, number, or str.
    opacity : float
        [0, 1] for all hexagons. for changing the opacity of specific hexagons, color them with an RGBA value
    wireframe : bool
    elevation_scale : float
    hide_underscored : bool
    """
    rows, info = dispatch(data)
    kwargs.update(info)

    return plot_rows(rows, **kwargs)

