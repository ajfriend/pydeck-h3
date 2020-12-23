import pydeck_h3 as pdh


rain_data = [
    {'h3cell': '89283082807ffff', 'cats': 6,  'dogs': 15},
    {'h3cell': '89283082833ffff', 'cats': 0,  'dogs': 5},
    {'h3cell': '8928308283bffff', 'cats': 18, 'dogs': 1},
]

def test_2d():
    expected = [
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

    out = pdh.pdk_rows.utilNd.make_pdk_rows(
        rain_data,
        'h3cell',
        color = 'cats',
        cmap = 'YlOrRd',
        line_width = 'dogs',
    )

    assert out == expected


def test_3d():
    expected = [
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

    out = pdh.pdk_rows.utilNd.make_pdk_rows(
        rain_data,
        'h3cell',
        color = 'cats',
        height = 'dogs',
    )

    assert out == expected
