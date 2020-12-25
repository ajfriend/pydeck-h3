import h3
import pydeck as pdk


MB_KEY = 'pk.eyJ1IjoiYWpmcmllbmQiLCJhIjoiY2pmbmRjczJmMTVkMzJxcW92Y2E4cHZjdCJ9.Jf-gFXU7FOIQxALzPajbdg'


def get_deck_params(rows, hide_underscored=True):

    view = _compute_view(
        hexes = {r['_pdk_h3cell'] for r in rows},
        tilt = ('_pdk_elevation' in rows[0]),
    )

    tooltip = _get_tooltip(rows[0], hide_underscored=hide_underscored)

    params = {
        'initial_view_state': view,
        'tooltip': tooltip,
        'mapbox_key': MB_KEY,
        'map_style': 'mapbox://styles/mapbox/light-v10',
    }

    return params

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
