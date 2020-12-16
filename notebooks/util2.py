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


def set2cellmap(cells, _pdk=None):
    def get_pdk():
        if _pdk is None:
            return {}
        else:
            return _pdk

    cellmap = {
        h: dict(_pdk=get_pdk())
        for h in cells
    }

    return cellmap


def dict2cellmap(data, col_val='value'):
    cellmap = {
        h: {
            col_val: v,
            '_pdk': {} # should this have default values?
           }
        for h,v in data.items()
    }

    return cellmap


def cellmap2records(cellmap, col_hex='h3cell'):
    records = [
        toolz.merge({col_hex: k}, v)
        for k, v in cellmap.items()
    ]

    return records


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

def get_tooltip(data):
    """probably want to make sure the hexid is the first key!
    """
    keys = list(data[0].keys()) # wanna check all the keys? not just the first

    keys = [k for k in keys if not k.startswith('_')]

    s = '<br/>'.join(
        '<b>{}</b>: {}'.format(k, '{'+k+'}')
        for k in keys
    )

    return {"html": s}


from copy import deepcopy

def addcolor(cellmap, cmap='YlOrRd', col_val='value'):
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)

    def foo(value):
        r,g,b,a = cmap(value, bytes=True)

        return int(r), int(g), int(b)

    colors = {h: v[col_val] for h,v in cellmap.items()}
    colors = normalize_dict(colors)
    colors = toolz.valmap(foo, colors)

    cellmap = deepcopy(cellmap)

    for h, c in colors.items():
        d = cellmap[h]
        if '_pdk' not in  d:
            d['_pdk'] = {}

        d['_pdk']['fill_color'] = c


    return cellmap


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

    opt = {
        'fill_color': fill_color,
        'line_width': line_width,
    }

    data = set2cellmap(hexes, _pdk=opt)

    ## before this point, have some `prep_hexset` function.
    # everything below this should be basically the same across functions

    data = cellmap2records(data, col_hex='h3cell')

    layer = pdk.Layer(
        'H3HexagonLayer',
        data,

        get_hexagon = 'h3cell',
        get_fill_color = '_pdk.fill_color',
        get_line_width = '_pdk.line_width',

        pickable = True,
        extruded = False,
        opacity = opacity
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
        tooltip = get_tooltip(data),
    )

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
    view = compute_view(hexvals)

    cellmap = dict2cellmap(hexvals)
    cellmap = addcolor(cellmap, cmap)

    for d in cellmap.values():
        d['_pdk']['line_width'] = line_width


    data = cellmap2records(cellmap, col_hex='h3cell')
    layer = pdk.Layer(
        'H3HexagonLayer',
        data,

        get_hexagon = 'h3cell',
        get_fill_color = '_pdk.fill_color',
        get_line_width = '_pdk.line_width', # could fill these _pdk things out automatically...

        pickable = True,
        extruded = False,
        opacity = opacity
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
        tooltip = get_tooltip(data),
    )

    return d


"""
should this guy normalize the elevation?

"""
def plot_hexvals3D(hexvals, cmap='YlOrRd', opacity=.7, wireframe=True, elevation_scale=20):
    view = compute_view(hexvals, tilt=True)

    cellmap = dict2cellmap(hexvals)
    cellmap = addcolor(cellmap, cmap)

    for d in cellmap.values():
        d['_pdk']['elevation'] = d['value']

    data = cellmap2records(cellmap, col_hex='h3cell')
    layer = pdk.Layer(
        'H3HexagonLayer',
        data,

        get_hexagon = 'h3cell',
        get_fill_color = '_pdk.fill_color',
        #get_line_width = line_width, # doesn't do anything for 3d
        get_elevation = '_pdk.elevation',

        pickable = True,
        extruded = True,
        opacity = opacity,
        wireframe = wireframe,
        elevation_scale = elevation_scale,
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
        tooltip = get_tooltip(data),
    )

    return d




"""
todo: something to denote which is color and which is height?

todo: height normalization should have a "start at zero?" option?
    maybe it should error out if any values are negative?
"""
def plot_hexvals4D(
    cellmap,
    col_hex = 'hex',
    col_color = 'val1',
    col_height = 'val2',
    cmap = 'YlOrRd',
    elevation_scale = 20,
    opacity = .7,
    wireframe = True,
):
    view = compute_view(cellmap, tilt=True)

    cellmap = addcolor(cellmap, cmap, col_val=col_color) # this thing needs a better name
    # col val should be col_color?

    for d in cellmap.values():
        # we should probably normalize the height, yeah?
        d['_pdk']['elevation'] = d[col_height]

    data = cellmap2records(cellmap, col_hex='h3cell')
    layer = pdk.Layer(
        'H3HexagonLayer',
        data,

        get_hexagon = 'h3cell',
        get_fill_color = '_pdk.fill_color',
        #get_line_width = line_width, # doesn't do anything for 3d
        get_elevation = '_pdk.elevation',

        pickable = True,
        extruded = True,
        opacity = opacity,
        wireframe = wireframe,
        elevation_scale = elevation_scale,
    )

    d = pdk.Deck(
        [layer],
        initial_view_state = view,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
        tooltip = get_tooltip(data),
    )

    return d
