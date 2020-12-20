import pydeck as pdk
import h3


MB_KEY = 'pk.eyJ1IjoiYWpmcmllbmQiLCJhIjoiY2pmbmRjczJmMTVkMzJxcW92Y2E4cHZjdCJ9.Jf-gFXU7FOIQxALzPajbdg'


def plot2d(rows, opacity=.7, hide_underscored=True):
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
    tooltip = _get_tooltip(rows[0], hide_underscored=hide_underscored)

    d = pdk.Deck(
        [layer],
        initial_view_state = _compute_view(hexes),
        tooltip = tooltip,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
    )

    return d


def plot3d(rows, opacity=.7, wireframe=False, elevation_scale=20, hide_underscored=True):

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
    tooltip = _get_tooltip(rows[0], hide_underscored=hide_underscored)

    d = pdk.Deck(
        [layer],
        initial_view_state = _compute_view(hexes, tilt=True),
        tooltip = tooltip,
        mapbox_key = MB_KEY,
        map_style = 'mapbox://styles/mapbox/light-v10',
    )

    return d


def _compute_view(hexes, tilt=False):
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

def _get_tooltip(keys, hide_underscored=True):
    """probably want to make sure the hexid is the first key!

    keys: list of strings, or dict with strings for keys
    """
    keys = list(keys)

    if hide_underscored:
        keys = [k for k in keys if not k.startswith('_')]

    s = '<br/>'.join(
        '<b>{}</b>: {}'.format(k, '{'+k+'}')
        for k in keys
    )

    return {"html": s}
