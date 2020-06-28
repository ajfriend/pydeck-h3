import matplotlib.pyplot as plt
import toolz
import pandas as pd

import pydeck as pdk
import h3

"""
todo: list of map tiles that people can use
todo: explain colormaps
todo: what if we set `col_height=None` to get a 2d map (and works with DF!)
"""


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


def dict2rows(d, col_hex='hex', col_val='value'):
    out = [
        {col_hex: h, col_val: v}
        for h,v in d.items()
    ]

    return out


def rows2dict(rows, col_hex='hex', col_val='value'):
    out = {
        r[col_hex]: r[col_val]
        for r in rows
    }

    return out


def normalize_dict(d):
    if len(d) == 0:
        return d

    v = d.values()
    vmin, vmax = min(v), max(v)
    spread = vmax-vmin

    if spread == 0:
        d = {k: 1.0 for k in d}
    else:
        d = {
            k: (v-vmin)*1.0/spread
            for k,v in d.items()
        }

    return d


def addcolor(data, cmap='YlOrRd', col_hex='hex', col_val='value', col_color='_color'):
    """

    todo: easy to add a constant color?

    Parameters
    ----------
    data : List[Dict[str, Any]]
        List of hexagon data to plot.
    cmap : str or matplotlib.Colormap
        'YlOrRd' or 'YlOrRd_r' to reverse order!


    Returns
    -------
    Return new list of rows, augmented with `colo_color` column.

    Example
    -------
    >>> data = [
    ...    {'hex': '89283082807ffff', 'value': 1},
    ...    {'hex': '89283082833ffff', 'value': 0},
    ...    {'hex': '8928308283bffff', 'value': 9}]
    >>>
    >>> addcolor(data, cmap='YlOrRd', col_color='_color')
    [{'hex': '89283082807ffff', 'value': 1, '_color': (255, 239, 165)},
     {'hex': '89283082833ffff', 'value': 0, '_color': (255, 255, 204)},
     {'hex': '8928308283bffff', 'value': 9, '_color': (128, 0, 38)}]
    """
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)

    def foo(value):
        r,g,b,a = cmap(value, bytes=True)

        return int(r), int(g), int(b)

    colors = rows2dict(data, col_hex=col_hex, col_val=col_val)
    colors = normalize_dict(colors)
    colors = toolz.valmap(foo, colors)

    out = [
        toolz.assoc(row, col_color, colors[row[col_hex]])
        for row in data
    ]

    return out


def plot_hexset(hexes, fill_color=(245, 206, 66), opacity=.7, line_width=1):
    """
    Plot a collection of hexagons.
    Doesn't consider any values associated to the hexagons (count, value, etc.).

    Parameters
    ----------
    hexes : Iterable[str]
        An iterable of H3 hexagons in string representation.
        Set, list, tuple, pandas.Series, etc.

    Returns
    -------
    pydeck.DeckGLWidget
        Renders the map inside a Jupyter Notebook

    Notes
    -----
    Currently can only plot hexagons which are all the same resolution.
    Issue raised here: https://github.com/uber/deck.gl/issues/4329
    """
    view = compute_view(hexes)

    data = [
        {'hex': h}
        for h in hexes
    ]

    layer = pdk.Layer(
        'H3HexagonLayer',
        data,
        get_hexagon = 'hex',
        pickable = True,
        extruded = False,

        opacity = opacity,
        get_fill_color = fill_color,
        get_line_width = line_width,
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
    )

    #deckgl_widget = d.show()

    return d


def plot_hexvals(hexvals, cmap='YlOrRd', opacity=.7, line_width=1):
    """
    Plot a collection of hexagons and associated values.

    Parameters
    ----------
    hexvals : Dict[str, float]
        Mapping of hexids to values to plot.

    Returns
    -------
    pydeck.DeckGLWidget
        Renders the map inside a Jupyter Notebook
    """
    data = dict2rows(hexvals)
    data = addcolor(data, cmap)
    view = compute_view(hexvals)

    layer = pdk.Layer(
        'H3HexagonLayer',
        data,
        get_hexagon = 'hex',
        pickable = True,
        extruded = False,

        opacity = opacity,
        get_fill_color = '_color',
        get_line_width = line_width,
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
        tooltip = get_tooltip(data, 'value'),
    )

    return d


def plot_hexvals3D(hexvals, cmap='YlOrRd', opacity=.7, wireframe=True, elevation_scale=20):
    """
    Plot a collection of hexagons and associated values.

    Parameters
    ----------
    hexvals : Dict[str, float]
        Mapping of hexids to values to plot.

    Returns
    -------
    pydeck.DeckGLWidget
        Renders the map inside a Jupyter Notebook
    """
    data = dict2rows(hexvals)
    data = addcolor(data, cmap)
    view = compute_view(hexvals, tilt=True)

    layer = pdk.Layer(
        'H3HexagonLayer',
        data,
        get_hexagon = 'hex',
        pickable = True,
        extruded = True,

        opacity = opacity,
        get_fill_color = '_color',
        #get_line_width = line_width, # doesn't do anything for 3d

        wireframe = wireframe,
        elevation_scale = elevation_scale,
        get_elevation = 'value',
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
        tooltip = get_tooltip(data, 'value'),
    )

    return d


def get_tooltip(data, col_hex='hex'):
    keys = list(data[0].keys())
    keys = [k for k in keys if not k.startswith('_')]

    assert col_hex in keys

    keys.remove(col_hex)
    keys.append(col_hex)

    s = '<br/>'.join(
        '<b>{}</b>: {}'.format(k, '{'+k+'}')
        for k in keys
    )

    return {"html": s}


def plot_hexvals4D(
    data,
    col_hex = 'hex',
    col_color = 'val1',
    col_height = 'val2',
    cmap = 'YlOrRd',
    elevation_scale = 20,
    opacity = .7,
    wireframe = True,
    return_widget = True,
):
    """
    Plot a collection of hexagons and associated values.

    Parameters
    ----------
    data : List[ Dict[str, Any] ]
        List of properties for each hex.
        E.g., `{'hex': '89283082807ffff', 'color_val': 6, 'height_val': 1.2}`

    Returns
    -------
    pydeck.DeckGLWidget
        Renders the map inside a Jupyter Notebook
    """
    def prep_data(data):
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')

        # could have this keep track of the colors seen so far...!
        data = addcolor(data, cmap=cmap, col_hex=col_hex, col_val=col_color, col_color='_color')

        return data

    data = prep_data(data)

    hexes = {r[col_hex] for r in data}
    view = compute_view(hexes, tilt=True)

    layer = pdk.Layer(
        'H3HexagonLayer',
        data,
        get_hexagon = col_hex,
        pickable = True,
        extruded = True,

        opacity = opacity,
        get_fill_color = '_color',
        #get_line_width = line_width, # doesn't do anything for 3d

        wireframe = wireframe,
        elevation_scale = elevation_scale,
        get_elevation = col_height,
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
        tooltip = get_tooltip(data, col_hex),
    )
    d.prep_data = prep_data

    if return_widget:
        return d.show()
    else:
        return d
