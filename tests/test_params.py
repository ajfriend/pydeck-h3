import pydeck_h3 as pdh
from pytest import approx

rows2d = [
    {
        'h3cell': '89283082807ffff',
        'cats': 6,
        'dogs': 15,
        '_pdk_h3cell': '89283082807ffff',
        '_pdk_fill_color': (254, 191, 90, 255),
        '_pdk_line_width': 15,
    },
    {
        'h3cell': '89283082833ffff',
        'cats': 0,
        'dogs': 5,
        '_pdk_h3cell': '89283082833ffff',
        '_pdk_fill_color': (255, 255, 204, 255),
        '_pdk_line_width': 5,
    },
    {
        'h3cell': '8928308283bffff',
        'cats': 18,
        'dogs': 1,
        '_pdk_h3cell': '8928308283bffff',
        '_pdk_fill_color': (128, 0, 38, 255),
        '_pdk_line_width': 1,
    }
]

rows3d = [
    {
        'h3cell': '89283082807ffff',
        'cats': 6,
        'dogs': 15,
        '_pdk_fill_color': (254, 191, 90, 255),
        '_pdk_elevation': 15,
        '_pdk_h3cell': '89283082807ffff',
    },
    {
        'h3cell': '89283082833ffff',
        'cats': 0,
        'dogs': 5,
        '_pdk_fill_color': (255, 255, 204, 255),
        '_pdk_elevation': 5,
        '_pdk_h3cell': '89283082833ffff',
    },
    {
        'h3cell': '8928308283bffff',
        'cats': 18,
        'dogs': 1,
        '_pdk_fill_color': (128, 0, 38, 255),
        '_pdk_elevation': 1,
        '_pdk_h3cell': '8928308283bffff',
    }
]


def test_2d_layer():

    layer_params = pdh.params.get_layer_params(rows2d, opacity=.3)
    layer_expected = {
        'pickable': True,
        'extruded': False,
        'opacity': 0.3,
        'get_hexagon': '_pdk_h3cell',
        'get_fill_color': '_pdk_fill_color',
        'get_line_width': '_pdk_line_width',
    }

    assert layer_params == approx(layer_expected)


def test_2d_deck():

    deck_params = pdh.params.get_deck_params(rows2d, hide_underscored=True)
    deck_expected = {
        'initial_view_state': {"latitude": 37.776346003249365, "longitude": -122.42312111464462, "zoom": 16},
        'tooltip': {'html': '<b>h3cell</b>: {h3cell}<br/><b>cats</b>: {cats}<br/><b>dogs</b>: {dogs}'},
        'map_style': 'light'
    }

    assert eval(deck_params['initial_view_state'].to_json()) == approx(deck_expected['initial_view_state'])

    del deck_params['initial_view_state']
    del deck_expected['initial_view_state']

    assert deck_params == deck_expected


def test_3d_layer():
    layer_params = pdh.params.get_layer_params(
        rows3d,
        opacity = .123,
        wireframe = True,
        elevation_scale = 123,
    )

    layer_expected = {
        'pickable': True,
        'extruded': True,
        'opacity': 0.123,
        'wireframe': True,
        'elevation_scale': 123,
        'get_hexagon': '_pdk_h3cell',
        'get_fill_color': '_pdk_fill_color',
        'get_elevation': '_pdk_elevation',
    }

    assert layer_params == approx(layer_expected)
