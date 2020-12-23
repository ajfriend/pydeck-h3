import pydeck_h3 as pdh
import matplotlib.pyplot as plt

rows = [
    {'cats': 6, 'dogs': 15},
    {'cats': 0, 'dogs': 5},
    {'cats': 18, 'dogs': 1},
]

def test_color_helper():
    out = pdh.pdk_rows.helpers.color_helper(rows, color='cats', cmap='YlOrRd')
    expected = {
        '_pdk_fill_color': [
            (254, 191, 90, 255),
            (255, 255, 204, 255),
            (128, 0, 38, 255)
        ]
    }

    assert out == expected


    out = pdh.pdk_rows.helpers.color_helper(rows, color='dogs', cmap='coolwarm')
    expected = {
        '_pdk_fill_color': [
            (179, 3, 38, 255),
            (153, 186, 254, 255),
            (58, 76, 192, 255),
        ]
    }

    assert out == expected


    out = pdh.pdk_rows.helpers.color_helper(rows, color=(1,2,3,4))
    expected = {
        '_pdk_fill_color': [
            (1,2,3,4),
            (1,2,3,4),
            (1,2,3,4),
        ]
    }

    assert out == expected


    cmap = plt.get_cmap('PuOr')
    out = pdh.pdk_rows.helpers.color_helper(rows, color='dogs', cmap=cmap)
    expected = {
        '_pdk_fill_color': [
            (45, 0, 75, 255),
            (249, 176, 88, 255),
            (127, 59, 8, 255),
        ]
    }

    assert out == expected
